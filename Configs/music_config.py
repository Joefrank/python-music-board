MODULATION_SHARP = "SHARP"
MODULATION_FLAT = "FLAT"
TREBLE_CLEF = "TREBLE_CLEF"
BASS_CLEF = "BASS_CLEF"

musical_rests = [
    {"name": "Whole rest", "no_of_beats": 4, "font_code": "\uE4E3"},
    {"name": "Half rest", "no_of_beats": 2, "font_code": "\uE4E4"},
    {"name": "Quarter rest", "no_of_beats": 1, "font_code": "\uE4E5"},
    {"name": "Eighth rest", "no_of_beats": 0.5, "font_code": "\uE4E6"},
    {"name": "Sixteenth rest", "no_of_beats": 0.25, "font_code": "\uE4E7"}
]

valid_note_durations = \
    [ #(duration, note_type font_code, stem-on/off)
        ("1","Whole", "\uE0A2",False),
        ("2","Half", "\uE0A2", True),
        ("4","Quarter","\uE0A4", True),
        ("8","Eighth","\uE0A4", True),
        ("0","Sixteenth","\uE0A4", True)
    ]

default_note_duration = ("4","Quarter","\uE0A4", True)

supported_time_signatures = {
    "2x2":{"fraction" : (2,2), "symbol" : ("\uE082","\uE082")},
    "2x4":{"fraction" : (2,4), "symbol" : ("\uE082","\uE084")},
    "3x2":{"fraction" : (3,2), "symbol" : ("\uE083","\uE082")},
    "3x4":{"fraction" : (3,4), "symbol" : ("\uE083","\uE084")},
    "4x4":{"fraction" : (4,4), "symbol" : ("\uE084","\uE084")},
    "6x8":{"fraction" : (6,8), "symbol" : ("\uE086","\uE088")},
    "9x8":{"fraction" : (9,8), "symbol" : ("\uE089","\uE088")},
    "12x8":{"fraction" : (12,8), "symbol" : ("\uE082","\uE088")}
}

# because the clef is centered around the top of the staff, we want to push it down based on where it's center is
supported_clef_settings = {
    TREBLE_CLEF : { # for treble, center is around the center of the circle
        "size" : 40,
        "font_code": "\uE050",
        "margins":(0,40,0,10),
        "notes_per_line":("E4","G4","B4","D5","F5"), # this depends on key signature.
        "notes_per_interval":("F4","A4","C5","E5"),
        "signature_position_pattern": {
            "C": [],
            "G": [{"F":(0,1)}],
            "D": [{"F":(0,1)}, {"C":(1,2)}],
            "A": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}],
            "E": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}, {"D":(0,2)}],
            "B": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}, {"D":(0,2)}, {"A":(1,3)}],
            "F#": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}, {"D":(0,2)}, {"A":(1,3)}, {"E":(1,1)}],
            "C#": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}, {"D":(0,2)}, {"A":(1,3)}, {"E":(1,1)},{"B":(0,3)}],
            "F":  [{"B":(0,3)}],
            "Bb":  [{"B":(0,3)},{"E":(1,1)}],
            "Eb":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)}],
            "Ab":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)},{"D":(0,2)}],
            "Db":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)},{"D":(0,2)},{"G":(0,4)}],
            "Gb":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)},{"D":(0,2)},{"G":(0,4)},{"C":(1,2)}],
            "Cb":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)},{"D":(0,2)},{"G":(0,4)},{"C":(1,2)},{"F":(1,4)}]
        }
    },
    BASS_CLEF : {  # for bass, center is around the big dot
        "size" : 40,
        "font_code": "\uE062",
        "margins":(0,10,0,0),
        "notes_per_line":("G2","B2","D3","F3","A3"),
        "notes_per_interval":("A2","C3","E3","G3"),
        "signature_position_pattern": {
            "C": [],
            "G": [{"F":(0,2)}], # 0 is for line, 1 is interval. in this case (0,2) => (line, index 2) 
            "D": [{"F":(0,2)}, {"C":(1,3)}], # (1,3) means 3rd interval
            "A": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}],
            "E": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}, {"D":(0,3)}],
            "B": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}, {"D":(0,3)}, {"A":(1,4)}],
            "F#": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}, {"D":(0,3)}, {"A":(1,4)}, {"E":(1,2)}],
            "C#": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}, {"D":(0,3)}, {"A":(1,4)}, {"E":(1,2)},{"B":(0,4)}],
            "F":  [{"B":(0,4)}],
            "Bb":  [{"B":(0,4)},{"E":(1,2)}],
            "Eb":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)}],
            "Ab":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)},{"D":(0,3)}],
            "Db":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)},{"D":(0,3)},{"G":(0,5)}],
            "Gb":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)},{"D":(0,3)},{"G":(0,5)},{"C":(1,3)}],
            "Cb":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)},{"D":(0,3)},{"G":(0,5)},{"C":(1,3)},{"F":(1,5)}]
        }
    }
}



