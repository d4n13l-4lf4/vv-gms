from typing import List

from vv_gms.models.course import Course
from vv_gms.repositories.base import ICourseRepository


class CourseRepo(ICourseRepository):
    def save_courses(self, courses: List[Course]):
        pass
