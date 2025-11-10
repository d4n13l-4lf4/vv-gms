import click

from click import prompt, echo
from typing import  Dict

from vv_gms.constant import CMD_ADD_COURSES
from vv_gms.dani.bootstrap import bootstrap

commands = {
    '1': CMD_ADD_COURSES,
    '2': 'Remove courses',
    '3': 'Add assignment',
    '4': 'Calculate statistics',
    '5': 'Generate report',
    '6': 'Exit'
}

def load_data():
    return {
        'courses': {
            'CS0001': 'Computing'
        },
        'assignments': {}
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
            echo("Calc Stats")
        elif value == "5":
            echo("Generate Report")
        elif value == "6":
            echo("Exit")
            break
        else:
            echo(f"Invalid option. Please choose one of {', '.join(commands.keys())}")

if __name__ == '__main__':
    shell()