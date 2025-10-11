class MusicScore:
    staves_sequence = [] #combination of all GrandStaves, could also be simple staffs
    top_left_position = None   
    staff_color = None
    key_signature_list = None
    score_width = None
    title = None
    title_position = None
    highest_credit_y_offset = None
    credits = [] # array of text blocks to be added to the top of score apart from title.
    raw_credits = []
    lyrics = []

    def __init__(self, top_left, score_width, title, credits):
        self.top_left_position = top_left
        self.score_width = score_width
        self.title = title
        self.raw_credits = credits # these need processing

    def add_staff(self, staff):
        self.staves_sequence.append(staff)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left   

    def set_score_width(self, score_width):
        self.score_width = score_width

    #def get_lowest_y_credit(self):
        # credits: list of ScoreCredit
        #if not self.credits:
           # return None
        # get min position
        
        #return min(self.credits, key=lambda sc: sc.position.y)

   
  
