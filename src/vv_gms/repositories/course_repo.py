from dataclasses import asdict
from typing import List, Iterator

from tinydb import Query

from vv_gms.models.course import Course
from vv_gms.repositories.base import ICourseRepository


class CourseRepo(ICourseRepository):
    def __init__(self, table):
        self.__table_ = table

    def save_courses(self, courses: Iterator[Course]):
        courses_as_dict = (asdict(course) for course in courses)
        self.__table_.insert_multiple(courses_as_dict)

    def get_course(self, course_id: str) -> Course:
        courses = Query()
        return self.__table_.get(courses.course_id == course_id)
