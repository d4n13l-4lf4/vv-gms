from typing import Iterator, Any, Generator

from click import prompt, echo

from vv_gms.dani.exception.custom import CustomException
from vv_gms.dani.exception.decorator import catch_error
from vv_gms.dani.models.course import Course
from vv_gms.dani.repository.assignment import AssignmentRepo
from vv_gms.dani.repository.course import CourseRepository
from vv_gms.dani.utils.parsers.base import FileParser


class CourseService:
    def __init__(self,
                 file_parser: FileParser[Course],
                 course_repo: CourseRepository,
                 assignment_repo: AssignmentRepo
                 ):
        self.__course_repo_ = course_repo
        self.__file_parser_ = file_parser
        self.__assignment_repo_ = assignment_repo

    def add_courses(self, filename: str):
        courses = self.__file_parser_.parse(filename)
        valid_courses = self.__check_course_(courses)
        self.__course_repo_.save_course(valid_courses)

    def __check_course_(self, courses: Iterator[Course]) -> Generator[dict[str, str], None, None]:
        for course in courses:
            found = self.__course_repo_.get_course(course.course_id)
            if found is not None:
                raise CustomException(f"{course.course_id} already exists.")
            yield { "course_id": course.course_id, "course_name": course.course_name }

    def remove_course(self, course_id: str):
        course = self.__course_repo_.get_course(course_id)
        if course is None:
            raise CustomException('CourseID not found.')
        assignments = self.__assignment_repo_.get_assignments_by_course_id(course_id)
        if assignments is not None:
            raise CustomException('Cannot delete course with active assignments or grades.')
        self.__course_repo_.remove_course(course_id)


class CourseController:
    def __init__(self, course_service: CourseService):
        self.__course_service_ = course_service

    @catch_error(echo)
    def add_courses(self):
        filename = prompt('Enter filename')
        self.__course_service_.add_courses(filename)
        echo('List of courses added to the system.\n')

    @catch_error(echo)
    def remove_course(self):
        course_id = prompt('Enter course id')
        self.__course_service_.remove_course(course_id)
        echo(f"Course {course_id} removed.\n")