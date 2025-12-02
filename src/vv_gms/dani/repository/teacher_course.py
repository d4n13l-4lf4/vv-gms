from typing import Dict, Any, List

from pydash import get

from vv_gms.dani.repository.teacher import TeacherRepository


class TeacherCourseRepository:
    def __init__(self, data, teacher_repo: TeacherRepository):
        self.__data_ = data
        self.__teacher_repo_ = teacher_repo

    def get_teacher_by_course_id(self, course_id) -> Dict[str, Any] | None:
        teachers = self.__data_.get(course_id, [])
        return self.__teacher_repo_.get_teacher_by_id(get(teachers, 0, '-1'))
