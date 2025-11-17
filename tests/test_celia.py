from unittest.mock import patch

import pytest
from click.testing import CliRunner
from hamcrest import assert_that, equal_to

from tests.util import find_command_option, get_input, prepare_input
from vv_gms.constant import CMD_EXIT, CMD_ADD_STUDENT
from vv_gms.main import shell, commands


ids = [
    'TC_ADD_STUDENT_01',
    'TC_ADD_STUDENT_02',
    'TC_ADD_STUDENT_03',
    'TC_ADD_STUDENT_04',
]


class TestCelia:

    @pytest.mark.parametrize("input_data,expected_output", [
        (['file:TC_ADD_STUDENT_01.csv'], 'List of students added to the system.'),
        (['file:TC_ADD_STUDENT_02.txt'], 'List of students added to the system.'),
        (['file:TC_ADD_STUDENT_03.csv'], 'Error: invalid student file format.'),
        (['file:TC_ADD_STUDENT_04.txt'], 'List of students added to the system.'),
    ], ids=ids)
    @patch('vv_gms.main.load_data')
    def test_add_student(self, load_data, input_data, expected_output, get_filename):
        cmd_option = find_command_option(commands, CMD_ADD_STUDENT)
        exit_option = find_command_option(commands, CMD_EXIT)
        load_data.return_value = {'courses': {}, 'assignments': {}, 'grades': {}, 'students': {}, 'course_teacher': {}, 'teachers': {}}
        prepared_input = prepare_input(input_data, get_filename)
        prepared_input = get_input([cmd_option] + prepared_input + [exit_option])

        runner = CliRunner()
        result = runner.invoke(shell, input=prepared_input)
        out_lines = list(filter(lambda out: out == expected_output, result.output.splitlines()))
        assert_that(len(out_lines), equal_to(1))
        assert_that(result.exit_code, equal_to(0))