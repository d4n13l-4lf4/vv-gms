from typing import Dict

import click
from click import prompt, echo

from vv_gms.functions_celia import add_student, remove_student, add_grade, edit_grade
from vv_gms.constant import CMD_ADD_COURSES, CMD_EXIT, CMD_GENERATE_REPORT, CMD_CALCULATE_STATISTICS, \
    CMD_ADD_ASSIGNMENT, CMD_REMOVE_COURSES, CMD_ADD_STUDENT, WELCOME_MESSAGE, CMD_REMOVE_STUDENT, CMD_ADD_GRADE, \
    CMD_EDIT_GRADE, CMD_ADD_TEACHER, CMD_ASSIGN_TEACHER, CMD_REMOVE_TEACHER
from vv_gms.dani.factory import CommandFactory
from vv_gms.functions_edu import add_teacher, assign_teacher, remove_teacher
from vv_gms.shared import data_file

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
    '10': CMD_EXIT,
    '11': CMD_ADD_TEACHER,
    '12': CMD_ASSIGN_TEACHER,
    '13': CMD_REMOVE_TEACHER
}

def print_menu(cmds: Dict[str, str]):
    echo(WELCOME_MESSAGE)
    for key, value in cmds.items():
        print(f"{key}. {value}")


@click.command()
def shell():
    print(f"DATA FILE LOCATED AT: {data_file}\n")
    facade = CommandFactory()
    while True:
        print_menu(commands)
        value = prompt("Enter your choice")
        if value == "1":
            facade.add_courses()
        elif value == "2":
            facade.remove_course()
        elif value == "3": # Need to modify
            filename = prompt("Enter student file name")
            add_student(filename)
        elif value == "4":
            student_id = prompt("Enter student ID")
            course_id = prompt("Enter course ID")
            remove_student(student_id, course_id)
        elif value == "5":
            facade.add_assignment()
        elif value == "6":
            course_id = prompt("Enter course ID")
            assigment_name = prompt("Enter assigment name")
            grade = prompt("Enter grade: ")
            add_grade(course_id, assigment_name, grade)
        elif value == "7":
            course_id = prompt("Enter course ID")
            student_id = prompt("Enter student ID")
            assignment_name = prompt("Enter assignment name")
            new_grade = prompt("Enter new grade")
            edit_grade(course_id,student_id,assignment_name,new_grade)
        elif value == "8":
            facade.calc_stats()
        elif value == "9":
            facade.generate_report()
        elif value == "10":
            echo("Exit")
            break
        elif value == "11":
            filename = prompt("Enter teacher file name")
            add_teacher(filename)
        elif value == "12":
            course_id = prompt("Enter course ID")
            teacher_id = prompt("Enter teacher file name")
            assign_teacher(course_id,teacher_id)
        elif value == "13":
            course_id = prompt("Enter course ID")
            teacher_id = prompt("Enter teacher file name")
            remove_teacher(course_id,teacher_id)
        else:
            echo(f"Invalid option. Please choose one of {', '.join(commands.keys())}")

if __name__ == '__main__':
    shell()