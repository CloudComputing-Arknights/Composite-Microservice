from enum import Enum


class ListTransactionsTransactionsGetTypeType0(str, Enum):
    PURCHASE = "purchase"
    TRADE = "trade"

    def __str__(self) -> str:
        return str(self.value)
