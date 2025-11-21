import decimal
from typing import Dict, List, Any


class AssignmentRepo:
    def __init__(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        self.__data_ = data

    def get_assignments_by_course_id(self, course_id) -> List[Dict[str, Any]]:
        return self.__data_.get(course_id, [])

    def get_assignment_by_course_id_and_name(self, course_id: str, assignment_name: str) -> Dict[str, Any] | None:
        assignments = self.get_assignments_by_course_id(course_id)
        assignment = list(filter(lambda asg: asg['assignment_name'] == assignment_name, assignments))
        return None if len(assignment) == 0 else assignment[0]

    def save_assignment(self, course_id: str, assignment_name: str, weight: decimal.Decimal) -> None:
        assignments = self.__data_.get(course_id, [])
        assignments.append({'course_id': course_id, 'assignment_name': assignment_name, 'weight': weight})
