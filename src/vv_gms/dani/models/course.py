from dataclasses import dataclass, field


@dataclass(frozen=True)
class Course():
    course_id: str = field(metadata={'csv': 'CourseID', 'txt': 0})
    course_name: str = field(metadata={'csv': 'CourseName', 'txt': 1})