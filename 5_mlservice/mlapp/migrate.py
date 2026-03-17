import os
import time

import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mlservice:mlservice@db:5432/mlservice")


DDL = """
CREATE TABLE IF NOT EXISTS inference_logs (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    model_uri TEXT NOT NULL,
    model_version TEXT NULL,
    latency_ms DOUBLE PRECISION NOT NULL,
    input JSONB NOT NULL,
    output JSONB NOT NULL
);
"""


def main() -> None:
    attempts = int(os.getenv("MIGRATE_ATTEMPTS", "30"))
    delay_s = float(os.getenv("MIGRATE_DELAY_S", "1"))

    last_err: Exception | None = None
    for _ in range(attempts):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            try:
                with conn.cursor() as cur:
                    cur.execute(DDL)
                conn.commit()
            finally:
                conn.close()
            print("migration: ok")
            return
        except Exception as e:
            last_err = e
            time.sleep(delay_s)

    raise SystemExit(f"migration: failed after {attempts} attempts: {last_err}")


if __name__ == "__main__":
    main()

