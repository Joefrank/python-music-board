import unittest

from Configs.music_config import piano_notes_sharps, piano_notes_flats


class KeySignaturePatternsGeneratorTests(unittest.TestCase):

    def test_note_pattern_generation_with_sharp(self):
        special_prefixes = ("F", "C", "G", "D", "A", "E", "B")

        resulting_notes = [
            (i, s) for i, s in enumerate(piano_notes_sharps)
            if ("#" not in s and not s.startswith(special_prefixes))
               or (s.startswith(special_prefixes) and "#" in s)
        ]

        # Separate into indexes and values
        result_indexes = [i for i, _ in resulting_notes]
        result_strings = [s for _, s in resulting_notes]

        print("Indexes:", result_indexes)
        print("Strings:", result_strings)
        print("----------------------------------------------------------------------------------")

    def test_note_pattern_generation_with_flat(self):
        special_prefixes = ("B", "E", "A", "D", "G", "C", "F")

        resulting_notes = [
            (i, s) for i, s in enumerate(piano_notes_flats)
            if ("b" not in s and not s.startswith(special_prefixes))
               or (s.startswith(special_prefixes) and "b" in s)
        ]

        # Separate into indexes and values
        result_indexes = [i for i, _ in resulting_notes]
        result_strings = [s for _, s in resulting_notes]

        print("Indexes:", result_indexes)
        print("Strings:", result_strings)
        print("----------------------------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()