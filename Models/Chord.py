from Models.Note import Note


class Chord:

    def __init__(self, name: str, x_offset: int = 0):
        self.name = name
        self.notes: list[Note] = []
        self.x_offset = x_offset

    def add_note(self, note: Note):
        note.position.moveHorizontallyTo(self.x_offset)
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
        pass

    def get_playable_notes(self) -> list[(int, int)]:
        notes_to_play = []
        for note in self.notes:
            note_duration, rest_duration = note.get_exact_duration()
            notes_to_play.append((note.key_value, note_duration))
            if rest_duration > 0:
                notes_to_play.append((0, rest_duration))  # 0 key_value for rest

        return notes_to_play
    
    def __str__(self):
        return f"Chord: {self.name} - Notes: " + " | ".join(str(note) for note in self.notes)


    