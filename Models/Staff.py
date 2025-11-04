class Staff: 
   
    
    def __init__(self, clef, time_signature, key_signature):       
         # lines and intervals
        self.lines = [] 
        self.intervals = []
        self.virtual_lines = [] # any lines above or below staff
        self.virtual_intervals = [] #any interval above or below staff
         # position attributes
        self.position_rect = None
        self.top_position = None #postion of top line of staff
        self.bottom_position = None #position of bottom line of staff
        self.bottom_line = None # not necessary a line on the staff but how far below you can go with the ledger
        self.top_line = None # not necessary a line on the staff but how far above you can go with the ledger        
        # note boundaries attributes
        self.notes_left_offset = 0 # this is the left boundary for notes on this staff.
        self.notes_right_offset = 0 # this is the right boundary for notes on this staff.
        self.notes_top_offset = 0 # top boundary for notes belonging to this staff
        self.notes_bottom_offset = 0 # bottom boundary for notes belonging to this staff
         # other staff components
        self.modulations = []
        self.bars = []
        self.step_notes_rests_lyrics = []  # these are chords played in steps. It's a list of StaffStep
        self.dynamics = [] # use StaffDynamic as a list
        self.lyrics_lines = []
        # values from constructor parameters
        self.clef = clef
        self.time_signature = time_signature
        self.key_signature = key_signature
      
    def set_notes_boundaries(self, left, top, right, bottom):
        self.notes_left_offset = left
        self.notes_right_offset = right
        self.notes_top_offset = top
        self.notes_bottom_offset = bottom

    def get_width(self):
        return self.top_line.end_position.x - self.top_line.start_position.x
    
    def get_height(self):
        return self.bottom_position.y - self.top_position.y 

    def find_nearest_note(self, position):
        for line in self.lines:
            note = line.find_nearest_note(position)
            if note is not None:
                return note
        for interval in self.intervals:
            note = interval.find_nearest_note(position)
            if note is not None:
                return note
        return None
    
    def get_top_left(self):
        return self.top_position

    def get_bottom_left(self):
        return self.bottom_position
    
    def get_initial_navigator_line(self):
        return (self.get_top_left(), self.get_bottom_left())
    
    def __str__(self):
        lines_str = "-> ".join(str(line) for line in self.lines)
        intervals_str = "-> ".join(str(interval) for interval in self.intervals)
        virtual_lines_str = "-> ".join(str(line) for line in self.virtual_lines)
        virtual_intervals_str = "-> ".join(str(interval) for interval in self.virtual_intervals)

        return (f"clef: {self.clef} - time_signature: {self.time_signature} - key_signature: {self.key_signature} - "
                f"Top:{self.top_position.x, self.top_position.y} - Bottom:{self.bottom_position.x, self.bottom_position.y} -"
                f"\n- lines: [{lines_str}]" 
                f"\n- Virtual lines: [{virtual_lines_str}]" 
                f"\n- intervals: [{intervals_str}]"
                f"\n- Virtual intervals: [{virtual_intervals_str}]")


