import os
from vv_gms.shared import save_data, load_data


def add_student(filename):

    if not os.path.exists(filename):
        print(f"File '{os.path.basename(filename)}' does not exist.")
        return

    data = load_data()
    if "students" not in data:
        data["students"] = {}
    if "courses" not in data:
        data["courses"] = {}

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print("Student file is empty.")
        return

    header_line = lines[0].strip()

    if filename.endswith(".csv"):
        delimiter = ","
    else:

        if ";" in header_line:
            delimiter = ";"
        elif "," in header_line:
            delimiter = ","
        else:
            delimiter = ";"

    header_cols = [c.strip() for c in header_line.split(delimiter)] if header_line else []
    #if len(header_cols) < 3: THIS IS THE CORRECT ONE
    if len(header_cols) < 4:
        print("Error: Invalid input type file, or arguments. Use: <StudentID> <StudentName> <CourseID>")
        return

    for line in lines[1:]:
        if not line.strip():
            continue

        line = line.strip()
        row = [col.strip() for col in line.split(delimiter)]

        student_id = row[0].strip() if len(row) > 0 else ""
        student_name = row[1].strip() if len(row) > 1 else ""
        course_ids = [c for c in row[2:] if c] if len(row) > 2 else []

        if not student_id or not student_name or not course_ids:
            print("Error: Invalid input type file, or arguments. Use: <StudentID> <StudentName> <CourseID>")
            return

        for course_id in course_ids:
            if course_id not in data["courses"]:
                print("Error: CourseID not found.")
                return

        if student_id not in data["students"]:
            data["students"][student_id] = {
                "student_id": student_id,
                "student_name": student_name,
                "courses": []
            }
        else:
            existing_name = data["students"][student_id].get("student_name")
            if existing_name != student_name and student_name:
                data["students"][student_id]["student_name"] = student_name

        for course_id in course_ids:
            student_courses = data["students"][student_id].setdefault("courses", [])
            if course_id in student_courses:
                print("Error: StudentID already exists in this course.")
                return
            student_courses.append(course_id)
            print(f"Added student {student_name} ({student_id}) to course {course_id}.")

    save_data(data)
    print("List of students added to the system.")

def remove_student(student_id, course_id):


    data = load_data()

    if student_id not in data.get("students", {}):
        print("Error: StudentID not found.")
        return

    if course_id not in data.get("courses", {}):
        print("Error: CourseID not found.")
        return

    print("Warning: Removing a student will delete all associated grades.")

    removed = 0
    if "grades" in data and course_id in data["grades"]:
        original_len = len(data["grades"][course_id])
        data["grades"][course_id] = [
            g for g in data["grades"][course_id]
            if g.get("student_id") != student_id
        ]
        removed = original_len - len(data["grades"][course_id])

    save_data(data)

    print(f"Student {student_id} removed from course {course_id}.")

def add_grade(course_id, student_id, assignmentName, grade):
    data = load_data()

    if (not course_id or not student_id or not assignmentName or
            grade is None or str(grade).strip() == ""):
        print("Error: Invalid arguments. Use: add_grade <CourseID> <StudentID> <AssignmentName> <Grade>")
        return

    courses = data.get("courses", {})
    students = data.get("students", {})
    assignments = data.get("assignments", {})


    if course_id not in courses:
        print("Error: Student or Assignment not found.")
        return


    if student_id not in students: # or not student_has_course:
        print("Error: Student or Assignment not found.")
        return


    course_assignments = assignments.get(course_id, [])
    exists_assignment = any(
        a.get("assignment_name") == assignmentName
        for a in course_assignments
    )
    if not exists_assignment:
        print("Error: Student or Assignment not found.")
        return

    try:
        numeric_grade = float(grade)
    except ValueError:
        print("Error: Invalid grade. Must be between 0 and 100.")
        return

    #if numeric_grade < 0 or numeric_grade > 100: THIS IS THE CORRECT ONE
    if numeric_grade <= 0 or numeric_grade >= 100:

        print("Error: Invalid grade. Must be between 0 and 100.")
        return

    grades_by_course = data["grades"]
    course_grades = grades_by_course.get(course_id, [])

    for g in course_grades:
        if (g.get("student_id") == student_id and
            g.get("assignment_name") == assignmentName and
            g.get("grade") == numeric_grade):
            print("Error: Grade record already exists.")
            return

    course_grades.append({
        "student_id": student_id,
        "assignment_name": assignmentName,
        "grade": numeric_grade
    })

    data["grades"][course_id] = course_grades
    print(
        f"Grade {numeric_grade} recorded for Student {student_id} in assignment {assignmentName} of course {course_id}."
    )
    save_data(data)

def edit_grade(course_id, student_id, assignmentName, new_grade):

    data = load_data()

    if course_id not in data.get("grades", {}):
        print("Error: Grade record not found.")
        return

    try:
        numeric_grade = float(new_grade)
    except ValueError:
        print("Error: Invalid grade. Must be between 0 and 100.")
        return

    if not (0 <= numeric_grade <= 100):
        print("Error: Invalid grade. Must be between 0 and 100.")
        return

    grades_list = data["grades"][course_id]
    found = False

    for g in grades_list:
        if g.get("student_id") == student_id and g.get("assignment_name") == assignmentName:
            g["grade"] = numeric_grade
            found = True
            break

    if not found:
        print("Error: Grade record not found.")
        return

    print(f"Grade updated: Course {course_id}, Student {student_id}, {assignmentName} = {numeric_grade}.")
    # save_data(data) DEBERÍA IR EL SAVE DATA