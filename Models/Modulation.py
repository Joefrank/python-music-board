from AIPiano.Models.Position import Position


class Modulation:
    key = None
    position = Position(0,0)
    staff_item = None

    def __init__(self, key, position, staff_item):
        self.key = key
        self.position = position
        self.staff_item = staff_item