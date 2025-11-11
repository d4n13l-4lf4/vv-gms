from click import prompt, echo

from vv_gms.dani.exception.custom import CustomException
from vv_gms.dani.exception.decorator import catch_error
from vv_gms.dani.models.statistic import Statistic
from vv_gms.dani.repository.assignment import AssignmentRepo
from vv_gms.dani.repository.course import CourseRepository
from vv_gms.dani.repository.grade import GradeRepository
from vv_gms.dani.utils.stats.statistics import calculate_statistics


class StatisticsService:
    def __init__(self, course_repo: CourseRepository, assignment_repo: AssignmentRepo, grade_repo: GradeRepository):
        self.__course_repo_ = course_repo
        self.__assignment_repo_ = assignment_repo
        self.__grade_repo_ = grade_repo

    def calc_stats(self, course_id: str, assignment_name: str) -> Statistic:
        course = self.__course_repo_.get_course(course_id)
        if course is None:
            raise CustomException('CourseID or AssignmentName not found.')

        assignment = self.__assignment_repo_.get_assignment_by_course_id_and_name(course_id, assignment_name)
        if assignment is None:
            raise CustomException('CourseID or AssignmentName not found.')

        grades = self.__grade_repo_.get_grades_by_course_id_assignment(course_id, assignment_name)
        if grades is None:
            raise CustomException('No grades recorded for this assignment.')

        grades = list(map(lambda grade: grade['grade'], grades))
        stats = calculate_statistics(grades)

        return stats




class StatisticsController:
    def __init__(self, statistics_service: StatisticsService):
        self.__statistics_service_ = statistics_service

    @catch_error(echo)
    def calc_stats(self):
        course_id = prompt("Enter course id")
        assignment_name = prompt("Enter assignment name")
        stats = self.__statistics_service_.calc_stats(course_id, assignment_name)
        echo(f"Assignment: {assignment_name}")
        echo(f"Average: {stats.average}")
        echo(f"Lowest: {stats.lowest}")
        echo(f"Best: {stats.best}")
        echo(f"SubmissionCount: {stats.submission_count}")

