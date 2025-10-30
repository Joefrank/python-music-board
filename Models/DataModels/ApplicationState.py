"""Application state management."""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from pygame import Surface
from Configs.screen_config import MouseEventType
from Configs.music_config import valid_note_durations, note_modifiers
from Models import MusicScore, Note
from Models.GrandStaff import GrandStaff
from Models.Menu import MainMenu
from Models.MouseEvent import MouseEvent
from Models.Position import Position
from Models.Staff import Staff
from Services.Sound.PianoSoundPlayer import SoundPlayer
from Services.Utils import StaffUtils


class ApplicationState:
    """Manages the current state of the application.""" 

    def __init__(self):
        self.sound_player = SoundPlayer() 
        self.main_canvass: Surface = None
        self.staff_renderer = None
        self.screen_renderer = None
        self.is_running: bool = True
        self.screen_needs_refresh = False
        self.music_score = None
        self.error_messages = List[str]
        self.last_note_added = None        
        self.note_duration = None
        self.note_modifier = None
        self.main_menu = None
        self.screen_width = None
        self.screen_height = None
        self.mouse_click = MouseEvent(MouseEventType.CLICK)
        self.mouse_hover = MouseEvent(MouseEventType.HOVER)

    def set_renderers(self, staff_renderer, screen_renderer):
        self.staff_renderer = staff_renderer
        self.screen_renderer = screen_renderer

    def set_main_screen(self, screen: Surface):
        self.main_canvass = screen
        
    def set_screen_refresh_status(self, needs_refresh: bool):
        self.screen_needs_refresh = needs_refresh

    def set_music_score(self, score: MusicScore):
        self.music_score = score

    def set_last_added_note(self, note: Note):
        self.last_note_added = note
    
    def add_error(self, message: str) -> None:
       # """Add an error message to the queue."""
        self.error_messages.append(message)

    def get_and_clear_errors(self) -> List[str]:
       """Get all error messages and clear the queue."""
       errors = self.error_messages.copy()
       self.error_messages.clear()
       return errors
    
    """ Registers key down as note duration."""
    def register_key_down(self, key_name):
        if key_name.isnumeric(): # this is key duration
            note_duration_details = next((item for item in valid_note_durations if item[0] == key_name), None)
            # At this stage, we only register note duration details.
            if note_duration_details is not None:
                self.note_duration = note_duration_details # this is font code
        elif key_name in note_modifiers:
            self.note_modifier = StaffUtils.get_modifier_by_key(key_name)
            # if key is unary, we want to clear mouse over recording
            if self.note_modifier[1] == 1:
                self.mouse_hover.reset_current_position()
                self.set_screen_refresh_status(True)
           

    def cancel_key_down(self):
        self.note_duration = None
        self.note_modifier = None

    def get_registered_key(self):
        return self.note_duration
    
    def get_registered_note_modifier(self):
        return self.note_modifier
    
    def check_click_around_note(self, position) -> Note:
        for staff in self.music_score.staves_sequence:
            nearest_note = staff.find_nearest_note(position)
            if nearest_note is not None:
                return nearest_note
        return None   
    
    def effect_note_modifier(self, note, modifier):
        if modifier[1] == 1:
            note.implement_unary_modifier(modifier)
        elif modifier[1] == 2:
            note.implement_binary_modifier(modifier)

    def set_main_menu(self, menu:MainMenu):
        self.main_menu = menu