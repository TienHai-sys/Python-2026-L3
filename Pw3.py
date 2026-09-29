"""
Practical work 3:
"""

import math
import curses

import numpy as np

# Domain classes

class Student:
    """A student: id, name, date of birth, and their marks per course id."""

    def __init__(self, sid, name, dob):
        self.id = sid
        self.name = name
        self.dob = dob
        self.marks = {}  # {course_id: mark}

    def set_mark(self, course_id, raw_mark):
        """Store a mark, rounded DOWN to 1 decimal place with math.floor()."""
        rounded = math.floor(raw_mark * 10) / 10
        self.marks[course_id] = rounded

    def get_mark(self, course_id):
        return self.marks.get(course_id)

    def gpa(self, courses):
        """
        Credit-weighted average GPA, computed with numpy arrays:

            GPA = sum(credit_i * mark_i) / sum(credit_i)

        `courses` is the list of Course objects; only courses this
        student actually has a mark for are counted.
        """
        credits = []
        student_marks = []
        for c in courses:
            mark = self.marks.get(c.id)
            if mark is not None:
                credits.append(c.credit)
                student_marks.append(mark)

        if not credits:
            return 0.0

        credit_arr = np.array(credits, dtype=float)
        mark_arr = np.array(student_marks, dtype=float)
        weighted_sum = np.sum(credit_arr * mark_arr)
        total_credit = np.sum(credit_arr)
        return float(weighted_sum / total_credit)


class Course:
    """A course: id, name, and number of credits (used to weight the GPA)."""

    def __init__(self, cid, name, credit):
        self.id = cid
        self.name = name
        self.credit = credit

# Manager: holds the data + all input/listing operations
class SchoolManager:
    def __init__(self):
        self.students = []
        self.courses = []

    # helpers
    def find_course(self, course_id):
        for c in self.courses:
            if c.id == course_id:
                return c
        return None

    def select_course(self):
        if not self.courses:
            print("No courses available yet. Please add courses first.")
            return None
        self.list_courses()
        course_id = input("Enter the id of the course to select: ").strip()
        course = self.find_course(course_id)
        if course is None:
            print("Course not found.")
        return course

    # input functions
    def input_number_of_students(self):
        while True:
            try:
                n = int(input("Enter number of students: "))
                if n < 0:
                    print("Please enter a non-negative number.")
                    continue
                return n
            except ValueError:
                print("Invalid number, try again.")

    def input_students(self):
        n = self.input_number_of_students()
        self.students = []
        for i in range(n):
            print(f"\n-- Student {i + 1} --")
            sid = input("  Student id: ").strip()
            name = input("  Student name: ").strip()
            dob = input("  Date of birth (dd/mm/yyyy): ").strip()
            self.students.append(Student(sid, name, dob))

    def input_number_of_courses(self):
        while True:
            try:
                n = int(input("Enter number of courses: "))
                if n < 0:
                    print("Please enter a non-negative number.")
                    continue
                return n
            except ValueError:
                print("Invalid number, try again.")

    def input_courses(self):
        n = self.input_number_of_courses()
        self.courses = []
        for i in range(n):
            print(f"\n-- Course {i + 1} --")
            cid = input("  Course id: ").strip()
            cname = input("  Course name: ").strip()
            while True:
                try:
                    credit = int(input("  Credit (so tin chi): ").strip())
                    if credit <= 0:
                        print("  Credit must be a positive number.")
                        continue
                    break
                except ValueError:
                    print("  Invalid number, try again.")
            self.courses.append(Course(cid, cname, credit))

    def input_marks_for_course(self):
        course = self.select_course()
        if course is None:
            return
        if not self.students:
            print("No students available yet. Please add students first.")
            return

        print(f"\nEntering marks for course: {course.name} ({course.id})")
        print("Scores are rounded DOWN to 1 decimal place (math.floor).")
        for s in self.students:
            while True:
                try:
                    raw = input(f"  Mark for {s.name} ({s.id}): ").strip()
                    raw_mark = float(raw)
                    s.set_mark(course.id, raw_mark)
                    print(f"    -> stored as {s.get_mark(course.id)}")
                    break
                except ValueError:
                    print("  Invalid mark, please enter a number.")

    # listing functions
    def list_courses(self):
        print("\n=== Course list ===")
        if not self.courses:
            print("(no courses yet)")
            return
        print(f"{'ID':<10}{'Name':<25}{'Credit':<8}")
        print("-" * 45)
        for c in self.courses:
            print(f"{c.id:<10}{c.name:<25}{c.credit:<8}")

    def list_students(self):
        print("\n=== Student list ===")
        if not self.students:
            print("(no students yet)")
            return
        print(f"{'ID':<10}{'Name':<25}{'DoB':<15}")
        print("-" * 50)
        for s in self.students:
            print(f"{s.id:<10}{s.name:<25}{s.dob:<15}")

    def show_marks_for_course(self):
        course = self.select_course()
        if course is None:
            return
        print(f"\n=== Marks for course: {course.name} ({course.id}) ===")
        if not self.students:
            print("(no students yet)")
            return
        print(f"{'ID':<10}{'Name':<25}{'Mark':<10}")
        print("-" * 45)
        for s in self.students:
            mark = s.get_mark(course.id)
            print(f"{s.id:<10}{s.name:<25}{mark if mark is not None else 'N/A'}")

    # numpy: GPA + sorting 
    def list_students_by_gpa(self):
        """Show every student's GPA, sorted descending (numpy-based)."""
        print("\n=== Student GPA ranking (descending) ===")
        if not self.students:
            print("(no students yet)")
            return
        if not self.courses:
            print("(no courses yet)")
            return

        gpas = np.array([s.gpa(self.courses) for s in self.students])
        # argsort ascending, then reverse for descending order
        order = np.argsort(gpas)[::-1]

        print(f"{'Rank':<6}{'ID':<10}{'Name':<25}{'GPA':<8}")
        print("-" * 50)
        for rank, idx in enumerate(order, start=1):
            s = self.students[idx]
            print(f"{rank:<6}{s.id:<10}{s.name:<25}{gpas[idx]:<8.2f}")

