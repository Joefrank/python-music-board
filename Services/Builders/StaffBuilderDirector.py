
from Configs.music_config import TREBLE_CLEF
from Configs.screen_config import VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_ON, VERTICAL_POSITION_TOP, staff_generic_settings
from Models import Rect
from Models.Position import Position
from Services.Builders import StaffBuilder


class StaffBuilderDirector:
    
    def __init__(self):
        self.staff_builder = StaffBuilder()
        self.interval_thickness = staff_generic_settings["STAFF_LINE_GAP"]
        self.line_thickness = staff_generic_settings["STAFF_LINE_THICKNESS"]
        self.staff_spacing = staff_generic_settings["STAFF_SPACING"]
        self.staff_no_lines = staff_generic_settings["STAFF_NO_LINES"]
        self.staff_no_intervals = staff_generic_settings["STAFF_NO_INTERVALS"]
        self.staff_offset_margins_y = staff_generic_settings["STAFF_ALLOWED_MARGIN"]

    def build_staff(self, clef, time_signature, key_signature, staff_original_position, staff_vertical_padding, staff_width):       
        self.staff_builder.init_staff(clef, time_signature, key_signature, staff_vertical_padding, staff_original_position, staff_width)
        # this gives the total number of lines and intervals we can fit in the staff_offset_margins_y
        possible_no_oftop_lines_and_intervals = self.staff_offset_margins_y // (self.interval_thickness + self.line_thickness)
        possible_staff_padding = possible_no_oftop_lines_and_intervals * (self.interval_thickness + self.line_thickness)

        original_position = Position(staff_original_position.x, staff_original_position.y - possible_staff_padding)        
        self.staff_builder.build_virtual_lines(self.interval_thickness, self.line_thickness, piano_key_details, original_position, VERTICAL_POSITION_TOP, possible_staff_padding)
        original_position = Position(original_position.x, original_position.y + self.line_thickness)
        self.staff_builder.build_virtual_intervals(self.interval_thickness, self.line_thickness, piano_key_details, original_position, VERTICAL_POSITION_TOP, possible_staff_padding)        
        original_position = staff_original_position
        self.staff_builder.build_lines(self.staff_no_lines, self.interval_thickness, self.line_thickness, piano_key_details, staff_original_position, False, VERTICAL_POSITION_ON)
        original_position = Position(staff_original_position.x, staff_original_position.y + self.line_thickness) 
        self.staff_builder.build_intervals(self.staff_no_intervals, self.interval_thickness, self.line_thickness, piano_key_details, staff_original_position, False, VERTICAL_POSITION_ON)        
        self.staff_builder.set_position(self.staff_builder.lines) # we can calculate staff boundaries at this stage
        staff_bottom_line = self.staff_builder.staff.bottom_line # we can now use the staff bottom_line     
        original_position = Position(staff_bottom_line.start_position.x, staff_bottom_line.start_position.y + 1) # + 1 because we want to start at the next pixel after the bottom line tickness
        self.staff_builder.build_virtual_intervals(self.interval_thickness, self.line_thickness, piano_key_details, original_position, VERTICAL_POSITION_BOTTOM, possible_staff_padding)
        original_position = Position(staff_bottom_line.start_position.x, staff_bottom_line.start_position.y + self.interval_thickness + 1)
        self.staff_builder.build_virtual_lines(self.interval_thickness, self.line_thickness, piano_key_details, original_position, VERTICAL_POSITION_BOTTOM, possible_staff_padding)