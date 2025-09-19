from Configs import VERTICAL_POSITION_BOTTOM
from Configs.screen_config import VERTICAL_POSITION_TOP
from Configs.screen_config import VERTICAL_POSITION_ON
from Models.Position import Position
from Services.Builders.StaffBuilder import StaffBuilder
import unittest

class TestStaffBuilder(unittest.TestCase):

    def test_build_lines(self):
        # Arrange
        staff_no_lines = 5
        staff_left_top = Position(60, 140) # this is starting position
        piano_ley_details = [('F5','F5#'),('D5','D5'),('B4','B4'),('G4','G4'),('E4', 'E4')]
        line_thickness = 1
        interval_thickness = 10
        is_virtual = False
        staff_offset_margins_y = 50

        # Act
        staff_builder = StaffBuilder()
        staff_builder.init_staff("TREBLE_CLEF", "6x8", "G", staff_offset_margins_y, staff_left_top, 1100)
        staff_builder.build_lines(staff_no_lines, interval_thickness, line_thickness, piano_ley_details, staff_left_top, is_virtual, VERTICAL_POSITION_ON)

        # Assert
        self.assertEqual(len(staff_builder.lines), staff_no_lines)
        # check keys are saved correctly on line
        for i in range(staff_no_lines):
            self.assertEqual(staff_builder.lines[i].key, piano_ley_details[i][0])
            self.assertEqual(staff_builder.lines[i].key_id, piano_ley_details[i][1])  
            # check spacing between lines
            if i < staff_no_lines - 2:
                line1 = staff_builder.lines[i]
                line2 = staff_builder.lines[i+1]   
                self.assertEqual(line2.start_position.y - line1.start_position.y, interval_thickness)
                self.assertEqual(line2.end_position.y - line1.end_position.y, interval_thickness)

        # test start and end positions
        self.assertEqual(staff_builder.lines[0].start_position.x, staff_left_top.x)
        self.assertEqual(staff_builder.lines[0].start_position.y, staff_left_top.y)
        # test is virtual works. they should all have true as set above in build_lines()
        self.assertTrue(all(not line.is_virtual for line in staff_builder.lines))
        # test vertical_positioning
        self.assertTrue(all(line.vertical_positioning == VERTICAL_POSITION_ON for line in staff_builder.lines))
        # check thickness
        self.assertTrue(all(line.thickness == line_thickness for line in staff_builder.lines))

    def test_build_top_virtual_lines(self):
        # Arrange        
        staff_left_top = Position(60, 140) # this is starting position
        piano_ley_details = [('B6','B6'),('G6','G6'),('E6','E6'),('C6', 'C6'),('A5','A5')]
        line_thickness = 1
        interval_thickness = 10
        is_virtual = True
        staff_offset_margins_y = 50
        staff_no_lines = staff_offset_margins_y // interval_thickness
        # Start building virtual lines at the offset above the staff staff_offset_margins_y
        start_position = Position(staff_left_top.x, staff_left_top.y - staff_offset_margins_y)
        
        # Act
        staff_builder = StaffBuilder()        
        staff_builder.init_staff("TREBLE_CLEF", "6x8", "G", staff_offset_margins_y, staff_left_top, 1100)
        staff_builder.build_lines(staff_no_lines, interval_thickness, line_thickness, piano_ley_details, start_position, is_virtual, VERTICAL_POSITION_TOP)
        
        # Assert
        self.assertEqual(len(staff_builder.lines), staff_no_lines)
        # check keys are saved correctly on line
        for i in range(staff_no_lines):
            self.assertEqual(staff_builder.lines[i].key, piano_ley_details[i][0])
            self.assertEqual(staff_builder.lines[i].key_id, piano_ley_details[i][1])  
            # check spacing between lines
            if i < staff_no_lines - 2:
                line1 = staff_builder.lines[i]
                line2 = staff_builder.lines[i+1]   
                self.assertEqual(line2.start_position.y - line1.start_position.y, interval_thickness)
                self.assertEqual(line2.end_position.y - line1.end_position.y, interval_thickness)

        # test start and end positions
        self.assertEqual(staff_builder.lines[0].start_position.x, start_position.x)
        self.assertEqual(staff_builder.lines[0].start_position.y, start_position.y)
        # test is virtual works. they should all have true as set above in build_lines()
        self.assertTrue(all(line.is_virtual for line in staff_builder.lines))
        # test vertical_positioning
        self.assertTrue(all(line.vertical_positioning == VERTICAL_POSITION_TOP for line in staff_builder.lines))
        # check thickness
        self.assertTrue(all(line.thickness == line_thickness for line in staff_builder.lines))
       
    def test_build_bottom_virtual_lines(self):
        # Arrange    
        staff_left_top = Position(60, 140) # this is starting position    
        staff_bottom_left = Position(60, 190) # this is starting position
        piano_ley_details = [('C4','C4'),('A3','A3'),('F3','F3#'),('D3', 'D3'),('B2','B2')]
        line_thickness = 1
        interval_thickness = 10
        is_virtual = True
        staff_offset_margins_y = 50
        staff_no_lines = staff_offset_margins_y // interval_thickness
        # Start building virtual lines at the bottom line + 1 interval_thickness offset
        start_position = Position(staff_bottom_left.x, staff_bottom_left.y + interval_thickness)
        
        # Act
        staff_builder = StaffBuilder()   
        staff_builder.init_staff("TREBLE_CLEF", "6x8", "G", staff_offset_margins_y, staff_left_top, 1100)     
        staff_builder.build_lines(staff_no_lines, interval_thickness, line_thickness, piano_ley_details, start_position, is_virtual, VERTICAL_POSITION_BOTTOM)
        
        # Assert
        self.assertEqual(len(staff_builder.lines), staff_no_lines)
        # check keys are saved correctly on line
        for i in range(staff_no_lines):
            self.assertEqual(staff_builder.lines[i].key, piano_ley_details[i][0])
            self.assertEqual(staff_builder.lines[i].key_id, piano_ley_details[i][1])  
            # check spacing between lines
            if i < staff_no_lines - 2:
                line1 = staff_builder.lines[i]
                line2 = staff_builder.lines[i+1]   
                self.assertEqual(line2.start_position.y - line1.start_position.y, interval_thickness)
                self.assertEqual(line2.end_position.y - line1.end_position.y, interval_thickness)

        # test start and end positions
        self.assertEqual(staff_builder.lines[0].start_position.x, start_position.x)
        self.assertEqual(staff_builder.lines[0].start_position.y, start_position.y)
        # test is virtual works. they should all have true as set above in build_lines()
        self.assertTrue(all(line.is_virtual for line in staff_builder.lines))
        # test vertical_positioning
        self.assertTrue(all(line.vertical_positioning == VERTICAL_POSITION_BOTTOM for line in staff_builder.lines))
        # check thickness
        self.assertTrue(all(line.thickness == line_thickness for line in staff_builder.lines))

    def test_build_intervals(self):
        # Arrange
        staff_no_intervals = 4
        staff_left_top = Position(60, 140)
        piano_ley_details = [('E5', 'E5'), ('C5', 'C5'), ('A4', 'A4'), ('F4', 'F4#')]
        line_thickness = 1
        interval_thickness = 10
        is_virtual = False
        staff_offset_margins_y = 50
        
        ## Act
        staff_builder = StaffBuilder()
        staff_builder.init_staff("TREBLE_CLEF", "6x8", "G", staff_offset_margins_y, staff_left_top, 1100) 
        staff_builder.build_intervals(staff_no_intervals, interval_thickness, line_thickness, piano_ley_details,
                                      staff_left_top, is_virtual, VERTICAL_POSITION_ON)
        intervals = staff_builder.intervals

        ## Assert
        self.assertEqual(len(intervals), staff_no_intervals)
        # check keys are saved correctly on interval
        for i in range(staff_no_intervals):
            self.assertEqual(intervals[i].key, piano_ley_details[i][0])
            self.assertEqual(intervals[i].key_id, piano_ley_details[i][1])
            # check spacing between intervals is equal to line thickness
            if i > 0:
                previous_interval = intervals[i - 1]
                current_interval = intervals[i]
                self.assertEqual(
                    current_interval.position_rect.bottom_left.y - previous_interval.position_rect.bottom_left.y,
                    interval_thickness + line_thickness)
                self.assertEqual(
                    current_interval.position_rect.top_left.y - previous_interval.position_rect.bottom_left.y,
                    line_thickness + 1)

        # test start and end positions
        self.assertEqual(intervals[0].position_rect.top_left.x, staff_left_top.x)
        self.assertEqual(intervals[0].position_rect.top_left.y, staff_left_top.y)
        # test is virtual works. they should all have true as set above in build_lines()
        self.assertTrue(all(not interval.is_virtual for interval in staff_builder.intervals))
        # test vertical_positioning
        self.assertTrue(
            all(interval.vertical_positioning == VERTICAL_POSITION_ON for interval in staff_builder.intervals))
        # check thickness
        self.assertTrue(all(interval.get_tickness() == interval_thickness for interval in staff_builder.intervals))

    #### test that your intervals are lined up from the starting position to the offset
    def test_build_virtual_top_intervals(self):
        # Arrange
        staff_left_top = Position(60, 140)
        piano_ley_details = [('A6', 'A6'), ('F6', 'F6#'), ('D6', 'D6'), ('B5', 'B5'), ('G5', 'G5')]
        line_thickness = 1
        interval_thickness = 10
        staff_offset_margins_y = 50
        staff_no_intervals = staff_offset_margins_y // interval_thickness
        # because we are starting on top of staff, we need to start from the offset at the margin set for notes.
        start_position = Position(staff_left_top.x, staff_left_top.y - staff_offset_margins_y)

        ## Act
        staff_builder = StaffBuilder()
        staff_builder.init_staff("TREBLE_CLEF", "6x8", "G", staff_offset_margins_y, staff_left_top, 1100)
        staff_builder.build_virtual_intervals(interval_thickness, line_thickness, piano_ley_details, start_position,
                                              VERTICAL_POSITION_TOP, staff_offset_margins_y)
        intervals = staff_builder.intervals

        ## Assert
        self.assertEqual(len(intervals), staff_no_intervals)
        # check keys are saved correctly on interval
        for i in range(staff_no_intervals):
            self.assertEqual(intervals[i].key, piano_ley_details[i][0])
            self.assertEqual(intervals[i].key_id, piano_ley_details[i][1])
            # check spacing between intervals is equal to line thickness
            if i > 0:
                previous_interval = intervals[i - 1]
                current_interval = intervals[i]
                self.assertEqual(
                    current_interval.position_rect.bottom_left.y - previous_interval.position_rect.bottom_left.y,
                    interval_thickness + line_thickness)
                self.assertEqual(
                    current_interval.position_rect.top_left.y - previous_interval.position_rect.bottom_left.y,
                    line_thickness + 1)

        # test start and end positions
        self.assertEqual(intervals[0].position_rect.top_left.x, staff_left_top.x)
        self.assertEqual(intervals[0].position_rect.top_left.y, staff_left_top.y - staff_offset_margins_y)
        # test is virtual works. they should all have true as set above in build_lines()
        self.assertTrue(all(interval.is_virtual for interval in staff_builder.intervals))
        # test vertical_positioning
        self.assertTrue(
            all(interval.vertical_positioning == VERTICAL_POSITION_TOP for interval in staff_builder.intervals))
        # check thickness
        self.assertTrue(all(interval.get_tickness() == interval_thickness for interval in staff_builder.intervals))

    def test_build_virtual_bottom_intervals(self):
         # Arrange
        staff_left_top = Position(60, 140)
        staff_bottom_left = Position(60, 185)
        piano_key_details = [('D4','D4'),('B3','B3'),('G3','G3'),('E3','E3'),('C3','C3')]
        line_thickness = 1
        interval_thickness = 10
        staff_offset_margins_y = 50
        staff_no_intervals = staff_offset_margins_y // interval_thickness

        ## Act
        staff_builder = StaffBuilder()
        staff_builder.init_staff("TREBLE_CLEF", "6x8", "G", staff_offset_margins_y, staff_left_top, 1100)
        staff_builder.intervals.clear()
        staff_builder.build_virtual_intervals(interval_thickness, line_thickness, piano_key_details, staff_bottom_left, VERTICAL_POSITION_BOTTOM, staff_offset_margins_y)
        intervals = staff_builder.intervals

        ## Assert
        self.assertEqual(len(intervals), staff_no_intervals)
        # check keys are saved correctly on interval
        for i in range(staff_no_intervals):
            self.assertEqual(intervals[i].key, piano_key_details[i][0])
            self.assertEqual(intervals[i].key_id, piano_key_details[i][1])
            # check spacing between intervals is equal to line thickness
            if i > 0:
                previous_interval = intervals[i-1]
                current_interval = intervals[i]
                self.assertEqual(current_interval.position_rect.bottom_left.y - previous_interval.position_rect.bottom_left.y, interval_thickness + line_thickness)
                self.assertEqual(current_interval.position_rect.top_left.y - previous_interval.position_rect.bottom_left.y, line_thickness + 1)

        # test start and end positions
        self.assertEqual(intervals[0].position_rect.top_left.x, staff_bottom_left.x)
        self.assertEqual(intervals[0].position_rect.top_left.y, staff_bottom_left.y)
        # test is virtual works. they should all have true as set above in build_lines()
        self.assertTrue(all(interval.is_virtual for interval in staff_builder.intervals))
        # test vertical_positioning
        self.assertTrue(all(interval.vertical_positioning == VERTICAL_POSITION_BOTTOM for interval in staff_builder.intervals))
        # check thickness
        self.assertTrue(all(interval.get_tickness() == interval_thickness for interval in staff_builder.intervals))


if __name__ == '__main__':
    unittest.main()