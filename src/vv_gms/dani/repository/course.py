from typing import Dict, Iterator

class CourseRepository:
    def __init__(self, data: Dict[str, Dict[str, str]]):
        self.__data_ = data

    def get_course(self, course_id: str) -> Dict[str, str] | None:
        return self.__data_.get(course_id)

    def save_course(self, courses: Iterator[Dict[str, str]]) -> None:
        for course in courses:
            self.__data_[course['course_id']] = course

    def remove_course(self, course_id: str) -> None:
        del self.__data_[course_id]