import os
from dotenv import load_dotenv

from app.client.messaging.messaging_microservice_client.client import Client as MessagingClient

_messaging_client: MessagingClient | None = None

def init_env():
    load_dotenv()

def get_messaging_client() -> MessagingClient:
    global _messaging_client
    if _messaging_client is None:
        init_env()
        base_url = os.getenv("MESSAGING_SERVICE_URL")
        if not base_url:
            raise RuntimeError("MESSAGING_SERVICE_URL is not set in .env")
        _messaging_client = MessagingClient(base_url=base_url)
    return _messaging_client
