"""
Practical work 1: Student mark management
-------------------------------------------
A simple console program built with functions and collections
(lists / dicts), as required by the practical:

  Input functions:
    - input number of students in a class
    - input student information: id, name, DoB
    - input number of courses
    - input course information: id, name
    - select a course, input marks for students in this course

  Listing functions:
    - list courses
    - list students
    - show student marks for a given course
"""
def input_number_of_students():
    """Input the number of students in a class."""
    while True:
        try:
            n = int(input("Enter number of students: "))
            if n < 0:
                print("Please enter a non-negative number.")
                continue
            return n
        except ValueError:
            print("Invalid number, try again.")


def input_students(n):
    """Input student information (id, name, DoB) for n students."""
    students = []
    for i in range(n):
        print(f"\n-- Student {i + 1} --")
        sid = input("  Student id: ").strip()
        name = input("  Student name: ").strip()
        dob = input("  Date of birth (dd/mm/yyyy): ").strip()
        students.append({"id": sid, "name": name, "dob": dob})
    return students


def input_number_of_courses():
    """Input the number of courses."""
    while True:
        try:
            n = int(input("Enter number of courses: "))
            if n < 0:
                print("Please enter a non-negative number.")
                continue
            return n
        except ValueError:
            print("Invalid number, try again.")


def input_courses(n):
    """Input course information (id, name) for n courses."""
    courses = []
    for i in range(n):
        print(f"\n-- Course {i + 1} --")
        cid = input("  Course id: ").strip()
        cname = input("  Course name: ").strip()
        courses.append({"id": cid, "name": cname})
    return courses


def find_course_by_id(courses, course_id):
    for c in courses:
        if c["id"] == course_id:
            return c
    return None


def select_course(courses):
    """Let the user pick one of the existing courses. Returns the course dict or None."""
    if not courses:
        print("No courses available yet. Please add courses first.")
        return None

    list_courses(courses)
    course_id = input("Enter the id of the course to select: ").strip()
    course = find_course_by_id(courses, course_id)
    if course is None:
        print("Course not found.")
    return course


def input_marks_for_course(students, courses, marks):
    """Select a course, then input marks for every student in that course."""
    course = select_course(courses)
    if course is None:
        return

    if not students:
        print("No students available yet. Please add students first.")
        return

    course_marks = marks.setdefault(course["id"], {})
    print(f"\nEntering marks for course: {course['name']} ({course['id']})")
    for s in students:
        while True:
            try:
                raw = input(f"  Mark for {s['name']} ({s['id']}): ").strip()
                mark = float(raw)
                course_marks[s["id"]] = mark
                break
            except ValueError:
                print("  Invalid mark, please enter a number.")

def list_courses(courses):
    """Print all courses."""
    print("\n=== Course list ===")
    if not courses:
        print("(no courses yet)")
        return
    print(f"{'ID':<10}{'Name':<30}")
    print("-" * 40)
    for c in courses:
        print(f"{c['id']:<10}{c['name']:<30}")


def list_students(students):
    """Print all students."""
    print("\n=== Student list ===")
    if not students:
        print("(no students yet)")
        return
    print(f"{'ID':<10}{'Name':<25}{'DoB':<15}")
    print("-" * 50)
    for s in students:
        print(f"{s['id']:<10}{s['name']:<25}{s['dob']:<15}")


def show_marks_for_course(students, courses, marks):
    """Show marks of every student for a chosen course."""
    course = select_course(courses)
    if course is None:
        return

    course_marks = marks.get(course["id"], {})
    print(f"\n=== Marks for course: {course['name']} ({course['id']}) ===")
    if not students:
        print("(no students yet)")
        return

    print(f"{'ID':<10}{'Name':<25}{'Mark':<10}")
    print("-" * 45)
    for s in students:
        mark = course_marks.get(s["id"], "N/A")
        print(f"{s['id']:<10}{s['name']:<25}{mark}")

MENU =


def main():
    students = []
    courses = []
    marks = {}  # {course_id: {student_id: mark}}

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            n = input_number_of_students()
            students = input_students(n)
        elif choice == "2":
            n = input_number_of_courses()
            courses = input_courses(n)
        elif choice == "3":
            input_marks_for_course(students, courses, marks)
        elif choice == "4":
            list_courses(courses)
        elif choice == "5":
            list_students(students)
        elif choice == "6":
            show_marks_for_course(students, courses, marks)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
