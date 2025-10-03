import logging
import pygame
from Configs import screen_config
from Models.DataModels.ApplicationState import ApplicationState
from Services.Renderer.StaffRenderer import StaffRenderer

class ScreenRenderer:
    RED = (255, 0, 0)
    main_canvas = None

    def __init__(self, state: ApplicationState):
        self.main_canvas = None
        self.logger = logging.getLogger(__name__)
        self.staff_renderer = StaffRenderer(state)
        self.state = state

    def init_screen(self, width, height, caption, background_color=(30, 30, 30)):
        pygame.init()
        self.main_canvas = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.main_canvas.fill(background_color)
        pygame.display.set_caption(caption)
        return self.main_canvas

    def draw_rect_surface(self, width, height, surface_color, alpha, position, screen=None):
        if self.main_canvas is None and screen is None:
            print("Screen has not been initialized.")
            return
        elif self.main_canvas is None and screen is not None:
            self.main_canvas = screen

        # Create a temporary surface with per-pixel alpha
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fill with background color but apply transparency
        rect_surface.fill((*surface_color, alpha))  # RGBA
        # Draw the transparent rectangle at (100, 100)
        self.main_canvas.blit(rect_surface, (position.x, position.y))

    def render_mouse_tracker(self, screen, position):
        pygame.draw.circle(screen, self.RED, position, 5)

    def render_frame(self, screen, music_score) -> None:
        """Render a complete frame."""
        try:
            if self.state.needs_refresh:
                self._clear_screen(screen)
                self.staff_renderer.render_music_score(screen, music_score)
                #self._render_ui_elements()
                #self._render_error_messages()
                pygame.display.flip()
                self.state.needs_refresh = False
        except Exception as e:
            self.logger.error(f"Rendering error: {e}")
            #self.state.add_error(f"Rendering failed: {e}")

    def _clear_screen(self, screen) -> None:
        """Clear the screen with background color."""
        screen.fill(screen_config.WindowConfig.BACKGROUND_COLOR)