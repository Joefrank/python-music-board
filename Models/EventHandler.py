"""Event handling for the music application."""

import pygame
import logging
from Configs.constants import SoundPlayerEventConstants
from Models import Note
from Models.DataModels.ApplicationState import ApplicationState
from Models.Events.Event import Event
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
        #check events in state
        next_event:Event = self.state.get_next_event()
        if next_event is not None:            
            next_event.notify()
      
    def handle_polling(self) -> None:
        """Handle polling-based updates."""         
        # Poll for sound feedback events       
        while not self.sound_player.feedback_queue.empty():
            feedback_event = self.sound_player.feedback_queue.get()
            event_type, event_data = feedback_event
            if event_type == SoundPlayerEventConstants.CHORD_START:
                self.state.highlight_chord(event_data, True)
            elif event_type == SoundPlayerEventConstants.CHORD_END:
                self.state.highlight_chord(event_data, False)
            elif event_type == SoundPlayerEventConstants.BATCH_END:
                self.state.score_navigator.move_next()  # Play next chord batch
            elif event_type == SoundPlayerEventConstants.PENDING_CHORD_END:
                self.state.clear_pending_notes(event_data)
            self.sound_player.feedback_queue.task_done()

            
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
        self.state.register_mouse_click_event(Position(event.pos[0], event.pos[1])) # TODO: modify everything after this cause click should be actioned in function
        
        
    def _handle_key_down(self, event) -> None:
        key_name = pygame.key.name(event.key).lower()
        self.state.register_key_down(key_name)

    def _handle_key_up(self) -> None:
        self.state.handle_pending_events()
        self.state.set_screen_refresh_status(True)
        self.state.cancel_key_down()

    