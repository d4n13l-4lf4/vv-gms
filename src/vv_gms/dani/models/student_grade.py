from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class StudentGrade:
    student_id: str
    student_name: str
    grade: Decimal