from vv_gms.dani.commands.assignment import AssignmentController
from vv_gms.dani.commands.course import CourseController
from vv_gms.dani.commands.report import ReportController
from vv_gms.dani.commands.statistics import StatisticsController


class Facade:
    def __init__(self,
                 course_controller: CourseController,
                 assignment_controller: AssignmentController,
                 statistics_controller: StatisticsController,
                 report_controller: ReportController):
        self.__course_controller_ = course_controller
        self.__assignment_controller_ = assignment_controller
        self.__statistics_controller_ = statistics_controller
        self.__report_controller_ = report_controller

    def add_courses(self):
        return self.__course_controller_.add_courses()

    def remove_course(self):
        return self.__course_controller_.remove_course()

    def add_assignment(self):
        return self.__assignment_controller_.add_assignment()

    def calc_stats(self):
        return self.__statistics_controller_.calc_stats()

    def generate_report(self):
        return self.__report_controller_.generate_report()