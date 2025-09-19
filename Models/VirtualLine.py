from Models import Line

class VirtualLine(Line):

    def __init__(self, start_position, end_position, thickness, key, key_id, vertical_positioning, staff_index):
        super().__init__(start_position, end_position, thickness, False, key, key_id, vertical_positioning, staff_index)
        self.is_virtual = True