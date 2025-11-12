import os

from dotenv import load_dotenv

from app.client.item.item_thread_api_client.client import Client as ItemClient
from app.client.transaction.transaction_api_client.client import Client as TransactionClient
from app.client.user.user_address_api_client.client import Client as UserClient

_user_client: UserClient | None = None
_item_client: ItemClient | None = None
_transaction_client: TransactionClient | None = None


def init_env():
    load_dotenv()

    global _user_client, _item_client, _transaction_client

    _user_client = UserClient(base_url=os.environ.get("USER_SERVICE_URL"))
    _item_client = ItemClient(base_url=os.environ.get("ITEM_SERVICE_URL"))
    _transaction_client = TransactionClient(base_url=os.environ.get("TRANSACTION_SERVICE_URL"))


def get_user_client() -> UserClient:
    if _user_client is None:
        init_env()
    return _user_client


def get_item_client() -> ItemClient:
    if _item_client is None:
        init_env()
    return _item_client


def get_transaction_client() -> TransactionClient:
    if _transaction_client is None:
        init_env()
    return _transaction_client
