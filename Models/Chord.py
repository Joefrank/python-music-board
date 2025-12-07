from Models.Note import Note


class Chord:

    def __init__(self, name: str, x_offset: int = 0):
        self.name = name
        self.notes: list[Note] = []
        self.x_offset = x_offset

    def add_note(self, note: Note):
        print(f"Note before move:{note.position}")
        note.position.moveHorizontallyTo(self.x_offset)
        print(f"Note after move:{note.position}")
        self.notes.append(note)
        self.reassess_name()

    def set_notes(self, notes):        
        self.notes = notes

    """ Should only append a chord with same x_offset. And name might change based on new notes added """
    def append_chord(self, chord) -> bool:
        if chord.x_offset != self.x_offset:
            return False
        self.notes.extend(chord.notes)
        self.reassess_name()
        return True
        
    def reassess_name(self):
        # logic to reassess chord name based on notes
        print(f"chord notes: {self.notes}")   
        pass

    def get_playable_notes(self) -> list[(int, int)]:
        return [(note.key_value, note.duration[4]) for note in self.notes]
        