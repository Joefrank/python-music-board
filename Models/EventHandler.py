"""Event handling for the music application."""

import pygame
import logging
from Models.DataModels.ApplicationState import ApplicationState


class EventHandler:
    """Handles all user input events."""

    def __init__(self, state: ApplicationState):
        self.state = state
        self.logger = logging.getLogger(__name__)

    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    self._handle_quit()
                #elif event.type == pygame.KEYDOWN:
                   # self._handle_key_down(event)
                #elif event.type == pygame.KEYUP:
                  #  self._handle_key_up(event)
                #elif event.type == pygame.MOUSEBUTTONDOWN:
                   # self._handle_mouse_click(event)
                #elif event.type == pygame.VIDEORESIZE:
                   # self._handle_window_resize(event)
            except Exception as e:
                self.logger.error(f"Error handling event {event.type}: {e}")
                #self.state.add_error(f"Event handling error: {e}")

    def _handle_quit(self) -> None:
        """Handle application quit event."""
        self.logger.info("Application quit requested")
        self.state.is_running = False


