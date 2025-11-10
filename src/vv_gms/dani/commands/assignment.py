from functools import reduce

from click import prompt, echo

from vv_gms.dani.exception.custom import CustomException
from vv_gms.dani.exception.decorator import catch_error
from vv_gms.dani.repository.assignment import AssignmentRepo
from vv_gms.dani.repository.course import CourseRepository
from vv_gms.dani.validation.parameter import validate
from vv_gms.dani.validation.validator import between, not_empty


class AssignmentService:
    def __init__(self, assignment_repo: AssignmentRepo, course_repo: CourseRepository) -> None:
        self.__assignment_repo_ = assignment_repo
        self.__course_repo_ = course_repo

    @validate({
        'weight': between(0, 100, True, 'Invalid weight value. Must be integer 0-100'),
        'course_id': not_empty('Invalid arguments. Use: add_assignment <CourseID> <AssignmentName> [<Weight>]'),
        'assignment_name': not_empty('Invalid arguments. Use: add_assignment <CourseID> <AssignmentName> [<Weight>]'),
    })
    def add_assignment(self, course_id: str, assignment_name: str, weight: int):
        course = self.__course_repo_.get_course(course_id)
        if course is None:
            raise CustomException('CourseID not found.')
        assignment = self.__assignment_repo_.get_assignment_by_course_id_and_name(course_id, assignment_name)
        if assignment is not None:
            raise CustomException('Assignment already exist in this course.')

        assignments = self.__assignment_repo_.get_assignments_by_course_id(course_id)
        current_weight = reduce(lambda acc, asg: asg.weight + acc,assignments, 0)
        if current_weight + weight > 100:
            raise CustomException("Invalid total assignment weights can't exceed 100.")


class AssignmentController:
    def __init__(self, assignment_service: AssignmentService) -> None:
        self.__assignment_service_ = assignment_service

    @catch_error(echo)
    def add_assignment(self):
        course_id = prompt('Enter course ID')
        assignment_name = prompt('Enter assignment name')
        weight = prompt('Enter weight value')
        self.__assignment_service_.add_assignment(course_id, assignment_name, weight)