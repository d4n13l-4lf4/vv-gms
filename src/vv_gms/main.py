import click

from click import prompt, echo
from typing import  Dict

from vv_gms.constant import CMD_ADD_COURSES, CMD_EXIT, CMD_GENERATE_REPORT, CMD_CALCULATE_STATISTICS, \
    CMD_ADD_ASSIGNMENT, CMD_REMOVE_COURSES, CMD_REMOVE_STUDENT, CMD_ADD_GRADE, CMD_EDIT_GRADE
from vv_gms.dani.bootstrap import bootstrap
from vv_gms.functions_celia import add_student, remove_student, add_grade, edit_grade

from src.vv_gms.constant import CMD_ADD_STUDENT

commands = {
    '1': CMD_ADD_COURSES,
    '2': CMD_REMOVE_COURSES,
    '3': CMD_ADD_STUDENT,
    '4': CMD_REMOVE_STUDENT,
    '5': CMD_ADD_ASSIGNMENT,
    '6': CMD_ADD_GRADE,
    '7': CMD_EDIT_GRADE,
    '8': CMD_CALCULATE_STATISTICS,
    '9': CMD_GENERATE_REPORT,
    '10': CMD_EXIT
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
            filename = prompt("Enter student file name: ")
            add_student(filename)
        elif value == "4":
            student_id = prompt("Enter student ID: ")
            course_id = prompt("Enter course ID: ")
            remove_student(student_id, course_id)
        elif value == "5":
            facade.add_assignment()
        elif value == "6":
            course_id = prompt("Enter course ID: ")
            assigment_name = prompt("Enter assigment name: ")
            grade = prompt("Enter grade: ")
            add_grade(course_id, assigment_name, grade)
        elif value == "7":
            course_id = prompt("Enter course ID: ")
            student_id = prompt("Enter student ID: ")
            assignment_name = prompt("Enter assignment name: ")
            new_grade = prompt("Enter new grade: ")
            edit_grade(course_id,student_id,assignment_name,new_grade)
        elif value == "8":
            facade.calc_stats()
        elif value == "9":
            facade.generate_report()
        elif value == "10":
            echo("Exit")
            break
        else:
            echo(f"Invalid option. Please choose one of {', '.join(commands.keys())}")

if __name__ == '__main__':
    shell()