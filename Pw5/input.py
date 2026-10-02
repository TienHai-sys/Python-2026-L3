"""input"""
from domains import Student, Course

def input_number(prompt):
    """Read a non-negative integer, re-asking until valid."""
    while True:
        try:
            n = int(input(prompt))
            if n < 0:
                print("Please enter a non-negative number.")
                continue
            return n
        except ValueError:
            print("Invalid number, try again.")

def write_students(students):
    with open("students.txt", "w", encoding="utf-8") as f:
        for s in students:
            f.write(f"{s.id},{s.name},{s.dob}\n")


def write_courses(courses):
    with open("courses.txt", "w", encoding="utf-8") as f:
        for c in courses:
            f.write(f"{c.id},{c.name},{c.credit}\n")


def write_marks(students, courses):
    with open("marks.txt", "w", encoding="utf-8") as f:
        for c in courses:
            for s in students:
                mark = s.get_mark(c.id)
                if mark is not None:
                    f.write(f"{c.id},{s.id},{mark}\n")

def input_students():
    """Input the number of students, then their id/name/DoB; save to students.txt."""
    n = input_number("Enter number of students: ")
    students = []
    for i in range(n):
        print(f"\n-- Student {i + 1} --")
        sid = input("  Student id: ").strip()
        name = input("  Student name: ").strip()
        dob = input("  Date of birth (dd/mm/yyyy): ").strip()
        students.append(Student(sid, name, dob))
    write_students(students)
    print("Saved to students.txt")
    return students


def input_courses():
    """Input the number of courses, then their id/name/credit; save to courses.txt."""
    n = input_number("Enter number of courses: ")
    courses = []
    for i in range(n):
        print(f"\n-- Course {i + 1} --")
        cid = input("  Course id: ").strip()
        cname = input("  Course name: ").strip()
        credit = input_number("  Credit: ")
        courses.append(Course(cid, cname, credit))
    write_courses(courses)
    print("Saved to courses.txt")
    return courses


def find_course(courses, course_id):
    for c in courses:
        if c.id == course_id:
            return c
    return None


def select_course(courses):
    """Let the user pick one of the existing courses. Returns the Course or None."""
    import output 

    if not courses:
        print("No courses available yet. Please add courses first.")
        return None

    output.list_courses(courses)
    course_id = input("Enter the id of the course to select: ").strip()
    course = find_course(courses, course_id)
    if course is None:
        print("Course not found.")
    return course


def input_marks_for_course(students, courses):
    """Select a course, input marks for every student, then save to marks.txt."""
    course = select_course(courses)
    if course is None:
        return

    if not students:
        print("No students available yet. Please add students first.")
        return

    print(f"\nEntering marks for course: {course.name} ({course.id})")
    print("Scores are rounded DOWN to 1 decimal place (math.floor).")
    for s in students:
        while True:
            try:
                raw = input(f"  Mark for {s.name} ({s.id}): ").strip()
                raw_mark = float(raw)
                s.set_mark(course.id, raw_mark)
                print(f"    -> stored as {s.get_mark(course.id)}")
                break
            except ValueError:
                print("  Invalid mark, please enter a number.")

    write_marks(students, courses)
    print("Saved to marks.txt")