"""Application state management."""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from pygame import Surface
from Configs.screen_config import MouseEventType
from Models.MouseEvent import MouseEvent
from Models.Position import Position
from Services.Sound.PianoSoundPlayer import SoundPlayer


class ApplicationState:
    """Manages the current state of the application."""  
    
    is_running: bool = True
    last_staff_item_hovered = None #line/interval
    current_staff_item_hovered = None #line/interval

    #placed_notes: List = field(default_factory=list)
    #error_messages: List[str] = field(default_factory=list)
    def __init__(self):
        self.sound_player = SoundPlayer() 
        self.main_canvass: Surface = None
        self.staff_renderer = None
        self.screen_renderer = None

        self.screen_needs_refresh = False
        self.mouse_click = MouseEvent(MouseEventType.CLICK)
        self.mouse_hover = MouseEvent(MouseEventType.HOVER)

    def set_renderers(self, staff_renderer, screen_renderer):
        self.staff_renderer = staff_renderer
        self.screen_renderer = screen_renderer

    def set_main_screen(self, screen: Surface):
        self.main_canvass = screen
        
    def set_screen_refresh_status(self, needs_refresh: bool):
        self.screen_needs_refresh = needs_refresh

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