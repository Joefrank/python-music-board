class Interval:
    is_virtual = False
    vertical_positioning = 0
    position_rect = None
    key = None
    key_id = None
    notes = []
    staff_index = None

    def __init__(self, position_rect, key, key_id, is_virtual, vertical_positioning, staff_index):
        self.staff_index = staff_index
        self.position_rect = position_rect
        self.key = key
        self.key_id = key_id
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning

    def add_note(self, note):
        self.notes.append(note)

    """
        Thickness will be highest y - lowest y + 1 because we count thickness as no of pixels. e.g. 140 to 149
    """
    def get_thickness(self):
        return self.position_rect.bottom_left.y - self.position_rect.top_left.y + 1

    """ Checks if point is contained within an interval. """
    def contains_position(self, position):
        return ((self.position_rect.top_left.x <= position.x <= self.position_rect.top_right.x) 
            and (self.position_rect.top_left.y <= position.y <= self.position_rect.bottom_left.y))

    def __str__(self):
        return (f"\n{"Virtual " if self.is_virtual else ""}Interval #{self.staff_index} - Key id: {self.key_id} - Vertical positioning: {self.vertical_positioning} - Top-Left{self.position_rect.top_left.x, self.position_rect.top_left.y} - Top-Right: {self.position_rect.top_right.x, self.position_rect.top_right.y} "
                f"- Bottom-Left: {self.position_rect.bottom_left.x, self.position_rect.bottom_left.y} - Bottom-Right: {self.position_rect.bottom_right.x, self.position_rect.bottom_right.y}"
                )