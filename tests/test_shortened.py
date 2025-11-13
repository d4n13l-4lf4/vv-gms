from unittest.mock import patch

import pytest


command_ids = [
    'TC_ADD_COURSE',
    'TC_REPORT'
]


class TestShortened:

    @pytest.mark.parametrize("test_case_file", [
        'TC_ADD_COURSES.csv',
        'TC_REPORT.csv'
    ], ids=command_ids)
    @patch('vv_gms.main.load_data')
    def test_commands(self, load_data, runner, subtests, test_case_file, get_filename):
        test_case = get_filename(test_case_file, 'cases')
        runner(subtests, load_data, test_case)