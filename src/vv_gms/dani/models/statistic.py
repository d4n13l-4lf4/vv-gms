from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Statistic:
    best: Decimal
    lowest: Decimal
    average: Decimal
    submission_count: int