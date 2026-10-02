"""
main
"""
import curses

import input as my_input
import output as my_output


def run_action(stdscr, state, index):
    """Leave curses mode, run a plain-console action, then come back."""
    curses.endwin()
    print("\n" + "=" * 50)
    try:
        if index == 0:
            state["students"] = my_input.input_students()
        elif index == 1:
            state["courses"] = my_input.input_courses()
        elif index == 2:
            my_input.input_marks_for_course(state["students"], state["courses"])
        elif index == 3:
            my_output.list_courses(state["courses"])
        elif index == 4:
            my_output.list_students(state["students"])
        elif index == 5:
            my_output.show_marks_for_course(state["students"], state["courses"])
        elif index == 6:
            my_output.list_students_by_gpa(state["students"], state["courses"])
    except Exception as exc:
        print(f"Error: {exc}")
    input("\nPress Enter to go back to the menu...")
    stdscr.refresh()


def curses_main(stdscr):
    curses.curs_set(0)
    my_output.init_colors()

    state = {"students": [], "courses": []}
    selected = 0

    while True:
        my_output.draw_menu(stdscr, selected)
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % len(my_output.MENU_ITEMS)
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % len(my_output.MENU_ITEMS)
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            if selected == len(my_output.MENU_ITEMS) - 1:  # Exit
                break
            run_action(stdscr, state, selected)
        elif key in (ord("q"), ord("Q")):
            break


def main():
    curses.wrapper(curses_main)
    print("Goodbye!")


if __name__ == "__main__":
    main()