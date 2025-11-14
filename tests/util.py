import csv
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
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
    return os.linesep.join(data) + os.linesep


def read_cases(test_case_file: str) -> List[Dict[str, str]]:
    with open(test_case_file, mode='r', encoding='utf-8') as f:
        test_cases = csv.DictReader(f)
        return list(test_cases)


def get_context(context_file: str) -> Dict[str, str]:
    with open(context_file, mode='r', encoding='utf-8') as f:
        return json.load(f)

def write_lines(file: str, out_lines: List[str], exception):
    filepath = Path(file)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(file, mode='w', encoding='utf-8') as f:
        [f.write(line + os.linesep) for line in out_lines]
        if exception:
            f.write('====== EXCEPTION ======' + os.linesep)
            f.write(f"{exception}")


@contextmanager
def temporary_file(suffix='.json', prefix='tmp'):
    """
    Context manager for a temporary file.

    :param suffix: Optional file suffix
    :param prefix: Optional file prefix
    """
    temp_path = tempfile.mktemp(suffix=suffix, prefix=prefix)
    try:
        yield temp_path  # provide the temporary file to the caller
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)  # ensure the file is closed