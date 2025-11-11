from unittest.mock import patch

import pytest
from click.testing import CliRunner

from tests.util import find_command_option, get_input, prepare_input
from vv_gms.constant import CMD_ADD_COURSES, CMD_EXIT
from vv_gms.main import shell, commands
from hamcrest import assert_that, equal_to, has_length

ids = [
    'TC_ADD_COURSE_01',
    'TC_ADD_COURSE_02',
    'TC_ADD_COURSE_03',
    'TC_ADD_COURSE_04',
    'TC_ADD_COURSE_05',
]

class TestDani:
    @pytest.mark.parametrize("input_data,expected_output", [
        (['file:TC_ADD_COURSE_01.csv'], 'List of courses added to the system.'),
        # Test case failed due to already present memory.
        (['file:TC_ADD_COURSE_02.txt'], 'List of courses added to the system.'),
        (['file:TC_ADD_COURSE_03.csv'], 'Error: CS0001 already exists.'),
        # Test case failed due to message wrong formatted.
        (['file:'], 'Error: Invalid input type file, or arguments. Use: <CourseID> <CourseName>'),
        # Test case failed due to incorrect handling of CSV file.
        (['file:TC_ADD_COURSE_05.csv'], 'Error: Invalid input type file, or arguments. Use: <CourseID> <CourseName>')
    ], ids=ids)
    @patch('vv_gms.main.load_data')
    def test_add_courses(self, load_data, input_data, expected_output, get_filename):
        cmd_option = find_command_option(commands, CMD_ADD_COURSES)
        exit_option = find_command_option(commands, CMD_EXIT)
        load_data.return_value = {'courses': {}, 'assignments': {}, 'grades': {}, 'students': {}, 'course_teacher': {}, 'teachers': {}}
        prepared_input = prepare_input(input_data, get_filename)
        prepared_input = get_input([cmd_option] + prepared_input + [exit_option])

        runner = CliRunner()
        result = runner.invoke(shell, input=prepared_input)
        out_lines = list(filter(lambda out: out == expected_output, result.output.splitlines()))
        assert_that(len(out_lines), equal_to(1))
        assert_that(result.exit_code, equal_to(0))