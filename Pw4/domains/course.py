"""Course domain class."""


class Course:
    """A course: id, name, and number of credits (used to weight the GPA)."""

    def __init__(self, cid, name, credit):
        self.id = cid
        self.name = name
        self.credit = credit