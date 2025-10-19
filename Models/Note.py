class Note:
    duration = None # in beats
    position = None # position to center rest around
    line_order = None
    extended = False
    stackato = False
    key = None
    key_id = None
    beam_with = None # this is when we link to another note

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
    def __init__(self, staff_item, duration, position, order, extended, key, key_id, beam_width=None):
        self.staff_item = staff_item
        self.duration = duration
        self.position = position
        self.order = order
        self.extended = extended
        self.key = key
        self.key_id = key_id
        self.beam_width = beam_width