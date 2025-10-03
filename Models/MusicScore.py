class MusicScore:
    staves_sequence = [] #combination of all GrandStaves, could also be simple staffs
    top_left_position = None   
    staff_color = None
    key_signature_list = None
    score_width = None
    title = None
    credits = [] # array of text blocks to be added to the top of score apart from title.
    lyrics = []

    def __init__(self, top_left, score_width, title, credits):
        self.top_left_position = top_left
        self.score_width = score_width
        self.title = title
        self.credits = credits

    def add_staff(self, staff):
        self.staves_sequence.append(staff)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left   

    def set_score_width(self, score_width):
        self.score_width = score_width


   
  
