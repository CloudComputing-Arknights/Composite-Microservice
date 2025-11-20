from enum import Enum


class ConditionType(str, Enum):
    BRAND_NEW = "BRAND_NEW"
    GOOD = "GOOD"
    LIKE_NEW = "LIKE_NEW"
    POOR = "POOR"

    def __str__(self) -> str:
        return str(self.value)
