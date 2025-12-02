import os

from vv_gms.dani.utils.stats.statistics import calculate_student_grade
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

    # Output del PDF
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

    # Asegurar que course_teacher existe
    if "course_teacher" not in data:
        data["course_teacher"] = {}

    # Asegurar que el curso tenga lista de profesores asignados
    if course_id not in data["course_teacher"]:
        data["course_teacher"][course_id] = []

    # Error Case del PDF:
    if teacher_id in data["course_teacher"][course_id]:
        print("Error: Teacher already assigned.")
        return


    data["course_teacher"][course_id].append(teacher_id)

    # Output del PDF:
    print(f"Teacher {data['teachers'][teacher_id]['name']} assigned to {course_id}.")

    save_data(data)


# REMOVE TEACHER
def remove_teacher(course_id, teacher_id):
    data = load_data()

    # Error Case del PDF:
    if course_id not in data["courses"]:
        print("Error: CourseID not found.")
        return

    # Error Case del PDF:
    if course_id not in data["course_teacher"]:
        print("Error: Teacher not assigned to this course.")
        return

    data["course_teacher"][course_id].remove(teacher_id)

    # Output del PDF
    print(f"Teacher {data['teachers'][teacher_id]['name']} removed from {course_id}.")

    save_data(data)

# CALCULATE COURSE STATS
def calc_course_stats(course_id: str):

    data = load_data()

    # Error Case del PDF:
    if course_id not in data["courses"]:
        print("Error: CourseID not found.")
        return

    students = [s for s_id, s in data["students"].items()]
    assignments = data.get("assignments", {}).get(course_id, [])
    grades = data.get("grades", {}).get(course_id, [])

    # Error Case del PDF:
    if not assignments:
        print("Error: No assignments defined for this course.")
        return

    # Error Case del PDF:
    if not grades:
        print("Error: No grades recorded for this course.")
        return

    final_grades_objs = calculate_student_grade(students, assignments, grades)
    final_grades = [s.grade for s in final_grades_objs if s.grade is not None]

    course_average = sum(final_grades) / len(final_grades)
    median = statistics.median(final_grades)
    stddev = statistics.pstdev(final_grades)

    # Output del PDF:
    print(f"Course: {course_id}")
    print(f"Students evaluated: {len(final_grades)}")
    print(f"Course Average: {course_average:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Standard Deviation: {stddev:.2f}")
