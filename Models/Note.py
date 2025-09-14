class Note:
    duration = None # in beats
    position = None # position to center rest around
    line_order = None
    extended = False
    stackato = False
    name = None
    key = None
    key_id = None
    beam_with = None # this is when we link to another note

    def __init__(self, duration, position, order, extended, name, key, key_id, beam_with):
        self.duration = duration
        self.position = position
        self.order = order
        self.extended = extended
        self.name = name
        self.key = key
        self.key_id = key_id
        self.beam_with = beam_with