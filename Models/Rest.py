class Rest:
    duration = None # in beats
    position = None # position to center rest around

    def __init__(self, duration, position):
        self.duration = duration
        self.position = position