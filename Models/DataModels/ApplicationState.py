"""Application state management."""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from Models import Position
from Services.Sound.PianoSoundPlayer import SoundPlayer

@dataclass
class ApplicationState:
    """Manages the current state of the application."""
   
    #current_note_duration: Optional[Tuple[str, str, str, bool]] = None
    #selected_staff = None
    #last_clicked_position: Optional[Position] = None
    is_running: bool = True
    needs_refresh: bool = True
    previous_mouse_over_position: Position = None
    current_mouse_over_position: Position = None
    previous_mouse_click_position: Position = None
    current_mouse_click_position: Position = None
    #placed_notes: List = field(default_factory=list)
    #error_messages: List[str] = field(default_factory=list)
    def __init__(self):
        self.sound_player = SoundPlayer() 

    #def set_note_duration(self, duration_details: Tuple[str, str, str, bool]) -> None:
      #  """Set the current note duration."""
        #self.current_note_duration = duration_details

    #def clear_note_duration(self) -> None:
       # """Clear the current note duration."""
        #self.current_note_duration = None

    #def add_error(self, message: str) -> None:
       # """Add an error message to the queue."""
        #self.error_messages.append(message)

   # def get_and_clear_errors(self) -> List[str]:
       # """Get all error messages and clear the queue."""
       # errors = self.error_messages.copy()
       # self.error_messages.clear()
       # return errors