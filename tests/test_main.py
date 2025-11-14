import pytest


command_ids = [
    'TC_ADD_COURSE',
    'TC_REPORT',
    'TC_ADD_STUDENT'
]


class TestMain:

    @pytest.mark.parametrize("test_case_file", [
        'TC_ADD_COURSES.csv',
        'TC_REPORT.csv',
        'TC_ADD_STUDENT.csv'
    ], ids=command_ids)
    def test_commands(self, runner, subtests, test_case_file, get_filename):
        test_case = get_filename(test_case_file, 'cases')
        runner(subtests, test_case)