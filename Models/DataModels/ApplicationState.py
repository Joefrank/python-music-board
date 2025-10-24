"""Application state management."""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple

from pygame import Surface
from Models.Position import Position
# from Services.Renderer.ScreenRenderer import ScreenRenderer
# from Services.Renderer.StaffRenderer import StaffRenderer
from Services.Sound.PianoSoundPlayer import SoundPlayer

@dataclass
class ApplicationState:
    """Manages the current state of the application."""  
    
    is_running: bool = True
    needs_refresh: bool = True
    previous_mouse_over_position: Position = None
    current_mouse_over_position: Position = None
    previous_mouse_click_position: Position = None
    current_mouse_click_position: Position = None
    last_staff_item_hovered = None #line/interval
    current_staff_item_hovered = None #line/interval

    #placed_notes: List = field(default_factory=list)
    #error_messages: List[str] = field(default_factory=list)
    def __init__(self):
        self.sound_player = SoundPlayer() 
        self.main_canvass: Surface = None
        self.staff_renderer = None
        self.screen_renderer = None
        self.music_score = None

    def set_renderers(self, staff_renderer, screen_renderer):
        self.staff_renderer = staff_renderer
        self.screen_renderer = screen_renderer

    def set_main_screen(self, screen: Surface):
        self.main_canvass = screen
        
    def set_music_score(self, score):
        self.music_score = score
        
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