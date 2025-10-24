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
        self.state.mouse_hover.set_current_position(Position(event.pos[0], event.pos[1])) 
        self.state.set_screen_refresh_status(True)

    def _handle_mouse_click(self, event) -> None:
        self.state.mouse_click.set_current_position(Position(event.pos[0], event.pos[1]))
        self.state.set_screen_refresh_status(True)
        
       