class Staff:
    # lines and intervals
    lines = []
    intervals = []
    virtual_lines = []
    virtual_intervals = []

    # position attributes
    position_rect = None
    top_position = None #postion of top line of staff
    bottom_position = None #position of bottom line of staff
    bottom_line = None # not necessary a line on the staff but how far below you can go with the ledger
    top_line = None # not necessary a line on the staff but how far above you can go with the ledger
    
    # note boundaries attributes
    notes_left_offset = 0 # this is the left boundary for notes on this staff.
    notes_right_offset = 0 # this is the right boundary for notes on this staff.
    notes_top_offset = 0 # top boundary for notes belonging to this staff
    notes_bottom_offset = 0 # bottom boundary for notes belonging to this staff

    # other staff components
    modulations = []
    bars = []
    step_notes_rests_lyrics = []  # these are chords played in steps. It's a list of StaffStep
    dynamics = [] # use StaffDynamic as a list
    lyrics_lines = []
    clef = None
    time_signature = None
    key_signature = None
    
    def __init__(self, clef, time_signature, key_signature):
        self.clef = clef
        self.time_signature = time_signature
        self.key_signature = key_signature  

    def set_notes_boundaries(self, left, top, right, bottom):
        self.notes_left_offset = left
        self.notes_right_offset = right
        self.notes_top_offset = top
        self.notes_bottom_offset = bottom


