from dataclasses import dataclass

@dataclass(frozen=True)
class Student:
    student_id: str
    student_name: str