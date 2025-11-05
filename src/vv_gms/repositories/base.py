from abc import ABC, abstractmethod
from typing import List

from vv_gms.models.course import Course


class ICourseRepository(ABC):
    @abstractmethod
    def save_courses(self, courses: List[Course]):
        pass