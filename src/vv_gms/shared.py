import json
import os

from platformdirs import user_data_dir
from pathlib import Path

data_file = str(Path(user_data_dir("gms_cli", "cde", "v1")) / "data.json")

# General functions
def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "courses": {},
        "assignments": {},
        "teachers": {},
        "students": {},
        "course_teacher": {},
        "grades": {}
    }


def save_data(data):
    Path(data_file).parent.mkdir(parents=True, exist_ok=True)
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)