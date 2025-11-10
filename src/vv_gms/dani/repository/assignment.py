from typing import Iterator, Dict

from vv_gms.dani.models.assignment import Assignment


class AssignmentRepo:
    def __init__(self, data: Dict[str, Iterator[Assignment]]) -> None:
        self.__data_ = data

    def get_assignments_by_course_id(self, course_id) -> Iterator[Assignment]:
        return self.__data_[course_id]

    def get_assignment_by_course_id_and_name(self, course_id: str, assignment_name: str) -> Assignment | None:
        assignments = self.get_assignments_by_course_id(course_id)
        assignment = list(filter(lambda asg: asg.assignment_name == assignment_name, assignments))
        return None if len(assignment) == 0 else assignment[0]