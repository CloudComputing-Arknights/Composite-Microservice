from enum import Enum


class UpdateStatusRequestStatus(str, Enum):
    CANCELED = "canceled"
    COMPLETED = "completed"

    def __str__(self) -> str:
        return str(self.value)
