import typer
from platformdirs import PlatformDirs

from vv_gms.controllers.course_controller import CourseController
from vv_gms.models.course import Course
from vv_gms.repositories.course_repo import CourseRepo
from vv_gms.repositories.db import create_db
from vv_gms.services.course_service import CourseService
from vv_gms.utils.converters.base import GenericConverter
from vv_gms.utils.parsers.generic_parser import GenericParser
from vv_gms.utils.platform.path import PlatformPath

app = typer.Typer(help="Grading Management System CLI")

# Global dependencies
filename = "db.json"
dirs = PlatformDirs("gmscli", "DCE", "1.0")
path = PlatformPath(dirs)
db = create_db(path.get_user_data_filename(filename))

# Course commands initialization
course_app = typer.Typer(help="Course management commands")
course_repository = CourseRepo(db.table('courses'))
courses_converter = GenericConverter(Course)
file_parser = GenericParser(courses_converter)
course_service = CourseService(file_parser, course_repository)
course_controller = CourseController(course_service)
course_app = course_controller.register(course_app)

# Grade commands initialization
# ...

# Etc
#...

app.add_typer(course_app, name="") # name is empty to keep cmds at root

if __name__ == "__main__":
    app()