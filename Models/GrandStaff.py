

import copy


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

    def get_top_left(self):
        if len(self.staves) > 0:
            return self.staves[0].get_top_left()
        
    def get_bottom_left(self):        
        no_of_staves = len(self.staves)
        if no_of_staves > 0:
            return self.staves[no_of_staves - 1].get_bottom_left()
        
    def get_notes(self):
        notes = []
        for staff in self.staves:
            notes.extend(staff.get_notes())
        return notes
    
    def get_notes_offsets(self):
        if len(self.staves) > 0:
            return self.staves[0].get_notes_offsets()
    
    def get_initial_navigator_line(self):
        top_staff_top, _ = self.staves[0].get_initial_navigator_line()
        _, bottom_staff_bottom = self.staves[-1].get_initial_navigator_line() 
        top_left = copy.deepcopy(top_staff_top)
        bottom_left = copy.deepcopy(bottom_staff_bottom)
        return (top_left, bottom_left)
    