from itertools import zip_longest
from Configs.music_config import (supported_clef_settings, piano_notes_sharps, supported_modulations,
                                  MODULATION_SHARP, MODULATION_FLAT, piano_notes_key_patterns, piano_notes_flats)
from Configs.screen_config import VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_TOP

class StaffNoteBuilder:

    def __init__(self):
        self.supported_clef_settings = supported_clef_settings

    """
        staff_offset_count: no of lines and interval (virtual ones) offset from staff
    """
    def build_staff_notes(self, clef, key_signature, staff_offset_count):
        clef_settings = self.supported_clef_settings[clef]
        amplitude_for_lines_and_intervals = staff_offset_count * 2
        modulation_type = next(
            (name for name, details in supported_modulations.items() if key_signature in details["key_signatures"]),
            None
        )
        notes_per_line = self.modulate_staff_notes(clef_settings["notes_per_line"], clef, key_signature, modulation_type)
        notes_per_interval = self.modulate_staff_notes(clef_settings["notes_per_interval"], clef, key_signature, modulation_type)
        interval_notes_top, line_notes_top = self.modulate_virtual_notes(clef, notes_per_line[-1], amplitude_for_lines_and_intervals,  key_signature,  VERTICAL_POSITION_TOP, modulation_type)
        interval_notes_bottom, line_notes_bottom = self.modulate_virtual_notes(clef, notes_per_line[0], amplitude_for_lines_and_intervals, key_signature, VERTICAL_POSITION_BOTTOM, modulation_type)
        return (notes_per_interval, notes_per_line), (interval_notes_top, line_notes_top), (interval_notes_bottom, line_notes_bottom)

    def modulate_staff_notes(self, notes, clef, key_signature, modulation_type):
        modulations = self.supported_clef_settings[clef]["signature_position_pattern"][key_signature]
        modulated_notes = [list(d.keys())[0] for d in modulations]
        resulting_notes = []

        for note in notes:
            if note[0] in modulated_notes:
                if modulation_type == MODULATION_SHARP: # modulate note
                    new_note = f"{note}#"
                elif modulation_type == MODULATION_FLAT:
                    new_note = f"{note}b"
                else:
                    new_note = note
                resulting_notes.append(new_note)
            else:
                resulting_notes.append(note)
        return resulting_notes

    """
        start_note: note on staff from which we start generating virtual notes 
        modulation_amplitude: number of virtual lines and intervals we are generating around staff vertical padding 
        key_signature: key signature of the staff
        vertical_positioning: top or bottom of staff where we generate virtual notes
        modulation_type: SHARP or FLAT
    """
    def modulate_virtual_notes(self, clef, start_note, modulation_amplitude, key_signature, vertical_positioning,
                               modulation_type):
        key_pattern = piano_notes_key_patterns[modulation_type][key_signature]

        if modulation_type == MODULATION_SHARP:  # modulate note
            all_notes = piano_notes_sharps
        elif modulation_type == MODULATION_FLAT:
            all_notes = piano_notes_flats
        else:
            all_notes = None

        if all_notes is None:
            return None, None

        if vertical_positioning == VERTICAL_POSITION_TOP: # in this case, we go from top line note and higher
            factor = 1
        elif vertical_positioning == VERTICAL_POSITION_BOTTOM: # we are going towards deeper notes bass
            factor = -1
        else:
            factor = 0 # go nowhere

        try:
            start_note_index = all_notes.index(start_note) # index in overall notes array.
            start_index_in_pattern = key_pattern.index(start_note_index) # find that index in pattern it must be there
            end_point = start_index_in_pattern + (factor * modulation_amplitude)

            if end_point > start_index_in_pattern:
                start_point = start_index_in_pattern + 1
                end_point += 1
            else:
                start_point = end_point
                end_point = start_index_in_pattern

            pattern_index_chunk = key_pattern[start_point: end_point]
            virtual_notes = [all_notes[i] for i in pattern_index_chunk]
            interval_notes = virtual_notes[::2]  # step = 2, starting at index 0
            line_notes = virtual_notes[1::2]  # step = 2, starting at index 1
            return interval_notes, line_notes

        except ValueError:
            print(f"not found in list")

        return None, None



