from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Grade:
    course_id: str
    student_id: str
    assignment_name: str
    grade: Decimal