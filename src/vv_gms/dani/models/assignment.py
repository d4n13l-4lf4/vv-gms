from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Assignment:
    course_id: str
    assignment_name: str
    weight: Decimal

    def __hash__(self):
        return hash(self.assignment_name)

    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return NotImplemented
        return self.assignment_name == other.assignment_name
