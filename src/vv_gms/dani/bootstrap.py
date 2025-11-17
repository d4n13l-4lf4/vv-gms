from vv_gms.dani.commands.assignment import AssignmentService, AssignmentController
from vv_gms.dani.commands.course import CourseService, CourseController
from vv_gms.dani.commands.facade import Facade
from vv_gms.dani.commands.report import ReportController, ReportService
from vv_gms.dani.commands.statistics import StatisticsController, StatisticsService
from vv_gms.dani.models.course import Course
from vv_gms.dani.repository.assignment import AssignmentRepo
from vv_gms.dani.repository.course import CourseRepository
from vv_gms.dani.repository.grade import GradeRepository
from vv_gms.dani.repository.student import StudentRepository
from vv_gms.dani.repository.teacher import TeacherRepository
from vv_gms.dani.repository.teacher_course import TeacherCourseRepository
from vv_gms.dani.utils.mappers.dict import DictMapper
from vv_gms.dani.utils.parsers.csv_parser import CSVParser
from vv_gms.dani.utils.parsers.facade import FacadeParser
from vv_gms.dani.utils.parsers.txt_parser import TXTParser


def bootstrap(data) -> Facade:
    course_mapper = DictMapper(Course)
    txt_parser = TXTParser(course_mapper)
    csv_parser = CSVParser(course_mapper)
    facade_parser = FacadeParser(txt_parser, csv_parser)
    course_repo = CourseRepository(data['courses'])
    assignment_repo = AssignmentRepo(data['assignments'])
    grade_repo = GradeRepository(data['grades'])

    course_service = CourseService(facade_parser, course_repo, assignment_repo, grade_repo)
    course_controller = CourseController(course_service)

    assignment_service = AssignmentService(assignment_repo, course_repo)
    assignment_controller = AssignmentController(assignment_service)

    statistics_service = StatisticsService(course_repo, assignment_repo, grade_repo)
    statistics_controller = StatisticsController(statistics_service)

    student_repo = StudentRepository(data['students'])

    teacher_repo = TeacherRepository(data['teachers'])
    teacher_course_repo = TeacherCourseRepository(data['course_teacher'], teacher_repo)

    report_service = ReportService(assignment_repo, course_repo, grade_repo, teacher_course_repo, student_repo)
    report_controller = ReportController(report_service)

    return Facade(
        course_controller,
        assignment_controller,
        statistics_controller,
        report_controller
    )