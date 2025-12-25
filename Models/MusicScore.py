from pathlib import Path
import json

from Services.Utils.InputOutputUtils import IOUtils

class MusicScore: 

    BASE_DIR = Path(__file__).resolve().parent

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
        self.output_dir = self.BASE_DIR / "music_sheets"

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
       
    def save_details(self):
        IOUtils.save_score_details(self, self.output_dir)
   
  
    def to_json(self):
        return {
            "top_left_position": self._serialize(self.top_left_position),
            "score_width": self.score_width,
            "title": self.title,
            #"raw_credits": [self._serialize(c) for c in self.raw_credits],
            #"credits": [self._serialize(c) for c in self.credits],
           # "lyrics": [self._serialize(c) for c in self.lyrics],
            "staff_color": self.staff_color,
            #"key_signature_list": [self._serialize(c) for c in self.key_signature_list],
            "title_position": self._serialize(self.title_position),
            "highest_credit_y_offset": self.highest_credit_y_offset,
            # "staves_sequence": [
            #     self._serialize(staff) for staff in self.staves_sequence
            # ],
            #"output_dir": str(self.output_dir)
        }

    @staticmethod
    def _serialize(obj):
        """Helper for nested objects"""
        if obj is None:
            return None
        if hasattr(obj, "to_json"):
            return obj.to_json()
        if isinstance(obj, Path):
            return str(obj)
        return "" #obj