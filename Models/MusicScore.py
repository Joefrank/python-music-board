class MusicScore:
    

    def __init__(self, top_left, score_width, title, credits):        
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

   
  