# curses-based decorated menu

MENU_ITEMS = [
    "Input students",
    "Input courses",
    "Select a course & input marks",
    "List courses",
    "List students",
    "Show marks for a course",
    "Show GPA ranking (numpy, sorted desc)",
    "Exit",
]


def draw_menu(stdscr, manager, selected):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    title = " STUDENT MARK MANAGEMENT "
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(1, max(0, (width - len(title)) // 2), title)
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

    box_top, box_left = 3, 4
    box_height = len(MENU_ITEMS) + 2
    box_width = 45

    try:
        win = curses.newwin(box_height, box_width, box_top, box_left)
        win.box()
        for i, item in enumerate(MENU_ITEMS):
            label = f"{i + 1}. {item}"
            if i == selected:
                win.attron(curses.color_pair(2) | curses.A_BOLD)
                win.addstr(i + 1, 2, label)
                win.attroff(curses.color_pair(2) | curses.A_BOLD)
            else:
                win.addstr(i + 1, 2, label)
        win.refresh()
    except curses.error:
        # terminal too small for the box; fall back to a plain list
        for i, item in enumerate(MENU_ITEMS):
            mark = ">" if i == selected else " "
            stdscr.addstr(box_top + i, box_left, f"{mark} {i + 1}. {item}")

    info = "Up/Down: move   Enter: select   q: quit"
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height - 2, 2, info[: max(0, width - 4)])
    stdscr.attroff(curses.color_pair(3))
    stdscr.refresh()


def run_action(stdscr, manager, index):
    """Leave curses mode, run a plain-console action, then come back."""
    curses.endwin()
    print("\n" + "=" * 50)
    try:
        if index == 0:
            manager.input_students()
        elif index == 1:
            manager.input_courses()
        elif index == 2:
            manager.input_marks_for_course()
        elif index == 3:
            manager.list_courses()
        elif index == 4:
            manager.list_students()
        elif index == 5:
            manager.show_marks_for_course()
        elif index == 6:
            manager.list_students_by_gpa()
    except Exception as exc:  # keep the menu alive even if something goes wrong
        print(f"Error: {exc}")
    input("\nPress Enter to go back to the menu...")
    stdscr.refresh()


def curses_main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # title
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)    # selected item
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # footer hint

    manager = SchoolManager()
    selected = 0

    while True:
        draw_menu(stdscr, manager, selected)
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % len(MENU_ITEMS)
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % len(MENU_ITEMS)
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            if selected == len(MENU_ITEMS) - 1:  # Exit
                break
            run_action(stdscr, manager, selected)
        elif key in (ord("q"), ord("Q")):
            break


def main():
    curses.wrapper(curses_main)
    print("Goodbye!")


if __name__ == "__main__":
    main()