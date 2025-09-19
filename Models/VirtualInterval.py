from Models import Interval


class VirtualInterval(Interval):
    position_top = True
    interval_offset = 0

    def __init__(self, position_rect, key, key_id, position_top, interval_offset, is_virtual, vertical_positioning, staff_index):
        super().__init__(position_rect, key, key_id, is_virtual, vertical_positioning, staff_index)
        self.position_top = position_top
        self.interval_offset = interval_offset
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning