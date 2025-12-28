"""Application state management."""

import copy
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from pygame import Surface
from Configs.screen_config import Color, MouseEventType
from Configs.music_config import valid_note_durations, note_modifiers
from Models import MusicScore, Note
from Models.Chord import Chord
from Models.Events.ScreenUpdateEvent import ScreenUpdateEvent
from Models.GrandStaff import GrandStaff
from Models.Menu import MainMenu
from Models.Menu.MenuItem import MenuItem
from Models.Events.MouseEvent import MouseEvent
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
        self.music_score_backup = None #used to reset score
        self.error_messages = List[str]
        self.last_note_added = None        
        self.note_duration = None
        self.note_modifier = None
        self.main_menu = None
        self.screen_width = None
        self.screen_height = None
        self.mouse_click = MouseEvent(MouseEventType.CLICK)
        self.mouse_hover = MouseEvent(MouseEventType.HOVER)
        self.score_navigator = None
        self.events_queue = []
        self.pending_chord: Chord = None

    def raise_screen_update_event(self):
        screen_update_event = ScreenUpdateEvent()
        screen_update_event.register(self)
        self.events_queue.append(screen_update_event)

    def screen_update_needed(self) -> bool:
        self.screen_needs_refresh = True
    
    def get_next_event(self):
        if len(self.events_queue) == 0:
            return None
        return self.events_queue.pop(0)
    
    def set_renderers(self, staff_renderer, screen_renderer):
        self.staff_renderer = staff_renderer
        self.screen_renderer = screen_renderer

    def set_main_screen(self, screen: Surface):
        self.main_canvass = screen
        
    def set_screen_refresh_status(self, needs_refresh: bool):
        self.screen_needs_refresh = needs_refresh

    def set_music_score(self, score: MusicScore):
        self.music_score = score
        self.music_score_backup = copy.deepcopy(score)

    def set_score_navigator(self, score_navigator):
        self.score_navigator = score_navigator

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
          
        if key_name.isnumeric(): # this is potentially a key duration
            note_duration_details = next((item for item in valid_note_durations if item[0] == key_name), None)
            # At this stage, we only register note duration details.
            if note_duration_details is not None:
                self.note_duration = note_duration_details # this is font code
        elif key_name in note_modifiers:
            self.note_modifier = StaffUtils.get_modifier_by_key(key_name)          
            # We want to clear the mouse tracking for any note modifier 
            # TODO: leave tracker until you come to close to a existing note
            if self.note_modifier is not None:
                self.hide_mouse_tracker()
    
    def hide_mouse_tracker(self):
        self.mouse_hover.reset_current_position()                   
        self.set_screen_refresh_status(True)      
    
    def handle_pending_events(self):
        # TODO: play the pending chord and record it
        if self.pending_chord is not None:
            self.sound_player.play_chord(self.pending_chord)
            self.pending_chord = None

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
    
    def effect_note_modifier(self, note: Note, modifier):        
        if modifier[1] == 1:
            note.implement_unary_modifier(modifier)
        elif modifier[1] == 2:
            note.implement_binary_modifier(modifier)
        elif modifier[1].lower() == 'x':          
            if self.pending_chord is None:
                self.pending_chord = Chord("", note.position.x)           
            self.pending_chord.add_note(note)

    def set_main_menu(self, menu:MainMenu):
        self.main_menu = menu

    def register_mouse_over_event(self, new_mouse_position):
        self.mouse_hover.set_current_position(new_mouse_position)
        self.mouse_hover.notify()

    def register_mouse_click_event(self, new_mouse_position):
        self.mouse_click.set_current_position(new_mouse_position)
        self.mouse_click.notify()
            
    def reset_all_actions(self, source_menu_item:MenuItem):
        self.music_score = copy.deepcopy(self.music_score_backup) 
        if source_menu_item is not None:
            source_menu_item.deactivate_item()

    def highlight_chord(self, chord: Chord, highlight: bool):
        for note in chord.notes:
            if not highlight and not note.is_in_play():
                color = Color.BLACK
            else:
                color = Color.PINK
            note.highlight(color)
        self.set_screen_refresh_status(True)

    def clear_pending_notes(self, notes: list[Note]):
        for note in notes:
            note.highlight(Color.BLACK)