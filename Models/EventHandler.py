"""Event handling for the music application."""

import pygame
import logging
from Configs.music_config import NoteDurationInTicks, default_note_duration
from Models import Note
from Models.DataModels.ApplicationState import ApplicationState
from Models.Position import Position
from Services.Renderer.ScreenRenderer import ScreenRenderer
from Services.Renderer.StaffRenderer import StaffRenderer
from Services.Sound.PianoSoundPlayer import SoundPlayer
from Services.Utils import StaffUtils

class EventHandler:
    """Handles all user input events."""

    def __init__(self, state: ApplicationState, staff_renderer: StaffRenderer):
        self.state = state
        self.logger = logging.getLogger(__name__)
        self.screen_renderer = ScreenRenderer(state)
        self.sound_player = state.sound_player
        self.staff_renderer = staff_renderer

    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    self._handle_quit()
                elif event.type == pygame.MOUSEMOTION:
                    self._handle_mouse_over(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                   self._handle_mouse_click(event)                
                #elif event.type == pygame.KEYDOWN:
                    #self._handle_key_down(event)
                #elif event.type == pygame.KEYUP:
                  #  self._handle_key_up(event)
                #elif event.type == pygame.VIDEORESIZE:
                   # self._handle_window_resize(event)
            except Exception as e:
                self.logger.error(f"Error handling event {event.type}: {e}")
                #self.state.add_error(f"Event handling error: {e}")

    def _handle_quit(self) -> None:
        """Handle application quit event."""
        self.logger.info("Application quit requested")
        self.state.is_running = False

    def _handle_mouse_over(self, event) -> None:  ## only set this position active if it collides with item on score
        if self.state.current_mouse_over_position is None:
            self.state.current_mouse_over_position = Position(event.pos[0], event.pos[1])  
        else:    
            self.state.current_mouse_over_position.from_tuple(event.pos)
        self.state.needs_refresh = True

    def _handle_mouse_click(self, event) -> None:

        if self.state.current_staff_item_hovered is not None:
            mouse_position = Position(event.pos[0], event.pos[1])
            staff_item = self.state.current_staff_item_hovered
            key_code = StaffUtils.get_key_code_from_keyid(staff_item.key_id)
            self.sound_player.play_piano_note(key_code, NoteDurationInTicks.QUARTER)           
            
            note_duration = default_note_duration 
            note_order = staff_item.get_next_note_index()  
            note_extended = False     
            new_note = Note(staff_item, note_duration, mouse_position, note_order, note_extended, staff_item.key,
                            staff_item.key_id)
            staff_item.add_note(new_note)  

            #self.staff_renderer.draw_staff_item_notes(self.state.main_canvass, staff_item)
            #self.staff_renderer.render_note_at_position(mouse_position, self.state.main_canvass, staff_item)
            
            self.state.last_staff_item_hovered = self.state.current_staff_item_hovered
            self.state.current_staff_item_hovered = None
            
            self.state.needs_refresh = True

        # if self.state.current_mouse_click_position is None:
        #     self.state.current_mouse_click_position =  mouse_position 
        # else:    
        #     self.state.current_mouse_click_position.from_tuple(event.pos)
        