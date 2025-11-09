from enum import Enum


class CategoryType(str, Enum):
    FURNITURE = "FURNITURE"

    def __str__(self) -> str:
        return str(self.value)
