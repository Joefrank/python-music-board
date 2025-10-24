import logging
import pygame
from Configs import screen_config
from Models.DataModels.ApplicationState import ApplicationState
from Services.Renderer.BaseRenderer import BaseRenderer
from Services.Renderer.MusicScoreRenderer import MusicScoreRenderer


class ScreenRenderer(BaseRenderer):
    RED = (255, 0, 0)
    main_canvas = None

    def __init__(self, state: ApplicationState):
        super().__init__(state) 
        self.main_canvas = None
        self.logger = logging.getLogger(__name__)
        self.score_renderer = MusicScoreRenderer(state)        
        #self.state = state

    def init_screen(self, width, height, caption, background_color=(30, 30, 30)):
        pygame.init()
        self.main_canvas = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.main_canvas.fill(background_color)
        pygame.display.set_caption(caption)
        return self.main_canvas

    def render_mouse_tracker(self, screen, position):
        pygame.draw.circle(screen, self.RED, position, 5)

    def render_frame(self) -> None:
        """Render a complete frame."""
        try:
            if self.state.needs_refresh:
                #print("refreshing.")
                self._clear_screen(self.screen)
                self.score_renderer.render_score(self.screen, self.state.music_score)               
                pygame.display.flip()
                self.state.needs_refresh = False
                #print("Completed Refreshing.")
        except Exception as e:
            self.logger.error(f"Rendering error: {e}")

    def _clear_screen(self, screen) -> None:
        """Clear the screen with background color."""
        screen.fill(screen_config.WindowConfig.BACKGROUND_COLOR)