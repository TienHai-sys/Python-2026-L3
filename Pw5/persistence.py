"""
persistence
"""
import os
import zipfile

from domains import Student, Course

DATA_FILES = ["students.txt", "courses.txt", "marks.txt"]
ARCHIVE_NAME = "students.dat"

def save_archive():
    """Compress the existing .txt data files into students.dat (zip)."""
    existing = [f for f in DATA_FILES if os.path.exists(f)]
    if not existing:
        return
    with zipfile.ZipFile(ARCHIVE_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in existing:
            zf.write(fname)
    print(f"Saved data into {ARCHIVE_NAME}")


def load_archive():
    """If students.dat exists (from a previous run), unpack the .txt files from it."""
    if not os.path.exists(ARCHIVE_NAME):
        return False
    with zipfile.ZipFile(ARCHIVE_NAME, "r") as zf:
        zf.extractall()
    print(f"Loaded data from {ARCHIVE_NAME}")
    return True

def load_students():
    students = []
    if not os.path.exists("students.txt"):
        return students
    with open("students.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid, name, dob = line.split(",", 2)
            students.append(Student(sid, name, dob))
    return students


def load_courses():
    courses = []
    if not os.path.exists("courses.txt"):
        return courses
    with open("courses.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cid, name, credit = line.split(",", 2)
            courses.append(Course(cid, name, int(credit)))
    return courses


def load_marks(students, courses):
    """Fill in students[*].marks from marks.txt (course_id,student_id,mark)."""
    if not os.path.exists("marks.txt"):
        return
    student_by_id = {s.id: s for s in students}
    with open("marks.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            course_id, student_id, mark = line.split(",", 2)
            student = student_by_id.get(student_id)
            if student is not None:
                student.marks[course_id] = float(mark)


def load_all():
    """Load persisted state at program startup. Returns (students, courses)."""
    load_archive()  
    students = load_students()
    courses = load_courses()
    load_marks(students, courses)
    return students, courses