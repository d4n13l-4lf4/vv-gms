import os
from typing import Callable, Counter

import pytest
from click.testing import CliRunner
from hamcrest import assert_that, has_entry, equal_to

from tests.util import read_cases, find_command_option, get_context, prepare_input, get_input
from vv_gms.constant import CMD_EXIT
from vv_gms.main import commands, shell


@pytest.fixture
def get_filename() -> Callable[[str, str], str]:
    def __inner__(file: str, folder: str = 'data'):
        dir_to_search = ['resources', folder]
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, *dir_to_search, file)
        return str(config_path)
    return __inner__

@pytest.fixture
def runner(get_filename):
    def __inner__(subtests, load_data, test_case_file: str):
        test_cases = read_cases(test_case_file)
        for idx, test_case in enumerate(test_cases):
            with subtests.test(msg=test_case['TEST_CASE_ID'], i=idx):
                cmd_option = find_command_option(commands, test_case['CMD'])
                exit_option = find_command_option(commands, CMD_EXIT)
                context_file = get_filename(test_case['CONTEXT'], 'context')
                context = get_context(context_file)
                inputs = test_case['INPUTS'].split('|')
                load_data.return_value = context
                prepared_input = prepare_input(inputs, get_filename)
                prepared_input = get_input([cmd_option] + prepared_input + [exit_option])
                runner = CliRunner()
                result = runner.invoke(shell, input=prepared_input)
                expected_outputs = Counter(test_case['EXPECTED_OUTPUTS'].split('|'))
                out_lines = [line.strip() for line in result.output.splitlines()]
                output_lines = Counter(out_lines)
                common = dict(expected_outputs & output_lines)
                for expected_output in expected_outputs:
                    assert_that(common, has_entry(expected_output, equal_to(1)))
    return __inner__