from dataclasses import dataclass
from typing import List, Dict, Any

from vv_gms.dani.models.statistic import Statistic
from vv_gms.dani.models.student_grade import StudentGrade


@dataclass(frozen=True)
class Report:
    course: Dict[str, Any]
    teacher: Dict[str, Any]
    stats: Statistic
    grades: List[StudentGrade]