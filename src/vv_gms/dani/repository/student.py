from typing import List, Dict, Any

class StudentRepository:
    def __init__(self, data):
        self.__data_ = data

    def get_student_by_id(self, student_id) -> Dict[str, Any] | None:
        return self.__data_.get(student_id)

    def get_students_by_id(self, *student_ids) -> List[Dict] | None:
        return [self.get_student_by_id(sid) for sid in student_ids]