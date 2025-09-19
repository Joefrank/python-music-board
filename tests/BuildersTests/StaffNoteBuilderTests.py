from Configs import VERTICAL_POSITION_BOTTOM
from Configs.screen_config import VERTICAL_POSITION_TOP
from Configs.screen_config import VERTICAL_POSITION_ON
from Models.Position import Position
from Services.Builders.StaffNoteBuilder import StaffNoteBuilder
import unittest


class StaffNoteBuilderTests(unittest.TestCase):

    def test_build_lines(self):
        # Arrange
        staff_offset_count = 5

        # Act
        staff_note_builder = StaffNoteBuilder()
        staff_line_and_interval_notes, staff_line_and_interval_notes_top, staff_line_and_interval_notes_bottom = (
            staff_note_builder.build_staff_notes("TREBLE_CLEF", "G", staff_offset_count))

        # Assert
        self.assertEqual(len(staff_line_and_interval_notes[0]), staff_offset_count - 1) # on the staff there are only 4 intervals
        self.assertEqual(len(staff_line_and_interval_notes[1]), staff_offset_count)
        self.assertEqual(len(staff_line_and_interval_notes_top[0]), staff_offset_count)
        self.assertEqual(len(staff_line_and_interval_notes_top[1]), staff_offset_count)
        self.assertEqual(len(staff_line_and_interval_notes_bottom[0]), staff_offset_count)
        self.assertEqual(len(staff_line_and_interval_notes_bottom[1]), staff_offset_count)

        # test start and end positions



if __name__ == '__main__':
    unittest.main()