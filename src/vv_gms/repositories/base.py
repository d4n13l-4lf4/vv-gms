from abc import ABC, abstractmethod
from typing import Iterator

from vv_gms.models.course import Course


class ICourseRepository(ABC):
    @abstractmethod
    def save_courses(self, courses: Iterator[Course]):
        pass

    @abstractmethod
    def get_course(self, course_id: str) -> Course:
        pass