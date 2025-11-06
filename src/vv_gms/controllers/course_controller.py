import typer

from vv_gms.services.base import ICourseService

class CourseController:
    def __init__(self, course: ICourseService):
        self.__course_ = course

    def register(self, app):
        app.command(name="add_courses")(self.add_courses)
        return app

    def add_courses(self, filename: str):
        """Import courses from a CSV/TXT file."""
        self.__course_.add_courses(filename)
        typer.echo(f"List of courses added to the system.")