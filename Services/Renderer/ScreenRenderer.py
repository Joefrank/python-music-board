import pygame

class BaseRenderer:

    def __init__(self):
        self.screen_init_time = None
        self.original_screen = None

    def draw_rect_surface(self, width, height, surface_color, alpha, position):
        if self.original_screen is None:
            print("Screen has not been initialized.")
            return
        # Create a temporary surface with per-pixel alpha
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fill with background color but apply transparency
        rect_surface.fill((*surface_color, alpha))  # RGBA
        # Draw the transparent rectangle at (100, 100)
        self.original_screen.blit(rect_surface, (position.x, position.y))