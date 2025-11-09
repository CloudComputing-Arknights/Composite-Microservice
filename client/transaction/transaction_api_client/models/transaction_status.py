from enum import Enum


class TransactionStatus(str, Enum):
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    COMPLETED = "completed"
    PENDING = "pending"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
