class Line:
    is_virtual = False
    vertical_positioning = 0
    start_position = None
    end_position = None
    key = None
    key_id = None
    notes = []
    thickness = None

    def __init__(self, start_position, end_position, thickness, is_virtual, key, key_id,  vertical_positioning):
        self.start_position = start_position
        self.end_position = end_position
        self.thickness = thickness
        self.key = key
        self.key_id = key_id
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning

    def add_note(self, note):
        self.notes.append(note)