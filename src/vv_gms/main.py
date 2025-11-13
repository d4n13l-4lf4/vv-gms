import click

from click import prompt, echo
from typing import  Dict

from vv_gms.constant import CMD_ADD_COURSES, CMD_EXIT, CMD_GENERATE_REPORT, CMD_CALCULATE_STATISTICS, \
    CMD_ADD_ASSIGNMENT, CMD_REMOVE_COURSES
from vv_gms.dani.bootstrap import bootstrap

commands = {
    '1': CMD_ADD_COURSES,
    '2': CMD_REMOVE_COURSES,
    '3': CMD_ADD_ASSIGNMENT,
    '4': CMD_CALCULATE_STATISTICS,
    '5': CMD_GENERATE_REPORT,
    '6': CMD_EXIT
}

def load_data():
    return {
        "courses": {
            "CS0001": {
                "course_id": "CS0001",
                "course_name": "Computing"
            }
        },
        "assignments": {
            "CS0001": [
                {
                    "course_id": "CS0001",
                    "assignment_name": "Test 01",
                    "weight": 80
                },
                {
                    "course_id": "CS0001",
                    "assignment_name": "Test 02",
                    "weight": 20
                }
            ]
        },
        "grades": {
            "CS0001": [
                {
                    "student_id": "STD_ID_0001",
                    "assignment_name": "Test 01",
                    "grade": 100
                },
                {
                    "student_id": "STD_ID_0001",
                    "assignment_name": "Test 02",
                    "grade": 100
                },
                {
                    "student_id": "STD_ID_0002",
                    "assignment_name": "Test 02",
                    "grade": 100
                }
            ]
        },
        "students": {
            "STD_ID_0001": {
                "student_id": "STD_ID_0001",
                "student_name": "Student Name 01"
            },
            "STD_ID_0002": {
                "student_id": "STD_ID_0002",
                "student_name": "Student Name 02"
            }
        },
        "course_teacher": {
            "CS0001": "TEACH_001"
        },
        "teachers": {
            "TEACH_001": {
                "teacher_id": "TEACH_001",
                "teacher_name": "Teacher Name 01"
            }
        }
    }


def print_menu(cmds: Dict[str, str]):
    echo("Welcome to the grading management system")
    for key, value in cmds.items():
        print(f"{key}. {value}")


@click.command()
def shell():
    data = load_data()

    facade = bootstrap(data)
    # add_courses
    # remove_courses
    # add_assignment
    # calc_stats
    # generate_report
    while True:
        print_menu(commands)
        value = prompt("Enter your choice")

        if value == "1":
            facade.add_courses()
        elif value == "2":
            facade.remove_course()
        elif value == "3": # Need to modify
            facade.add_assignment()
        elif value == "4":
            facade.calc_stats()
        elif value == "5":
            facade.generate_report()
        elif value == "6":
            echo("Exit")
            break
        else:
            echo(f"Invalid option. Please choose one of {', '.join(commands.keys())}")

if __name__ == '__main__':
    shell()