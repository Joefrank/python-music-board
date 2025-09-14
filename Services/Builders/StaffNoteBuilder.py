from itertools import zip_longest
from Configs.music_config import supported_clef_settings, piano_notes
from Configs.screen_config import VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_TOP

class StaffNoteBuilder:

    def __init__(self):
        self.supported_cleff_settings = supported_clef_settings

    """
        staff_offset_count: no of lines and interval (virtual ones) offset from staff
    """
    def build_staff_notes(self, clef, key_signature, staff_offset_count):
        clef_settings = self.supported_cleff_settings[clef]
        notes_per_line = clef_settings["notes_per_line"].reverse() # we reverse this because notes in config are from bottom to top
        notes_per_interval = clef_settings["notes_per_interval"].reverse()
        staff_virtual_top_notes = []
        staff_notes = []
        staff_virtual_bottom_notes = []
        #  [('E5', 'E5'), ('C5', 'C5'), ('A4', 'A4'), ('F4', 'F4#')]
        staff_notes = [item for pair in zip_longest(notes_per_line, notes_per_interval) for item in pair if item is not None]
        staff_virtual_top_notes = self.determine_virtual_notes(staff_notes[0], clef_settings["signature_position_pattern"][key_signature], staff_offset_count, VERTICAL_POSITION_TOP)
        staff_virtual_bottom_notes = self.determine_virtual_notes(staff_notes[-1], clef_settings["signature_position_pattern"][key_signature], staff_offset_count, VERTICAL_POSITION_BOTTOM)
        return staff_virtual_top_notes, staff_notes, staff_virtual_bottom_notes
    
    def determine_virtual_notes(self, start_note, signature_pattern, staff_offset_count, vertical_positioning):
        virtual_notes = []
        if vertical_positioning == VERTICAL_POSITION_TOP: # in this case, we go from top line note and higher
            factor = 1
        elif vertical_positioning == VERTICAL_POSITION_BOTTOM: # we are going towards deeper notes bass
            factor = -1
        else:
            factor = 0 # go nowhere

        for i in range(staff_offset_count):
            start_index = piano_notes.index(start_note)
            next_note = piano_notes[start_index + factor]
            virtual_notes.append(next_note)
