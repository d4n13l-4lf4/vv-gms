from dataclasses import dataclass, field


@dataclass
class Course:
    course_id: str = field(metadata={'plain': 'CourseID'})
    course_name: str = field(metadata={'plain': 'CourseName'})