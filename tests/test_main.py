import pytest


command_ids = [
    #'TC_ADD_COURSE',
    #'TC_REMOVE_COURSE',
    #'TC_ADD_ASSIGNMENT',
    #'TC_CALC_STATS',
    #'TC_REPORT',
    #'TC_ADD_STUDENT'

    'TC_ADD_TEACHER',
    'TC_ASSIGN_TEACHER',
    'TC_REMOVE_TEACHER',
    'TC_CALC_COURSE_STATS'
]


class TestMain:

    @pytest.mark.parametrize("test_case_file", [
        #'TC_ADD_COURSES.csv',
        #'TC_REMOVE_COURSE.csv',
        #'TC_ADD_ASSIGNMENT.csv',
        #'TC_CALC_STATS.csv',
        #'TC_REPORT.csv',
        #'TC_ADD_STUDENT.csv',

        'TC_ADD_TEACHER.csv',
        'TC_ASSIGN_TEACHER.csv',
        'TC_REMOVE_TEACHER.csv',
        'TC_CALC_COURSE_STATS.csv'

    ], ids=command_ids)
    def test_commands(self, runner, subtests, test_case_file, get_filename):
        test_case = get_filename(test_case_file, 'cases')
        runner(subtests, test_case)