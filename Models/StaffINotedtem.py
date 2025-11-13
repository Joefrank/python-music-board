""" Items added directly to staff and that can hold notes like lines and intervals"""
class StaffNotedItem:
    
    def __init__(self, is_virtual, staff_index, key, key_id, vertical_positioning, line_collateral_boundaries):
        self.notes = []
        self.is_virtual = is_virtual
        self.staff_index = staff_index
        self.key = key
        self.key_id = key_id
        self.vertical_positioning = vertical_positioning
        self.line_collateral_boundaries = line_collateral_boundaries