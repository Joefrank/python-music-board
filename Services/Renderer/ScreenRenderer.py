import logging
import pygame
from Configs import screen_config
from Models.DataModels.ApplicationState import ApplicationState
from Models.Position import Position
from Services.Renderer.MenuRenderer import MenuRenderer
from Services.Renderer.BaseRenderer import BaseRenderer
from Services.Renderer.MusicScoreRenderer import MusicScoreRenderer


class ScreenRenderer(BaseRenderer):  

    def __init__(self, state):
        super().__init__(state)
        self.main_canvas = None
        self.logger = logging.getLogger(__name__)
        self.score_renderer = MusicScoreRenderer(state) 
        self.menu_renderer = MenuRenderer(state)

    def init_screen(self, width, height, caption, background_color=(30, 30, 30)):
        pygame.init()
        self.main_canvas = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.main_canvas.fill(background_color)
        pygame.display.set_caption(caption)
        return self.main_canvas

    def render_frame(self) -> None:
        """Render a complete frame."""
       # try:
        if self.state.screen_needs_refresh:
            self._clear_screen(self.state.main_canvass)
            self.menu_renderer.render_menu()
            self.score_renderer.render_score(self.state.main_canvass, self.state.music_score)               
            pygame.display.flip()
            self.state.set_screen_refresh_status(False)
        #except Exception as e:
           # self.logger.error(f"Rendering error: {e}")

    def _clear_screen(self, screen) -> None:
        """Clear the screen with background color."""
        screen.fill(screen_config.WindowConfig.BACKGROUND_COLOR)