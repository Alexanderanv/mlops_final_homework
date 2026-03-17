import uvicorn
import os

from .server import app

def main() -> None:
    host = os.getenv("SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("SERVICE_PORT", "8000"))
    uvicorn.run(app, host=host, port=port, access_log=False)

if __name__ == "__main__":
    main()

