from vv_gms.dani.commands.assignment import AssignmentController
from vv_gms.dani.commands.course import CourseController


class Facade:
    def __init__(self, course_controller: CourseController, assignment_controller: AssignmentController):
        self.__course_controller_ = course_controller
        self.__assignment_controller_ = assignment_controller

    def add_courses(self):
        return self.__course_controller_.add_courses()

    def remove_course(self):
        return self.__course_controller_.remove_course()

    def add_assignment(self):
        return self.__assignment_controller_.add_assignment()