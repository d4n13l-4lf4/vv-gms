from unittest.mock import patch

import pytest
from click.testing import CliRunner
from hamcrest import assert_that, equal_to

from tests.util import find_command_option, get_input, prepare_input
from vv_gms.constant import CMD_EXIT, CMD_ADD_STUDENT, CMD_EDIT_GRADE, CMD_REMOVE_STUDENT, CMD_ADD_GRADE
from vv_gms.main import shell, commands


ids = [
    'TC_ADD_STUDENT_01',
    'TC_ADD_STUDENT_02',
    'TC_ADD_STUDENT_03',
    'TC_ADD_STUDENT_04',
    'TC_REMOVE_STUDENT_01',
    'TC_REMOVE_STUDENT_02',
    'TC_REMOVE_STUDENT_03',
    'TC_REMOVE_STUDENT_04',
    'TC_REMOVE_STUDENT_05',
    'TC_REMOVE_STUDENT_06',
    'TC_ADD_GRADE_01',
    'TC_ADD_GRADE_02',
    'TC_ADD_GRADE_03',
    'TC_ADD_GRADE_04',
    'TC_ADD_GRADE_05',
    "TC_EDIT_GRADE_01",
    "TC_EDIT_GRADE_02",
    "TC_EDIT_GRADE_03",
    "TC_EDIT_GRADE_04",
    "TC_EDIT_GRADE_05",
]


class TestCelia:

    @pytest.mark.parametrize(
        "input_data,expected_output",
        [
            (['file:TC_ADD_STUDENT_01.csv'], 'List of students added to the system.'),
            (['file:TC_ADD_STUDENT_02.txt'], 'List of students added to the system.'),
            (['file:TC_ADD_STUDENT_03.csv'], 'Error: invalid student file format.'),
            (['file:TC_ADD_STUDENT_04.txt'], 'List of students added to the system.'),
            (['file:TC_REMOVE_STUDENT_01.csv'], 'Error: invalid student file format.'),
            (['file:TC_REMOVE_STUDENT_02.csv'], 'Error: invalid student file format.'),
            (['file:TC_REMOVE_STUDENT_03.csv'], 'Error: invalid student file format.'),
            (['file:TC_REMOVE_STUDENT_04.csv'], 'Error: invalid student file format.'),
            (['file:TC_REMOVE_STUDENT_05.csv'], 'Error: invalid student file format.'),
            (['file:TC_REMOVE_STUDENT_06.csv'], 'Error: invalid student file format.'),
            (['file:TC_ADD_GRADE_01.csv'], 'Error: invalid student file format.'),
            (['file:TC_ADD_GRADE_02.csv'], 'Error: invalid student file format.'),
            (['file:TC_ADD_GRADE_03.csv'], 'Error: invalid student file format.'),
            (['file:TC_ADD_GRADE_04.csv'], 'Error: invalid student file format.'),
            (['file:TC_ADD_GRADE_05.csv'], 'Error: invalid student file format.'),
            (['file:TC_EDIT_GRADE_01.csv'], 'List of grades added to the system.'),
            (['file:TC_EDIT_GRADE_02.csv'], 'Error: invalid student file format.'),
            (['file:TC_EDIT_GRADE_03.csv'], 'New grade must be a number.'),
            (['file:TC_EDIT_GRADE_04.csv'], 'Error: invalid student file format.'),
            (['file:TC_EDIT_GRADE_05.csv'], "No grade found for student 123 in course CS101 for assignment 'HW2'."),
        ],
        ids=ids
    )
    @patch('vv_gms.main.load_data')
    def test_student_operations(self, load_data, input_data, expected_output, get_filename):
        load_data.return_value = {
            "courses": {
                "CS101": {"course_name": "Introduction to Computer Science"},
                "CS202": {"course_name": "Data Structures"},
                "CS310": {"course_name": "Software Engineering Project"},
                "CS500": {"course_name": "Advanced Topics in Computing"},
            },
            "assignments": {
                "A1": {"course_id": "CS101", "title": "Lab 1"},
                "A2": {"course_id": "CS101", "title": "Lab 2"},
                "B1": {"course_id": "CS202", "title": "Project Part 1"},
                "B2": {"course_id": "CS202", "title": "Project Part 2"},
            },
            "grades": {
                # Cambiar a estructura por curso con listas
                "CS101": [
                    {"student_id": "10001", "assignment_name": "A1", "grade": 8.5}
                ],
                "CS202": [
                    {"student_id": "20001", "assignment_name": "B1", "grade": 7.0},
                    {"student_id": "20001", "assignment_name": "B2", "grade": 6.5},
                ]
            },
            "students": {
                "10001": {"student_name": "Alice Johnson"},
                "10002": {"student_name": "Bob Smith"},
                "20001": {"student_name": "Charlie Brown"},
                "30001": {"student_name": "Dana White"},
            },
            "course_teacher": {},
            "teachers": {},
        }

        cmd_option = find_command_option(commands, CMD_ADD_STUDENT)
        exit_option = find_command_option(commands, CMD_EXIT)

        prepared_input = prepare_input(input_data, get_filename)
        prepared_input = get_input([cmd_option] + prepared_input + [exit_option])

        runner = CliRunner()
        result = runner.invoke(shell, input=prepared_input)

        out_lines = [
            out for out in result.output.splitlines()
            if out.strip() == expected_output
        ]

        assert_that(len(out_lines), equal_to(1))
        assert_that(result.exit_code, equal_to(0))