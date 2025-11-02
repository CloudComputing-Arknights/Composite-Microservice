from __future__ import annotations

import os

from fastapi import FastAPI

port = int(os.environ.get("FASTAPIPORT", 8000))


# -----------------------------------------------------------------------------
# FastAPI App Definition
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Composite API",
    description="An API to orchestrate calls to other microservices.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# Root Endpoint
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Composite API. See /docs for details."}


# -----------------------------------------------------------------------------
# Composite Endpoints
# -----------------------------------------------------------------------------
USER_SERVICE_URL = "https://users-api-121084561869.us-central1.run.app"
ITEM_SERVICE_URL = "https://microservice-item-713181822049.us-central1.run.app"
TRANSACTION_SERVICE_URL = "http://34.172.7.104:8000"

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
