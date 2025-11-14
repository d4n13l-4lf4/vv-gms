from typing import Dict

import click
from click import prompt, echo

from vv_gms.celia import add_student
from vv_gms.constant import CMD_ADD_COURSES, CMD_EXIT, CMD_GENERATE_REPORT, CMD_CALCULATE_STATISTICS, \
    CMD_ADD_ASSIGNMENT, CMD_REMOVE_COURSES, CMD_ADD_STUDENT
from vv_gms.dani.factory import CommandFactory
from vv_gms.shared import data_file

commands = {
    '1': CMD_ADD_COURSES,
    '2': CMD_REMOVE_COURSES,
    '3': CMD_ADD_ASSIGNMENT,
    '4': CMD_CALCULATE_STATISTICS,
    '5': CMD_GENERATE_REPORT,
    '6': CMD_ADD_STUDENT,
    '7': CMD_EXIT
}

def print_menu(cmds: Dict[str, str]):
    echo("Welcome to the grading management system")
    for key, value in cmds.items():
        print(f"{key}. {value}")


@click.command()
def shell():
    print(f"DATA FILE LOCATED AT: {data_file}\n")
    facade = CommandFactory()
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
            filename = prompt("Enter student file name")
            add_student(filename)
        elif value == "7":
            echo("Exit")
            break
        else:
            echo(f"Invalid option. Please choose one of {', '.join(commands.keys())}")

if __name__ == '__main__':
    shell()