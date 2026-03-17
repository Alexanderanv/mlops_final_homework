from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import os
import json
import logging
import time
import uuid
from typing import Any, Optional

import mlflow
import mlflow.sklearn
import numpy as np
import psycopg2
from psycopg2.extras import Json
from starlette_exporter import PrometheusMiddleware, handle_metrics


class PatientFeatures(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float


app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics, include_in_schema=False)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:8080")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

MODEL_URI = os.getenv("MODEL_URI", "models:/diabets/1")
MODEL_VERSION = os.getenv("MODEL_VERSION") or None
_model = None

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mlservice:mlservice@db:5432/mlservice")


logger = logging.getLogger("mlapp")
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
logger.propagate = False

def log_json(event: str, **fields: Any) -> None:
    payload = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": event,
        **fields,
    }
    logger.info(json.dumps(payload, ensure_ascii=False))

def _features_to_dict(features: PatientFeatures) -> dict[str, Any]:
    return features.model_dump()

def _db_connect():
    return psycopg2.connect(DATABASE_URL)

@app.on_event("startup")
def startup() -> None:
    conn = _db_connect()
    app.state.db = conn


@app.on_event("shutdown")
def shutdown() -> None:
    conn = getattr(app.state, "db", None)
    try:
        if conn is not None:
            conn.close()
    finally:
        pass


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    start = time.perf_counter()
    status_code: Optional[int] = None
    try:
        response: Response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        latency_ms = (time.perf_counter() - start) * 1000.0
        log_json(
            "request",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query=request.url.query,
            status_code=status_code,
            latency_ms=round(latency_ms, 3),
            client=request.client.host if request.client else None,
        )


def get_model():
    global _model
    if _model is None:
        _model = mlflow.sklearn.load_model(MODEL_URI)
    return _model


@app.post("/api/v1/predict")
def predict(features: PatientFeatures):
    model = get_model()
    started = time.perf_counter()
    input_payload = _features_to_dict(features)
    data = np.array(
        [
            [
                features.age,
                features.sex,
                features.bmi,
                features.bp,
                features.s1,
                features.s2,
                features.s3,
                features.s4,
                features.s5,
                features.s6,
            ]
        ]
    )
    prediction = float(model.predict(data)[0])
    latency_ms = (time.perf_counter() - started) * 1000.0

    output_payload = {"predict": prediction}

    conn = getattr(app.state, "db", None)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO inference_logs (model_uri, model_version, latency_ms, input, output)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (MODEL_URI, MODEL_VERSION, float(latency_ms), Json(input_payload), Json(output_payload)),
            )
        conn.commit()

    log_json(
        "inference",
        model_uri=MODEL_URI,
        model_version=MODEL_VERSION,
        latency_ms=round(latency_ms, 3),
        input=input_payload,
        output=output_payload,
    )
    return output_payload

