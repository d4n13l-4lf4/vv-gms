from typing import Dict, Any, List

class GradeRepository:
    def __init__(self, data: Dict[str, Any]):
        self.__data_ = data

    def get_grades_by_course_id_assignment(self, course_id: str, assignment_name: str) -> List[Dict[str, Any]]:
        return list(filter(lambda grade: grade['assignment_name'] == assignment_name, self.__data_.get(course_id, [])))

    def get_grades_by_course_id(self, course_id: str) -> List[Dict[str, Any]]:
        return self.__data_.get(course_id, [])
