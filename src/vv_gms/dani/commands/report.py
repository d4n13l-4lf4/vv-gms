from click import prompt, echo

from vv_gms.dani.exception.custom import CustomException
from vv_gms.dani.models.report import Report
from vv_gms.dani.repository.assignment import AssignmentRepo
from vv_gms.dani.repository.course import CourseRepository
from vv_gms.dani.repository.grade import GradeRepository
from vv_gms.dani.repository.student import StudentRepository
from vv_gms.dani.repository.teacher_course import TeacherCourseRepository
from vv_gms.dani.utils.stats.statistics import calculate_statistics
from vv_gms.dani.utils.stats.statistics import calculate_student_grade
from vv_gms.dani.validation.parameter import validate
from vv_gms.dani.validation.validator import not_empty


class ReportService:
    def __init__(self, assignment_repo: AssignmentRepo, course_repo: CourseRepository, grade_repo: GradeRepository, teacher_course_repo: TeacherCourseRepository, student_repo: StudentRepository):
        self.__assignment_repo_ = assignment_repo
        self.__grade_repo_ = grade_repo
        self.__teacher_course_repo_ = teacher_course_repo
        self.__course_repo_ = course_repo
        self.__student_repo_ = student_repo

    @validate({
        'course_id': not_empty('Invalid arguments. Use: generate_report <CourseID>'),
    })
    def generate_report(self, course_id: str) -> Report:
        grades = self.__grade_repo_.get_grades_by_course_id(course_id)
        if len(grades) == 0:
            raise CustomException('No grades recorded for this course')

        course = self.__course_repo_.get_course(course_id)
        assignments = self.__assignment_repo_.get_assignments_by_course_id(course_id)
        teacher = self.__teacher_course_repo_.get_teacher_by_course_id(course_id)
        students = self.__student_repo_.get_students_by_id(*set(map(lambda grade: grade['student_id'], grades)))

        final_grades = calculate_student_grade(students, assignments, grades)
        stats = calculate_statistics(list(map(lambda grade: grade.grade, final_grades)))
        report = Report(course, teacher, stats, final_grades)

        return report


class ReportController:
    def __init__(self, report_service: ReportService):
        self.__report_service = report_service

    def generate_report(self):
        course_id = prompt('Enter course id')
        report = self.__report_service.generate_report(course_id)
        echo(f"Course: {report.course['course_id']} - {report.course['course_name']}")
        echo(f"Teacher {report.teacher['teacher_name']}")
        echo(f"Average: {report.stats.average}")
        echo(f"Lowest: {report.stats.lowest}")
        echo(f"Highest: {report.stats.best}")
        echo("Student Final Grades:")
        for student in report.grades:
            echo(f"\t{student.student_id} {student.student_name}: {student.grade}")

