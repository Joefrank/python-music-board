
from Models.Events.Event import Event


class ScreenUpdateEvent(Event):
    def __init__(self, no_of_refreshes: int=1):
        super().__init__()
        self.no_of_refreshes = no_of_refreshes

    def notify(self) -> bool:
        if self.no_of_refreshes <= 0:
            return False
        for listener in self.listeners:
            listener.screen_update_needed()
            self.no_of_refreshes -= 1
            
        return True