import typer

from vv_gms.controllers.course_controller import CourseController
from vv_gms.repositories.course_repo import CourseRepo
from vv_gms.services.course_service import CourseService

app = typer.Typer(help="Grading Management System CLI")

# Course commands initialization
course_app = typer.Typer(help="Course management commands")
course_repository = CourseRepo()
course_service = CourseService()
course_controller = CourseController(course_service)
course_app = course_controller.register(course_app)

# Grade commands initialization
# ...

# Etc
#...

app.add_typer(course_app, name="") # name is empty to keep cmds at root

if __name__ == "__main__":
    app()