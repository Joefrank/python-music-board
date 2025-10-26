class GrandStaff:   
   
    def __init__(self, staves=None, top_left = (0, 0), bottom_right = (0, 0)):
        if staves is None:
            self.staves = []
        self.staves = staves
        self.top_left_position = top_left
        self.bottom_right_position = bottom_right

    def add_staff(self, staff):
        self.staves.append(staff)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left

    def set_bottom_right_position(self, bottom_right):
        self.bottom_right_position = bottom_right

    def find_nearest_note(self, position):
        for staff in self.staves:
            note = staff.find_nearest_note(position)
            if note is not None:
                return note
        return None

