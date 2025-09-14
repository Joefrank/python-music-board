class Interval:
    is_virtual = False
    vertical_positioning = 0
    position_rect = None
    key = None
    key_id = None
    notes = []

    def __init__(self, position_rect, key, key_id, is_virtual, vertical_positioning):
        self.position_rect = position_rect
        self.key = key
        self.key_id = key_id
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning

    def add_note(self, note):
        self.notes.append(note)

    """
        Thickness will be highest y - lowest y + 1 because we count tickness as no of pixels. e.g. 140 to 149
    """
    def get_tickness(self):
        return (self.position_rect.bottom_left.y - self.position_rect.top_left.y + 1)