import csv
import json
from typing import Dict, List


def find_command_option(cmd: Dict[str, str], name: str) -> Dict[str, str]:
    filtered = list(filter(lambda command: command[1] == name, cmd.items()))
    if len(filtered) > 0:
        return filtered[0][0]
    raise Exception(f"Command {name} not found")


def prepare_input(input_data: List[str], resolver) -> List[str]:
    prepared_input = []
    for arg in input_data:
        if 'file:' in arg:
            new_arg = arg.replace('file:', '')
            prepared_input.append(resolver(new_arg))
        else :
            prepared_input.append(arg)
    return prepared_input


def get_input(data: List[str]) -> str:
    return "\n".join(data) + "\n"


def read_cases(test_case_file: str) -> List[Dict[str, str]]:
    with open(test_case_file, mode='r', encoding='utf-8') as f:
        test_cases = csv.DictReader(f)
        return list(test_cases)


def get_context(context_file: str) -> Dict[str, str]:
    with open(context_file, mode='r', encoding='utf-8') as f:
        return json.load(f)