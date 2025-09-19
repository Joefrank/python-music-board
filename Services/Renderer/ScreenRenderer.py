import pygame

class ScreenRenderer:

    main_canvas = None

    def __init__(self):
        self.main_canvas = None

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