
from Models import StraightLine


class StaffBar:

    def __init__(self, previous, next, line):
        self.previous_bar: StaffBar = previous
        self.next_bar: StaffBar = next
        self.line: StraightLine = line

    def set_previous(self, previous):
        self.previous_bar = previous

    def set_next(self, next):
        self.next_bar = next
        