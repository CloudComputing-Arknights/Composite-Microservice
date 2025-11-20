from enum import Enum


class TransactionType(str, Enum):
    RENT = "RENT"
    SALE = "SALE"

    def __str__(self) -> str:
        return str(self.value)
