"""output"""
import curses

import numpy as np

def list_courses(courses):
    print("\n=== Course list ===")
    if not courses:
        print("(no courses yet)")
        return
    print(f"{'ID':<10}{'Name':<25}{'Credit':<8}")
    print("-" * 45)
    for c in courses:
        print(f"{c.id:<10}{c.name:<25}{c.credit:<8}")


def list_students(students):
    print("\n=== Student list ===")
    if not students:
        print("(no students yet)")
        return
    print(f"{'ID':<10}{'Name':<25}{'DoB':<15}")
    print("-" * 50)
    for s in students:
        print(f"{s.id:<10}{s.name:<25}{s.dob:<15}")


def show_marks_for_course(students, courses):
    import input as my_input  # local import: avoids a circular import

    course = my_input.select_course(courses)
    if course is None:
        return

    print(f"\n=== Marks for course: {course.name} ({course.id}) ===")
    if not students:
        print("(no students yet)")
        return

    print(f"{'ID':<10}{'Name':<25}{'Mark':<10}")
    print("-" * 45)
    for s in students:
        mark = s.get_mark(course.id)
        print(f"{s.id:<10}{s.name:<25}{mark if mark is not None else 'N/A'}")


def list_students_by_gpa(students, courses):
    """Show every student's GPA, sorted descending (numpy-based)."""
    print("\n=== Student GPA ranking (descending) ===")
    if not students:
        print("(no students yet)")
        return
    if not courses:
        print("(no courses yet)")
        return

    gpas = np.array([s.gpa(courses) for s in students])
    order = np.argsort(gpas)[::-1]  # descending

    print(f"{'Rank':<6}{'ID':<10}{'Name':<25}{'GPA':<8}")
    print("-" * 50)
    for rank, idx in enumerate(order, start=1):
        s = students[idx]
        print(f"{rank:<6}{s.id:<10}{s.name:<25}{gpas[idx]:<8.2f}")

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


def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # title
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)    # selected item
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # footer hint


def draw_menu(stdscr, selected):
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