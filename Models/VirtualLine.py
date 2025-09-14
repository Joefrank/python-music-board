from Models import Line

class VirtualLine(Line):
    position_top = True
    line_offset = 0

    def __init__(self, start_position, end_position, key, key_id, position_top, line_offset):
        super().__init__(start_position, end_position, key, key_id)
        self.position_top = position_top
        self.line_offset = line_offset