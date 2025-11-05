
from typer.testing import CliRunner, Typer

from vv_gms.controllers.course_controller import CourseController
from vv_gms.services.course_service import CourseService
from hamcrest import assert_that, equal_to


class TestCourseController:
    def test_add_courses(self):
        course_service = CourseService()
        controller = CourseController(course_service)
        app = Typer()
        app = controller.register(app)

        runner = CliRunner()
        result = runner.invoke(app, ["filename.txt"])
        assert_that(result.output, equal_to(f"Added courses from filename.txt\n"))
        assert_that(result.exit_code, equal_to(0))