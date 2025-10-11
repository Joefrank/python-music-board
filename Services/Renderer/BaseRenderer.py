import pygame

from Models.Position import Position

class BaseRenderer:

    def __init__(self, state):
        self.state = state
        self.screen_init_time = None
        self.original_screen = None
        # put these in config
        self.default_note_duration = ("4","Quarter","\uE0A4", True)

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

    """ 
        Draws text on screen. position: Position object
    """
    def draw_text(self, screen, text, position, font_size, container_width=100, font_color=(0, 0, 0), text_alignment="LEFT"):
        font = pygame.font.SysFont(None, font_size)  # None = default font, 48 = font size
        text_renderer = font.render(text, True, font_color)
        if text_alignment == "RIGHT":
            text_rect = text_renderer.get_rect()
            text_rect.topright = (position.x, position.y) # 20 px for padding
            #print(position)
            screen.blit(text_renderer, text_rect)
        elif text_alignment == "CENTER": # position here is the will be x: staff_top_left and y where you want title
            text_block_x = (container_width // 2) - (text_renderer.get_width() // 2)
            screen.blit(text_renderer, (position.x + text_block_x, position.y))
            #print((position.x + text_block_x, position.y))
        else:
            screen.blit(text_renderer, (position.x, position.y))  # White color text

    def draw_line_from_point(self, start_point, end_point, screen, color=(0, 0, 0), thickness=1):
        pygame.draw.line(screen, color, (start_point.x, start_point.y),
                         (end_point.x, end_point.y), thickness)
        
    def draw_line(self, line, screen, color=(0, 0, 0), thickness=1):
        self.draw_line_from_point(line.start_position, line.end_position, screen, color, thickness) 

    """ 
        note_type: duration of note (1: note, 2: semi-brev , 4:quaver), 
        note_size: font-size, 
        position: bottom-left position
    """
    def draw_note(self, screen, note_duration_details, note_name, note_size, stem_height, position):
        note_font_size = pygame.font.Font("fonts/Bravura.otf", note_size)
        note = note_font_size.render(note_duration_details[2], True, (100, 100, 100))
        # Get its rect and move it
        note_rect = note.get_rect(center=position.get_tuple())
        screen.blit(note, note_rect)

        # draw stem only if config says so
        if note_duration_details[3]:
            #y = position.y  # - note_size
            stem_start = (note_rect.right - 2, position.y)  # stem on right
            stem_end = (note_rect.right - 2, position.y - stem_height)
            #print(f"stem_start: {stem_start} - stem_end: {stem_end}")
            pygame.draw.line(screen, (0, 0, 0), stem_start, stem_end, 2)
            position.translateTo(10, 0)
            self.draw_text(screen, note_name, position, 30, font_color=(200, 70, 70))
            
    def draw_rect_surface(self, screen, width, height, surface_color, alpha, position):  
        # Create a temporary surface with per-pixel alpha
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fill with background color but apply transparency
        rect_surface.fill((*surface_color, alpha))  # RGBA
        # Draw the transparent rectangle at (100, 100)
        screen.blit(rect_surface, (position.x, position.y))