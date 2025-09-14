class StaffStep:
    duration = None
    start_position = None
    end_position = None
    notes_key_ids = []
    beam_with_step = None

    def __init__(self, duration, start_position, end_position):
        self.duration = duration
        self.start_position = start_position
        self.end_position = end_position

    def add_key_id(self, key_id):
        self.notes_key_ids.append(key_id)