class Line:    

    def __init__(self, start_position, end_position, thickness, is_virtual, key, key_id, vertical_positioning,
                  staff_index, line_collateral_boundaries):
        self.staff_index = staff_index
        self.start_position = start_position
        self.end_position = end_position
        self.thickness = thickness
        self.key = key
        self.key_id = key_id
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning
        self.line_collateral_boundaries = line_collateral_boundaries
        self.notes = []


    def add_note(self, note):
        self.notes.append(note)

    def is_in_vertical_proximity_of_position(self, position, vertical_threshold=0):
        return (self.start_position.y - vertical_threshold) <= position.y <= (self.start_position.y + vertical_threshold)

    def contains_position(self, position):
        return ((self.start_position.x <= position.x <= self.end_position.x and position.y == self.start_position.y)
        or (self.start_position.y <= position.y <= self.end_position.y and position.x == self.start_position.x))

    def is_within_collateral_boundaries(self, position):
        return self.line_collateral_boundaries.left_boundary <= position.x <= self.line_collateral_boundaries.right_boundary
    
    """
        We use this to track mouse 2 pixels around a line.
    """
    def mouse_hovering_around(self, mouse_position, vertical_threshold=0):
        return (self.is_within_collateral_boundaries(mouse_position) and 
                (self.is_in_vertical_proximity_of_position(mouse_position, vertical_threshold) or
                self.contains_position(mouse_position)))

    def is_above_position(self, position):
        return self.start_position.y < position.y and self.end_position.y < position.y
    
    def is_below_position(self, position):
        return self.start_position.y > position.y and self.end_position.y > position.y

    def get_next_note_index(self):
        return len(self.notes)
    
    def delete_note(self, note):
        if note in self.notes:
            self.notes.remove(note)

    def find_nearest_note(self, position):
        for note in self.notes:            
            if note.is_near_position(position):
                return note        
        return None
    
    def __str__(self):
        return f"\n{"Virtual " if self.is_virtual else ""}Line #{self.staff_index} - Thickness: {self.thickness} - Key id: {self.key_id} - Vertical positioning: {self.vertical_positioning} - Start: {self.start_position} - End: {self.end_position}"