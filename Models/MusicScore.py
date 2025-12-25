class MusicScore:
    TICKS_PER_BEAT = 480
    
    def __init__(self, top_left, score_width, title, credits, tempo=80):        
        self.staves_sequence = [] #combination of all GrandStaves, could also be simple staffs         
        self.staff_color = None
        self.key_signature_list = None
        self.title_position = None
        self.highest_credit_y_offset = None
        self.credits = [] # array of text blocks to be added to the top of score apart from title.        
        self.lyrics = []
        self.top_left_position = top_left
        self.score_width = score_width
        self.title = title
        self.raw_credits = credits # these need processing
        self.tempo = 80  # default tempo
       
   
    """ This duration is to be passed to the mido output for notes timing. """
    def get_duration_in_seconds(self, duration_in_ticks: int) -> float:
        seconds_per_beat = 60 / self.tempo
        seconds_per_tick = seconds_per_beat / self.TICKS_PER_BEAT
        return duration_in_ticks * seconds_per_tick
    
    def add_staff(self, staff):
        self.staves_sequence.append(staff)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left   

    def set_score_width(self, score_width):
        self.score_width = score_width

    def get_all_notes_in_positional_order(self):
        notes = []
        for staff in self.staves_sequence:
            notes.extend(staff.get_notes())
        return sorted(notes, key=lambda note: note.position.x)
    
    def set_tempo(self, tempo: int):
        self.tempo = tempo

    def get_tempo(self) -> int:
        return self.tempo

   
  
