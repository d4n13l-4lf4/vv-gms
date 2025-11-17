import os
import json


def add_student(filename):

    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print("Student file is empty.")
        return

    header_line = lines[0].strip()
    # Detección de delimitador (tu lógica original)
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


        if len(row) < 2:
            continue

        student_id = row[0]
        student_name = row[1]

        if not student_id:
            continue

        if student_id not in data["students"]:
            data["students"][student_id] = {
                "student_id": student_id,
                "student_name": student_name
            }
            print(f"Added student {student_name} ({student_id}).")
        else:
            # Si ya existe, opcionalmente actualizamos el nombre si es distinto
            if data["students"][student_id].get("student_name") != student_name:
                data["students"][student_id]["student_name"] = student_name
                print(f"Updated student name for {student_id} to {student_name}.")

    save_data(data)


def remove_student(student_id, course_id):

    data = load_data()

    if student_id not in data.get("students", {}):
        print(f"Student {student_id} does not exist.")
        return

    if course_id not in data.get("grades", {}):
        print(f"Course {course_id} has no grades registered.")
        return

    original_len = len(data["grades"][course_id])
    data["grades"][course_id] = [
        g for g in data["grades"][course_id]
        if g.get("student_id") != student_id
    ]
    removed = original_len - len(data["grades"][course_id])

    if removed > 0:
        print(f"Removed {removed} grade(s) for student {student_id} in course {course_id}.")
    else:
        print(f"No grades found for student {student_id} in course {course_id}.")

    save_data(data)


def add_grade(course_id, student_id, assignmentName, grade):

    data = load_data()

    if course_id not in data.get("courses", {}):
        print(f"Course {course_id} does not exist in 'courses'.")
        return

    if student_id not in data.get("students", {}):
        print(f"Student {student_id} does not exist in 'students'.")
        return

    try:
        numeric_grade = float(grade)
    except ValueError:
        print("Grade must be a number.")
        return

    # Inicializar lista de grades para el curso si no existe
    if "grades" not in data:
        data["grades"] = {}
    if course_id not in data["grades"]:
        data["grades"][course_id] = []

    # Evitar duplicados exactos (student_id + assignmentName)
    for g in data["grades"][course_id]:
        if g.get("student_id") == student_id and g.get("assignment_name") == assignmentName:
            print("Grade already exists for this student and assignment. Use 'edit grade' instead.")
            return

    data["grades"][course_id].append({
        "student_id": student_id,
        "assignment_name": assignmentName,
        "grade": numeric_grade
    })

    print(f"Added grade {numeric_grade} for student {student_id} in {course_id} - {assignmentName}.")
    save_data(data)


def edit_grade(course_id, student_id, assignmentName, new_grade):
    """
    Edita una nota existente en la estructura de 'grades'.
    """
    data = load_data()

    if course_id not in data.get("grades", {}):
        print(f"No grades found for course {course_id}.")
        return

    try:
        numeric_grade = float(new_grade)
    except ValueError:
        print("New grade must be a number.")
        return

    grades_list = data["grades"][course_id]
    found = False

    for g in grades_list:
        if g.get("student_id") == student_id and g.get("assignment_name") == assignmentName:
            g["grade"] = numeric_grade
            found = True
            break

    if not found:
        print(f"No grade found for student {student_id} in course {course_id} for assignment '{assignmentName}'.")
        return

    print(f"Updated grade for student {student_id} in {course_id} - {assignmentName} to {numeric_grade}.")
    save_data(data)


def main():
    while True:
        print("Welcome to the grading management system")
        print("These are the options you can choose")
        print("1. Add a student")
        print("2. Remove a student from a course (remove grades)")
        print("3. Add grade")
        print("4. Edit grade")
        print("5. Exit")
        value = input("Enter your choice: ")

        if value == "1":
            filename = input("Enter student file name: ").strip()
            add_student(filename)
        elif value == "2":
            student_id = input("Enter the student ID: ").strip()
            course_id = input("Enter the course ID: ").strip()
            remove_student(student_id, course_id)
        elif value == "3":
            course_id = input("Enter the course ID: ").strip()
            student_id = input("Enter the student ID: ").strip()
            assignmentName = input("Enter the assignment name: ").strip()
            grade = input("Enter the grade: ").strip()
            add_grade(course_id, student_id, assignmentName, grade)
        elif value == "4":
            course_id = input("Enter the course ID: ").strip()
            student_id = input("Enter the student ID: ").strip()
            assignmentName = input("Enter the assignment name: ").strip()
            new_grade = input("Enter the new grade: ").strip()
            edit_grade(course_id, student_id, assignmentName, new_grade)
        elif value == "5":
            print("Exiting grade management system. Bye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, 4 or 5.")


if __name__ == '__main__':
    main()