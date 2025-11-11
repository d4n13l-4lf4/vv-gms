from decimal import Decimal
from functools import reduce
from typing import List, Iterator, Dict, Any

from pydash.objects import set_, get

from vv_gms.dani.models.assignment import Assignment
from vv_gms.dani.models.grade import Grade
from vv_gms.dani.models.statistic import Statistic
from vv_gms.dani.models.student import Student
from vv_gms.dani.models.student_grade import StudentGrade


def calculate_statistics(data: List[Decimal]) -> Statistic:
    max_value = max(data)
    min_value = min(data)
    average = sum(data) / len(data)
    return Statistic(max_value, min_value, average, len(data))


def calculate_student_grade(students: List[Dict[str, Any]], assignments: List[Dict[str, Any]], grades: List[Dict[str, Any]]) -> List[StudentGrade]:
    grades = reduce(lambda acc, grade: set_(acc, f"{grade['student_id']}", acc.get(grade['student_id'], []) + [grade]), grades, {})
    assignments = reduce(lambda acc, asg: set_(acc, f"{asg['assignment_name']}", asg), assignments, {})
    final_grades = []
    for student in students:
        student_grades = grades.get(student['student_id'])
        final_grade = reduce(lambda acc, grade: acc + ((grade['grade'] * assignments.get(grade['assignment_name'])['weight']) / 100), student_grades, 0)
        student_grade = StudentGrade(student['student_id'], student['student_name'], final_grade)
        final_grades.append(student_grade)
    return final_grades