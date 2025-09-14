class MusicScore:
    staves_sequence = [] #combination of all GrandStaves, could also be simple staffs
    top_left_position = None
    bottom_right_position = None # this gets set after all calculations
    staff_color = None
    key_signature_list = None
    score_width = None
    score_height = None
    title = None
    credits = [] # array of text blocks to be added to the top of score apart from title.
    lyrics = []

    def __init__(self, top_left, score_width):
        self.top_left_position = top_left
        self.score_width = score_width

    def add_staff(self, staff):
        self.staves_sequence.append(staff)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left

    def set_bottom_right_position(self, bottom_right):
        self.bottom_right_position = bottom_right

    def set_score_width(self, score_width):
        self.score_width = score_width

    def set_score_height(self, score_height):
        self.score_height = score_height

   
  
