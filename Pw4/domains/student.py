"""Student domain class."""
import math

import numpy as np


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
        return float(np.sum(credit_arr * mark_arr) / np.sum(credit_arr))