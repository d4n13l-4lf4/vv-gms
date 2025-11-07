import pytest
from typer.testing import CliRunner, Typer

from vv_gms.controllers.course_controller import CourseController
from vv_gms.models.course import Course
from vv_gms.repositories.course_repo import CourseRepo
from vv_gms.services.course_service import CourseService
from hamcrest import assert_that, equal_to

from vv_gms.utils.converters.base import GenericConverter
from vv_gms.utils.parsers.generic_parser import GenericParser


ids = [
    "TC_ADD_COURSES_01",

]

class TestCourseController:
    @pytest.mark.parametrize("input_file,expected_output", [
        ("TC_ADD_COURSES_01.csv", "List of courses added to the system.")
    ], ids=ids)
    def test_add_courses(self, input_file, expected_output, data_resolver, db):
        # embed this into a fixture for the whole app
        course_repo = CourseRepo(db)
        course_converter = GenericConverter(Course)
        course_parser = GenericParser(course_converter)
        course_service = CourseService(course_parser, course_repo)
        controller = CourseController(course_service)
        app = Typer()
        app = controller.register(app)

        runner = CliRunner()
        test_filename = data_resolver(["resources", "data"], input_file)
        result = runner.invoke(app, [test_filename])
        assert_that(result.output, equal_to(f"{expected_output}\n"))
        assert_that(result.exit_code, equal_to(0))