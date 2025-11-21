from dataclasses import dataclass

@dataclass(frozen=True)
class Teacher:
    teacher_id: str
    teacher_name: str