
from Configs.screen_config import (VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_ON, VERTICAL_POSITION_TOP)
from Models.Position import Position
from Services.Builders import StaffBuilder
from Services.Builders.StaffNoteBuilder import StaffNoteBuilder


class StaffBuilderDirector:
    
    def __init__(self):
        self.staff_builder = StaffBuilder()
        self.staff_note_builder = StaffNoteBuilder()
        self.interval_thickness = None
        self.line_thickness = None
        self.staff_spacing = None
        self.staff_no_lines = None
        self.staff_no_intervals = None
        self.staff_offset_margins_y = None

    @staticmethod
    def calculate_first_staff_position(window_width, staff_width_percentage, staff_original_y_offset):
        staff_with = window_width * staff_width_percentage / 100
        all_staves_x_offset = (window_width - staff_with) // 2
        return staff_with, Position(all_staves_x_offset, staff_original_y_offset)

    def build_staff(self, clef, time_signature, key_signature, staff_original_position, staff_vertical_padding,
                    staff_width, interval_thickness, line_thickness, staff_spacing, staff_no_lines, staff_no_intervals):
        self.interval_thickness = interval_thickness
        self.staff_offset_margins_y = staff_vertical_padding
        self.line_thickness = line_thickness
        self.staff_spacing = staff_spacing
        self.staff_no_lines = staff_no_lines
        self.staff_no_intervals = staff_no_intervals

        possible_no_oftop_lines_and_intervals = self.staff_offset_margins_y // (
                    self.interval_thickness + self.line_thickness)
        possible_staff_padding = possible_no_oftop_lines_and_intervals * (self.interval_thickness + self.line_thickness)
        # Initialize the staff
        self.staff_builder.init_staff(clef, time_signature, key_signature, staff_vertical_padding, staff_original_position, staff_width)
        # Build music notes for staff and padding areas
        staff_note_items, staff_note_top_items, staff_note_bottom_item = self.staff_note_builder.build_staff_notes(clef, key_signature, possible_no_oftop_lines_and_intervals)

        # this gives the total number of lines and intervals we can fit in the staff_offset_margins_y
        # Build all lines and intervals above the staff
        #print(f"position y: {staff_original_position.y} - possible_staff_padding: {possible_staff_padding} - possible_no_oftop_lines_and_intervals: {possible_no_oftop_lines_and_intervals}")
        original_position = Position(staff_original_position.x, staff_original_position.y - possible_staff_padding)        
        #print(f"original_position VL-top: {original_position.x, original_position.y}")
        self.staff_builder.build_virtual_lines(self.interval_thickness, self.line_thickness, staff_note_top_items[1], original_position,
                                               VERTICAL_POSITION_TOP, possible_staff_padding, possible_no_oftop_lines_and_intervals)
        original_position = Position(original_position.x, original_position.y + self.line_thickness)
        #print(f"original_position VI-top: {original_position.x, original_position.y}")
        self.staff_builder.build_virtual_intervals(self.interval_thickness, self.line_thickness, staff_note_top_items[0], original_position,
                                                   VERTICAL_POSITION_TOP, possible_no_oftop_lines_and_intervals)
        # Build all lines and intervals on staff
        original_position = staff_original_position
        #print(f"original_position Lines: {original_position.x, original_position.y}")
        self.staff_builder.build_lines(self.staff_no_lines, self.interval_thickness, self.line_thickness, staff_note_items[1], original_position, False, VERTICAL_POSITION_ON)
        original_position = Position(staff_original_position.x, staff_original_position.y + self.line_thickness)
       # print(f"original_position Intervals: {original_position.x, original_position.y}")
        self.staff_builder.build_intervals(self.staff_no_intervals, self.interval_thickness, self.line_thickness, staff_note_items[0], original_position, False, VERTICAL_POSITION_ON)
        self.staff_builder.set_position() # we can calculate staff boundaries at this stage

        # Build all lines and intervals below the staff
        staff_bottom_line = self.staff_builder.staff.bottom_line # we can now use the staff bottom_line
        original_position = Position(staff_bottom_line.start_position.x, staff_bottom_line.start_position.y + 1) # + 1 because we want to start at the next pixel after the bottom line thickness
        #print(f"original_position VI-bottom: {original_position.x, original_position.y}")
        self.staff_builder.build_virtual_intervals(self.interval_thickness, self.line_thickness, staff_note_bottom_item[0], original_position, VERTICAL_POSITION_BOTTOM, possible_no_oftop_lines_and_intervals)
        original_position = Position(staff_bottom_line.start_position.x, staff_bottom_line.start_position.y + self.interval_thickness + 1)
       # print(f"original_position VL-bottom: {original_position.x, original_position.y}")
        self.staff_builder.build_virtual_lines(self.interval_thickness, self.line_thickness, staff_note_bottom_item[1], original_position, VERTICAL_POSITION_BOTTOM, possible_staff_padding, possible_no_oftop_lines_and_intervals)

        return self.staff_builder.build_staff()