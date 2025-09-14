from numpy.f2py.auxfuncs import throw_error

from Configs.screen_config import VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_TOP
from Models import Interval, Rect
from Models.Line import Line
from Models.Position import Position
from Models.Staff import Staff


class StaffBuilder:
    
    """
        clef: music clef of staff
        time_signature: time signature of staff
        key_signature: key signature of staff
        staff_vertical_padding: the distance at top and bottom of staff where we can add extra notes
        staff_top_left: the top left position of the staff
    """
    def __init__(self):        
        self.lines = []
        self.intervals = []
        self.staff = None

    def init_staff(self, clef, time_signature, key_signature, staff_vertical_padding, staff_top_left, staff_width):
        self.staff = Staff(clef, time_signature, key_signature)
        self.staff_vertical_padding = staff_vertical_padding
        self.staff_top_left = staff_top_left
        self.staff_width = staff_width
        return self

    """ 
        nof_of_lines includes virtual lines
        interval_thickness: is the height of interval between two lines or line spacing
        line_thickness: tickness of each line on staff
        piano_key_details: dictionary containing raw_key: realpiano key e.g. ("E", "E4#")
        original_position: position where we start all lines in this call
        is_virtual: tells if interval is virtual or not
        vertical_positioning: tells if line is above, below (virtual) or on the staff
    """
    def build_lines(self, no_of_lines, interval_thickness, line_thickness, piano_key_details, original_position, is_virtual, vertical_positioning):
        for i in range(no_of_lines):
            line_y = (i * interval_thickness)
            start_position = Position(original_position.x, original_position.y + line_y)
            end_position = Position(original_position.x + self.staff_width, original_position.y + line_y)
            line = Line(start_position, end_position, line_thickness, is_virtual, piano_key_details[i][0], piano_key_details[i][1], vertical_positioning)           
            self.lines.append(line)
        
        return self

    """
        Build intervals based on starting_position. 
        no_of_intervals includes virtual intervals
        interval_thickness: is the height of interval between two lines or line spacing. it's represented by the number of pixes the interval occupies.
            e.g. y_top: 140 - y_bottom: 149. the difference is 9 but as we count from 140, it is 10 pixels thicknes 
        line_thickness: tickness of each line on staff
        piano_key_details: dictionary containing raw_key: realpiano key e.g. ("E", "E4#")
        original_position: position where we start all intervals in this call
        is_virtual: tells if interval is virtual or not
        vertical_positioning: tells if interval is above, below (virtual) or on the staff
    """
    def build_intervals(self, no_of_intervals, interval_thickness, line_thickness, piano_key_details, original_position, is_virtual, vertical_positioning):
        interval_offset = interval_thickness - 1
        cumulative_y_offset = original_position.y - line_thickness

        for i in range(no_of_intervals):                        
            cumulative_y_offset += line_thickness # add 1 because we start the interval on the next pixel below
            position_rect = Rect(Position(original_position.x,  cumulative_y_offset), 
                                 Position(original_position.x + self.staff_width, cumulative_y_offset),
                             Position(original_position.x + self.staff_width, cumulative_y_offset + interval_offset),
                             Position(original_position.x, cumulative_y_offset + interval_offset))
            cumulative_y_offset +=  interval_offset + 1
            interval = Interval(position_rect, piano_key_details[i][0], piano_key_details[i][1], is_virtual, vertical_positioning)           
            self.intervals.append(interval)
        
        return self

    """
        A virtual interval is that holds extra notes above or below the staff.
        This function builds Virtual intervals based on starting_position on a specific staff.        
        interval_thickness: is the height of interval between two lines or line spacing. it's represented by the number of pixes the interval occupies.
            e.g. y_top: 140 - y_bottom: 149. the difference is 9 but as we count from 140, it is 10 pixels thicknes 
        line_thickness: tickness of each line on staff
        piano_key_details: dictionary containing raw_key: realpiano key e.g. ("E", "E4#")
        original_position: position where we start all interval in this call. It must be the top_left of staff or bottom_left of staff based on vertical_positioning
        is_virtual: tells if interval is virtual or not
        vertical_positioning: tells if interval is above, below (virtual) or on the staff
        staff_offset_margins_y: specifies how many pixes we can place virtual lines and intervals above/below staff. for 5 intervals, pass 5 * interval_tickness
    """
    def build_virtual_intervals(self, interval_thickness, line_thickness, piano_key_details, original_position, vertical_positioning, staff_offset_margins_y):
        no_of_intervals = staff_offset_margins_y // interval_thickness
        self.build_intervals(no_of_intervals, interval_thickness, line_thickness, piano_key_details, original_position,
                             True, vertical_positioning)
        
        return self

    """ 
       Builds virtual lines above/below staff based on provided offset.
       interval_thickness: is the height of interval between two lines or line spacing
       line_thickness: thickness of each line on staff
       piano_key_details: dictionary containing raw_key: realpiano key e.g. ("E", "E4#")
       original_position: position where we start all lines in this call
       vertical_positioning: tells if line is above, below (virtual) or on the staff
       staff_offset_margins_y: specifies how many pixes we can place virtual lines and intervals above/below staff. for 5 lines, pass 5 * interval_thickness
    """
    def build_virtual_lines(self, interval_thickness, line_thickness, piano_key_details, original_position, vertical_positioning, staff_offset_margins_y):
        y_offset = StaffBuilder.work_out_offset_y(vertical_positioning, original_position, staff_offset_margins_y)
        no_of_lines = staff_offset_margins_y // interval_thickness
        self.build_lines(no_of_lines, interval_thickness, line_thickness, piano_key_details, Position(original_position.x, y_offset),
                             True, vertical_positioning)

        return self

    @staticmethod
    def work_out_offset_y(vertical_positioning, original_position, staff_offset_margins_y):
        if vertical_positioning == VERTICAL_POSITION_TOP:
            y_offset = original_position.y - staff_offset_margins_y
        elif vertical_positioning == VERTICAL_POSITION_BOTTOM:
            y_offset = original_position.y + staff_offset_margins_y
        else:
            y_offset = 0
            throw_error(f"Invalid vertical_positioning for build_virtual_intervals(): {vertical_positioning}")

        # make sure offset is not negative as this will corrupt calculations. i.e. the offset that is not on the staff
        if y_offset < 0:
            y_offset *= -1

        return y_offset

    """
        We need to reorder our intervals based on their vertical/y positions. Virtual intervals are not displayed on staff.
    """
    def build_staff(self):    
        self.staff.lines = [line for line in self.lines if not line.is_virtual]
        self.staff.virtual_lines = [line for line in self.lines if line.is_virtual]
        self.staff.intervals = [interval for interval in self.intervals if not interval.is_virtual]   
        self.staff.virtual_intervals = [interval for interval in self.intervals if interval.is_virtual]  
    

    """
        Builds staff bounding coordinates.
        We calculate staff boundaries with real lines not virtual ones.
    """
    def set_position(self, all_lines):
        normal_lines = [line for line in all_lines if not line.is_virtual]        
        self.top_line = normal_lines[0]
        self.bottom_line = normal_lines[-1]
        self.position_rect = Rect((self.top_line.start_position.x, self.top_line.start_position.y), (self.top_line.end_position.x, self.top_line.end_position.y),
                                   (self.bottom_line.start_position.x, self.bottom_line.start_position.y), (self.bottom_line.end_position.x, self.bottom_line.end_position.y))       
        self.top_position = self.top_line.start_position
        self.bottom_position = self.bottom_line.start_position
        

    def set_position_attributes(self):
        pass

    