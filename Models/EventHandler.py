"""Event handling for the music application."""

import pygame
import logging
from Models import Note
from Models.DataModels.ApplicationState import ApplicationState
from Models.Position import Position
from Services.Renderer.ScreenRenderer import ScreenRenderer
from Services.Renderer.StaffRenderer import StaffRenderer
from Services.Sound.PianoSoundPlayer import SoundPlayer
from Services.Utils import StaffUtils

class EventHandler:
    """Handles all user input events."""

    def __init__(self, state: ApplicationState):
        self.state = state
        self.logger = logging.getLogger(__name__)
        self.screen_renderer = state.screen_renderer
        self.sound_player = state.sound_player
        self.staff_renderer = state.staff_renderer

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
                elif event.type == pygame.KEYDOWN:
                    self._handle_key_down(event)
                elif event.type == pygame.KEYUP:
                    self._handle_key_up()
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
        # we don't want to show mouse tracker when unary key modifiers are down
        note_modifier = self.state.get_registered_note_modifier()
        if note_modifier is None or note_modifier[1] == 2:
            mouse_position = Position(event.pos[0], event.pos[1])
            self.state.register_mouse_over_event(mouse_position)
            self.state.set_screen_refresh_status(True)

    def _handle_mouse_click(self, event) -> None:
        #we want only mouse left button click
        if event.button != 1:
            return
        
        # check if there are modifiers, that will determine what to do with mouse click
        note_modifier = self.state.get_registered_note_modifier()
        click_position = Position(event.pos[0], event.pos[1])
        self.state.register_mouse_click_event(click_position)
        nearest_note = None
        # if any modifier (key down) has been registered before click. unary modifier only in this case
        if note_modifier is not None and note_modifier[1] == 1:
            # check if there is any note near click and modify it           
            nearest_note = self.state.check_click_around_note(click_position)
            if nearest_note is not None:
                self.state.effect_note_modifier(nearest_note, note_modifier)

        # this will cause a new note to be added if no nearest note has been found.
        if nearest_note is None:
            self.state.mouse_click.set_current_position(click_position)
            self.state.set_screen_refresh_status(True)
        
    def _handle_key_down(self, event) -> None:
        key_name = pygame.key.name(event.key).upper()
        self.state.register_key_down(key_name)

    def _handle_key_up(self) -> None:
        self.state.cancel_key_down()

    