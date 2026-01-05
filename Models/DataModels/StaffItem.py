

""" Class acts as parent class for Line and Interval """
class StaffItem:
    def __init__(self, staff_index, key, key_id, is_virtual, vertical_positioning, 
                 line_collateral_boundaries, velocity, tempo, **kwargs):
        super().__init__(**kwargs)
        self.staff_index = staff_index
        self.key = key
        self.key_id = key_id
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning
        self.line_collateral_boundaries = line_collateral_boundaries
        self.velocity: int = velocity
        self.tempo: int = tempo
        self.notes = []

