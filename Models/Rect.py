from Models.Position import Position

"""
    This is represents a rectangular surface
"""
class Rect:
    top_left: Position = None
    top_right: Position = None
    bottom_right: Position = None
    bottom_left: Position = None

    def __init__(self, top_left, top_right, bottom_right, bottom_left):
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left