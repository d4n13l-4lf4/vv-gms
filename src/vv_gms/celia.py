import os

from vv_gms.shared import load_data, save_data


# Specific functions
def add_student(filename):
    if not os.path.exists(filename):
        return

    data = load_data()

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return

    header_line = lines[0].strip()
    if filename.endswith(".csv"):
        delimiter = ","
    else:
        if "  " in header_line:
            delimiter = "  "
        elif ";" in header_line:
            delimiter = ";"
        elif "," in header_line:
            delimiter = ","
        else:
            delimiter = ";"

    for line in lines[1:]:
        if not line.strip():
            continue

        line = line.strip()

        if delimiter == "  ":
            row = [col.strip() for col in line.split("  ")]
        else:
            row = [col.strip() for col in line.split(delimiter)]

        if len(row) < 3:
            continue

        student_id = row[0]
        student_name = row[1]
        course_ids = [c.strip() for c in row[2].replace(";", ",").split(",")]

        for course_id in course_ids:
            if not course_id:
                continue

            # Crear el curso si no existe aún
            if course_id not in data["courses"]:
                data["courses"][course_id] = {"students": {}}
            elif "students" not in data["courses"][course_id]:
                data["courses"][course_id]["students"] = {}

            if student_id in data["courses"][course_id]["students"]:
                continue

            data["courses"][course_id]["students"][student_id] = {
                "name": student_name,
                "grades": {}
            }

            if student_id not in data["students"]:
                data["students"][student_id] = {
                    "name": student_name,
                    "courses": []
                }

            if course_id not in data["students"][student_id]["courses"]:
                data["students"][student_id]["courses"].append(course_id)

            print(f"Added student {student_name} ({student_id}) to course {course_id}.")

    save_data(data)


def remove_student(student_id, course_id):
    data = load_data()

    if "courses" not in data or course_id not in data["courses"]:
        return

    course = data["courses"][course_id]

    if "students" not in course:
        return

    if student_id not in course["students"]:
        return

    del course["students"][student_id]

    if "students" in data and student_id in data["students"]:
        student_info = data["students"][student_id]

        if "courses" in student_info and isinstance(student_info["courses"], list):
            student_info["courses"] = [
                c for c in student_info["courses"] if c != course_id
            ]

    save_data(data)

def add_grade(course_id, student_id, assignmentName, grade):
    data = load_data()

    if "courses" not in data or course_id not in data["courses"]:
        return

    course = data["courses"][course_id]

    if "students" not in course or student_id not in course["students"]:
        return

    numeric_grade = float(grade)
    student_record = course["students"][student_id]


    if "grades" not in student_record or not isinstance(student_record["grades"], dict):
        student_record["grades"] = {}

    student_record["grades"][assignmentName] = numeric_grade
    save_data(data)

def edit_grade(course_id, student_id, assignmentName, new_grade):
    data = load_data()

    if "courses" not in data or course_id not in data["courses"]:
        return

    course = data["courses"][course_id]

    if "students" not in course or student_id not in course["students"]:
        return

    student_record = course["students"][student_id]

    if "grades" not in student_record or assignmentName not in student_record["grades"]:
        return

    numeric_grade = float(new_grade)

    student_record["grades"][assignmentName] = numeric_grade

    save_data(data)

def main():
    while True:
        print("Welcome to the grading management system")
        print("This are the options you can choose")
        print("1. Add a student")
        print("2. Remove a student")
        print("3. Add grade")
        print("4. Edit grade")
        print("5. Exit")
        value = input("Enter your choice: ")

        if value == "1":
            filename = input("Enter student file name: ").strip()
            print(f"filename: {filename}")
            add_student(filename)
        elif value == "2":
            student_id = input("Enter the student ID: ").strip()
            course_id = input("Enter the course ID: ").strip()
            remove_student(student_id, course_id)
        elif value == "3":
            course_id = input("Enter the course ID: ")
            student_id = input("Enter the student ID: ")
            assignmentName = input("Enter the assignment name: ")
            grade = input("Enter the grade: ")
            add_grade(course_id, student_id, assignmentName, grade)
        elif value == "4":
            course_id = input("Enter the course ID: ")
            student_id = input("Enter the student ID: ")
            assignmentName = input("Enter the assignment name: ")
            new_grade = input("Enter the new grade: ")
            edit_grade(course_id, student_id, assignmentName, new_grade)
        elif value == "5":
            print("Exiting grade management system. Bye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, 4 or 5.")
