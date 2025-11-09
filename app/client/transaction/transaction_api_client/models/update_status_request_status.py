from enum import Enum


class UpdateStatusRequestStatus(str, Enum):
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    COMPLETED = "completed"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
