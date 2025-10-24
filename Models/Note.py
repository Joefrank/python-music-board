from Models.Position import Position


class Note:

    """
        staff_item: line/interval containing this note
        duration: how long is the note for
        position: position on the staff item
        order: order on the staff item
        extended: if note duration is extended
        key: the related music note/key name that is for this object
        key_id: the exact piano music key to be played for this note
        beam_width: if this note has another key it is connected with.
    """
    def __init__(self, duration, position, order, extended, key, key_id, beam_with=None):
        #self.staff_item = staff_item
        self.duration:int = duration # in beats
        self.position:Position = position # position to center rest around
        self.order:int = order
        self.extended:bool = extended
        self.stackato:bool = None
        self.key:str = key
        self.key_id:str = key_id
        self.beam_with:Note = beam_with # this is when we link to another note

    def set_parent(self, staff_item):
        self.staff_item = staff_item