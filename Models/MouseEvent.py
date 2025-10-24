from Configs.screen_config import MouseEventType
from Models.Position import Position


class MouseEvent:

    def __init__(self, event_type: MouseEventType):
        self.event_type = event_type
        self.previous_position = None
        self.current_position = None

    def get_previous_position(self):
        return self.previous_position
    
    def get_current_position(self):
        return self.current_position
    
    def set_previous_position(self, position: Position):
        self.previous_position = position

    def set_current_position(self, position: Position):
        self.previous_position = self.current_position
        self.current_position = position

    def reset_current_position(self):
        self.previous_position = self.current_position
        self.current_position = None
        
    def reset(self):
        self.previous_position = None
        self.current_position = None

    
