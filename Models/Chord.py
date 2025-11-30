class Chord:

    def __init__(self, name: str, notes: list[(int, int)], x_offset: int = 0):
        self.name = name
        self.notes = notes
        self.x_offset = x_offset

    def add_note(self, note_tuple: tuple[int, int]):
        self.notes.append(note_tuple)
        self.reassess_name()

    """ Should only append a chord with same x_offset. And name might change based on new notes added """
    def append_chord(self, chord) -> bool:
        if chord.x_offset != self.x_offset:
            return False
        self.notes.extend(chord.notes)
        self.reassess_name()
        return True
        
    def reassess_name(self):
        # logic to reassess chord name based on notes
        pass