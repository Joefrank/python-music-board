class Interval:
    is_virtual = False
    vertical_positioning = 0
    position_rect = None
    key = None
    key_id = None
    notes = []
    staff_index = None

    def __init__(self, position_rect, key, key_id, is_virtual, vertical_positioning, staff_index, line_collateral_boundaries):
        self.staff_index = staff_index
        self.position_rect = position_rect
        self.key = key
        self.key_id = key_id
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning
        self.line_collateral_boundaries = line_collateral_boundaries

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

    def is_within_collateral_boundaries(self, position):
        return self.line_collateral_boundaries.left_boundary <= position.x <= self.line_collateral_boundaries.right_boundary
    
    """
        Checks if mouse position is within interval but leaving a threshold/padding if specified
    """
    def mouse_hovering_around(self, mouse_position, vertical_threshold=0):        
        return (self.is_within_collateral_boundaries(mouse_position) and
             (self.position_rect.top_left.y + vertical_threshold <= mouse_position.y 
              <= self.position_rect.bottom_left.y - vertical_threshold))
    
    def __str__(self):
        return (f"\n{"Virtual " if self.is_virtual else ""}Interval #{self.staff_index} - Key id: {self.key_id} - Vertical positioning: {self.vertical_positioning} - Top-Left{self.position_rect.top_left} - Top-Right: {self.position_rect} "
                f"- Bottom-Left: {self.position_rect.bottom_left} - Bottom-Right: {self.position_rect.bottom_right}"
                )