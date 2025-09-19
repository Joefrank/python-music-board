

class Position:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    """
        Compares this point with another to see if they are the same.
    """
    def is_same_as(self, position):
        return position.x == self.x and position.y == self.y
    
    """ 
        Determines if this position is on a horizontal or vertical line.
        This works for straight lines only. which is what we use on a staff.
    """
    def is_on_line(self, line):
        return (
            (line.start_position.x == self.x and line.end_position.x == line.start_position.x)
            or line.start_position.y == self.y and line.start_position.y == line.end_position.y)
    
    """
        Determines if a given position lies within a rectangle.
    """
    def is_within_rectangle(self, rectangle):
        return(
            (rectangle.top_left.x <= self.x <= rectangle.top_right.x)
            and (rectangle.top_left.y <= self.y <= rectangle.bottom_right.y)
        )
    
    """
        Determines if a given position belongs to a specific interval.
    """
    def belongs_to_interval(self, interval):
        return self.is_within_rectangle(interval.position_rect)

    def __str__(self):
        return f"Position:({self.x},{self.y})"