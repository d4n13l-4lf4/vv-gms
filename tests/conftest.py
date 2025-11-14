import os
from typing import Callable, Counter
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from hamcrest import assert_that, has_entry, equal_to

from tests.util import read_cases, find_command_option, prepare_input, get_input, write_lines, temporary_file
from vv_gms.constant import CMD_EXIT
from vv_gms.main import commands, shell
from shutil import copy


def pytest_addoption(parser):
    parser.addoption('--out_file', action='store', help='Output test case results')



@pytest.fixture
def get_filename() -> Callable[[str, str], str]:
    def __inner__(file: str, folder: str = 'data'):
        dir_to_search = ['resources', folder]
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, *dir_to_search, file)
        return str(config_path)
    return __inner__


@pytest.fixture
def runner(get_filename, request):
    def __inner__(subtests, test_case_file: str):
        test_cases = read_cases(test_case_file)
        for idx, test_case in enumerate(test_cases):
            with (subtests.test(msg=test_case['TEST_CASE_ID'], i=idx),
                  temporary_file(prefix=f"test_case_{test_case['TEST_CASE_ID']}_", suffix='.json') as json_file,
                  patch('vv_gms.shared.data_file', new=json_file)):
                cmd_option = find_command_option(commands, test_case['CMD'])
                exit_option = find_command_option(commands, CMD_EXIT)
                context_file = get_filename(test_case['CONTEXT'], 'context')
                inputs = test_case['INPUTS'].split('|')

                if context_file:
                    copy(context_file, json_file)

                prepared_input = prepare_input(inputs, get_filename)
                prepared_input = get_input([cmd_option] + prepared_input + [exit_option])
                runner = CliRunner()
                result = runner.invoke(shell, input=prepared_input)
                expected_outputs = Counter(test_case['EXPECTED_OUTPUTS'].split('|'))
                out_lines = [line.strip().strip(os.linesep) for line in result.output.splitlines()]
                output_lines = Counter(out_lines)

                out_file = request.config.getoption('out_file')
                if out_file:
                    out_filename = get_filename(test_case['TEST_CASE_ID'], 'report') + '.txt'
                    write_lines(out_filename, out_lines, result.exception)

                common = dict(expected_outputs & output_lines)
                for expected_output in expected_outputs:
                    assert_that(common, has_entry(expected_output, equal_to(1)), "output was not found")
    return __inner__