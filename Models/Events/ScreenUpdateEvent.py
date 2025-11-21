
from Models.Events.Event import Event


class ScreenUpdateEvent(Event):
    def __init__(self):
        super().__init__()

    def notify(self) -> bool:
        for listener in self.listeners:
            listener.screen_update_needed()
            
        return True