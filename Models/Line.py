class Line:
    is_virtual = False
    staff_index = None
    vertical_positioning = 0
    start_position = None
    end_position = None
    key = None
    key_id = None
    notes = []
    thickness = None

    def __init__(self, start_position, end_position, thickness, is_virtual, key, key_id, vertical_positioning, staff_index):
        self.staff_index = staff_index
        self.start_position = start_position
        self.end_position = end_position
        self.thickness = thickness
        self.key = key
        self.key_id = key_id
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning

    def add_note(self, note):
        self.notes.append(note)

    def contains_position(self, position):
        return ((self.start_position.x <= position.x <= self.end_position.x and position.y == self.start_position.y)
        or (self.start_position.y <= position.y <= self.end_position.y and position.x == self.start_position.x))

    def is_above_position(self, position):
        return self.start_position.y < position.y and self.end_position.y < position.y
    
    def is_below_position(self, position):
        return self.start_position.y > position.y and self.end_position.y > position.y

    def __str__(self):
        return f"\n{"Virtual " if self.is_virtual else ""}Line #{self.staff_index} - Thickness: {self.thickness} - Key id: {self.key_id} - Vertical positioning: {self.vertical_positioning} - Start: {self.start_position} - End: {self.end_position}"