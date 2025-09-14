from Models import Interval


class VirtualInterval(Interval):
    position_top = True
    interval_offset = 0

    def __init__(self, position_rect, key, key_id, position_top, interval_offset):
        super().__init__(position_rect, key, key_id)
        self.position_top = position_top
        self.interval_offset = interval_offset