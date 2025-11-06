from vv_gms.models.course import Course
from vv_gms.repositories.base import ICourseRepository
from vv_gms.services.base import ICourseService
from vv_gms.utils.parsers.generic_parser import GenericParser


class CourseService(ICourseService):
    def __init__(self, file_parser: GenericParser[Course], courses_repo: ICourseRepository):
        self.__parser_ = file_parser
        self.__courses_repo_ = courses_repo

    def add_courses(self, filename: str):
        courses = self.__parser_.parse(filename)
        self.__courses_repo_.save_courses(courses)