supported_modulations = {
    MODULATION_SHARP: {"font_code": "\uE262", "key_signatures": ("C", "G", "D", "A", "E", "B", "F#", "C#")},
    MODULATION_FLAT: {"font_code": "\uE260", "key_signatures": ("F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb")}
}

supported_time_signatures = {
    "2x2":{"fraction" : (2,2), "symbol" : ("\uE082","\uE082")},
    "2x4":{"fraction" : (2,4), "symbol" : ("\uE082","\uE084")},
    "3x2":{"fraction" : (3,2), "symbol" : ("\uE083","\uE082")},
    "3x4":{"fraction" : (3,4), "symbol" : ("\uE083","\uE084")},
    "4x4":{"fraction" : (4,4), "symbol" : ("\uE084","\uE084")},
    "6x8":{"fraction" : (6,8), "symbol" : ("\uE086","\uE088")},
    "9x8":{"fraction" : (9,8), "symbol" : ("\uE089","\uE088")},
    "12x8":{"fraction" : (12,8), "symbol" : ("\uE082","\uE088")}
}

lowest_note_code = 21 # midi number for lowest A note (first note on the left of 88-keys piano)
middle_c_code = 60 # midi note number for middle C 'C4'. index = 39

piano_notes = ['A0', 'A0#', 'B0', 'C1', 'C1#', 'D1', 'D1#', 'E1', 'F1', 'F1#', 'G1', 'G1#',
               'A1', 'A1#', 'B1', 'C2', 'C2#', 'D2', 'D2#', 'E2', 'F2', 'F2#', 'G2', 'G2#',
               'A2', 'A2#', 'B2', 'C3', 'C3#', 'D3', 'D3#', 'E3', 'F3', 'F3#', 'G3', 'G3#',
               'A3', 'A3#', 'B3', 'C4', 'C4#', 'D4', 'D4#', 'E4', 'F4', 'F4#', 'G4', 'G4#',
               'A4', 'A4#', 'B4', 'C5', 'C5#', 'D5', 'D5#', 'E5', 'F5', 'F5#', 'G5', 'G5#',
               'A5', 'A5#', 'B5', 'C6', 'C6#', 'D6', 'D6#', 'E6', 'F6', 'F6#', 'G6', 'G6#',
               'A6', 'A6#', 'B6', 'C7', 'C7#', 'D7', 'D7#', 'E7', 'F7', 'F7#', 'G7', 'G7#',
               'A7', 'A7#', 'B7', 'C8']

white_labels= ['A0', 'B0', 'C1', 'D1', 'E1', 'F1', 'G1',
               'A1', 'B1', 'C2', 'D2', 'E2', 'F2', 'G2',
               'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3',
               'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4',
               'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5',
               'A5', 'B5', 'C6', 'D6', 'E6', 'F6', 'G6',
               'A6', 'B6', 'C7', 'D7', 'E7', 'F7', 'G7',
               'A7', 'B7', 'C8']

black_labels = ['A0#', 'C1#', 'D1#', 'F1#', 'G1#',
                'A1#', 'C2#', 'D2#', 'F2#', 'G2#',
                'A2#', 'C3#', 'D3#', 'F3#', 'G3#',
                'A3#', 'C4#', 'D4#', 'F4#', 'G4#',
                'A4#', 'C5#', 'D5#', 'F5#', 'G5#',
                'A5#', 'C6#', 'D6#', 'F6#', 'G6#',
                'A6#', 'C7#', 'D7#', 'F7#', 'G7#',
                'A7#']

black_labels_flats = ['B0b', 'D1b', 'E1b', 'G1b', 'A1b',
                'B1b', 'D2b', 'E2b', 'G2b', 'A2b',
                'B2b', 'D3b', 'E3b', 'G3b', 'A3b',
                'B3b', 'D4b', 'E4b', 'G4b', 'A4b',
                'B4b', 'D5b', 'E5b', 'G5b', 'A5b',
                'B5b', 'D6b', 'E6b', 'G6b', 'A6b',
                'B6b', 'D7b', 'E7b', 'G7b', 'A7b',
                'B7b']