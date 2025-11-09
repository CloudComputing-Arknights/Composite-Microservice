from enum import Enum


class NewTransactionRequestType(str, Enum):
    PURCHASE = "purchase"
    TRADE = "trade"

    def __str__(self) -> str:
        return str(self.value)
