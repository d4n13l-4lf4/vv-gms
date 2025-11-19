import os
from vv_gms.shared import load_data, save_data
import statistics


# ADD TEACHER
def add_teacher(filename):
    # Comprueba si existe el archivo
    if not os.path.exists(filename):
        print("Error: Invalid file.")
        return

    # Carga datos previos
    data = load_data()

    # Abre el archivo
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print("Error: Empty file.")
        return

    # Analiza el encabezado y el delimitador
    header = lines[0].strip()
    if "," in header:
        delimiter = ","
    elif ";" in header:
        delimiter = ";"
    else:
        print("Error: Invalid file format. Delimiter not supported.")
        return

    # Procesa cada línea de datos
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        row = [col.strip() for col in line.split(delimiter)]

        # Validación de formato
        if len(row) < 2:
            print("Error: Invalid input type file, or arguments. Use: <TeacherID> <TeacherName>")
            continue

        teacher_id = row[0].strip()
        teacher_name = row[1].strip()

        # Validación de campos vacíos
        if not teacher_id or not teacher_name:
            print("Error: Invalid input type file, or arguments. Use: <TeacherID> <TeacherName>")
            continue

        if "teachers" not in data:
            data["teachers"] = {}

        # Validación de duplicados
        if teacher_id in data["teachers"]:
            print(f"Error: {teacher_id} already exists.")
            continue

        # Añade el profesor
        data["teachers"][teacher_id] = {"name": teacher_name}
        print(f"Added teacher {teacher_name} ({teacher_id}).")

    print("List of teachers added to the system.")
    save_data(data)



# ASSIGN TEACHER TO A COURSE
def assign_teacher(course_id, teacher_id):
    data = load_data()

    # Error Case del PDF:
    if course_id not in data["courses"]:
        print("Error: CourseID not found.")
        return

    if teacher_id not in data["teachers"]:
        print("Error: TeacherID not found.")
        return

    course = data["courses"][course_id]

    if "teachers" not in course:
        course["teachers"] = []

    # Error Case del PDF:
    if teacher_id in course["teachers"]:
        print("Error: Teacher already assigned.")
        return

    course["teachers"].append(teacher_id)

    # Output del PDF
    print(f"Teacher {data['teachers'][teacher_id]['name']} assigned to {course_id}.")

    save_data(data)


# REMOVE TEACHER
def remove_teacher(course_id, teacher_id):
    data = load_data()

    # Error Case del PDF:
    if course_id not in data["courses"]:
        print("Error: CourseID not found.")
        return

    course = data["courses"][course_id]

    # Error Case del PDF:
    if "teachers" not in course or teacher_id not in course["teachers"]:
        print("Error: Teacher not assigned to this course.")
        return

    course["teachers"].remove(teacher_id)

    # Output del PDF:
    print(f"Teacher {data['teachers'][teacher_id]['name']} removed from {course_id}.")
    save_data(data)


def calc_course_stats(course_id):
    # Error Case del PDF:
    if not course_id:
        print("Error: Invalid arguments. Use: calc_course_stats <CourseID>")
        return

    data = load_data()

    # Error Case del PDF:
    if course_id not in data["courses"]:
        print("Error: CourseID not found.")
        return

    course = data["courses"][course_id]

    if "students" not in course or not course["students"]:
        print("Error: No students in this course.")
        return


    final_grades = []

    for student_id, info in course["students"].items():
        if "grades" not in info or not info["grades"]:
            continue

        grades = list(info["grades"].values())
        avg = sum(grades) / len(grades)
        final_grades.append(avg)

    # Error Case del PDF:
    if not final_grades:
        print("Error: No assignments defined for this course.")
        # print("Error: No grades recorded for this course.") # DUDA -> los dos errores se tratan de la misma manera
        return

    course_average = sum(final_grades) / len(final_grades)
    median = statistics.median(final_grades)
    stddev = statistics.pstdev(final_grades)

    # Output del PDF:
    print(f"Course: {course_id}")
    print(f"Students evaluated: {len(final_grades)}")
    print(f"Course Average: {course_average:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Standard Deviation: {stddev:.2f}")
