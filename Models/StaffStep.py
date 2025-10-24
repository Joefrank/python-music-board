from Models import Position

class StaffStep:
    
    def __init__(self, duration:int, start_position: Position, end_position: Position):
        self.duration = duration
        self.start_position = start_position
        self.end_position = end_position
        self.notes_key_ids = []
        self.beam_with_step = None

    def add_key_id(self, key_id):
        self.notes_key_ids.append(key_id)

    def add_key_ids(self, keys):
        self.notes_key_ids = keys