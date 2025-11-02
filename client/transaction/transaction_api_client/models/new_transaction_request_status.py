from enum import Enum


class NewTransactionRequestStatus(str, Enum):
    CANCELED = "canceled"
    COMPLETED = "completed"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
