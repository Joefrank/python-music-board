import pygame

from Configs.screen_config import Color, GenericConfig, StaffConfig, staff_generic_settings
from Models import Note
from Models.Position import Position
from Configs.music_config import NoteOptions, default_note_duration

class BaseRenderer:

    @property
    def screen(self):
        return self.state.main_canvass
    
    def __init__(self, state):
        self.state = state
        self.screen_init_time = None
        self.original_screen = None       
        # put these in config
        self.default_note_duration = default_note_duration

    def render_mouse_tracker(self, position, key_id):
        note_duration = self.get_registered_note_duration()
        self.draw_note(note_duration, key_id, 40, 30, position) 

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
            screen.blit(text_renderer, text_rect)
        elif text_alignment == "CENTER": # position here is the will be x: staff_top_left and y where you want title
            text_block_x = (container_width // 2) - (text_renderer.get_width() // 2)
            screen.blit(text_renderer, (position.x + text_block_x, position.y))
        else:
            screen.blit(text_renderer, (position.x, position.y))  # White color text

    def draw_line_from_point(self, start_point, end_point, color=(0, 0, 0), thickness=1):
        pygame.draw.line(self.screen, color, (start_point.x, start_point.y),
                         (end_point.x, end_point.y), thickness)
        
    def draw_line(self, line, color=(0, 0, 0), thickness=1):
        self.draw_line_from_point(line.start_position, line.end_position, color, 
                                  thickness if line.thickness is None else line.thickness) 

    """ 
        note_type: duration of note (1: note, 2: semi-brev , 4:quaver), 
        note_size: font-size, 
        position: bottom-left position
    """
    def draw_note(self, note_duration_details, note_name, note_size, stem_height, position, color=(100, 100, 100)):
        note_font_size = pygame.font.Font("fonts/Bravura.otf", note_size)
        note = note_font_size.render(note_duration_details[2], True, color)
        # Get its rect and move it
        note_rect = note.get_rect(center=position.get_tuple())
        self.screen.blit(note, note_rect)

        # draw stem only if config says so
        if note_duration_details[3]:
            stem_start = (note_rect.right - 2, position.y)  # stem on right
            stem_end = (note_rect.right - 2, position.y - stem_height)
            pygame.draw.line(self.screen, color, stem_start, stem_end, 2) 

        text_position = Position(position.x + 5, position.y)           
        self.draw_text(self.screen, note_name, text_position, 20, font_color=color)

    def render_symbol(self, size, symbol_value, position, color=Color.BLACK):
        font = pygame.font.Font(GenericConfig.BRAVURA_FONT_PATH, size)
        surface = font.render(symbol_value, True, color)
        note_rect = surface.get_rect(center=position.get_tuple())
        self.screen.blit(surface, note_rect)
        return note_rect
    
    def render_note(self, note:Note, show_key_id:bool =False, note_color=Color.BLACK, text_color=Color.BLACK) -> None:
        # render main note symbol
        note_rect = self.render_symbol(StaffConfig.STAFF_NOTE_SIZE, note.duration[2], note.position, note_color)
        # check for extention - staccato
        if note.staccato:
            staccato_offset = note.position.y - 7 if note.stem_inverted else note.position.y + 10
            stacc_position = Position(note.position.x, staccato_offset)
            self.render_symbol(StaffConfig.STACCATO_SYMBOL_SIZE, NoteOptions.STACCATO, stacc_position, note_color)
        
        # check note extension
        if note.extended:
            extended_position = Position(note.position.x + 12, note.position.y)
            self.render_symbol(StaffConfig.STACCATO_SYMBOL_SIZE, NoteOptions.STACCATO, extended_position, note_color)

        # draw stem only if config says so
        if note.duration[3]:
            # check note inversion
            line_end_y = note.position.y
            if note.stem_inverted:               
                line_end_y +=  StaffConfig.STAFF_NOTE_STEM_SIZE
            else:
                line_end_y -=  StaffConfig.STAFF_NOTE_STEM_SIZE

            stem_start = (note_rect.right - 2, note.position.y)  # stem on right
            stem_end = (note_rect.right - 2, line_end_y)
            pygame.draw.line(self.screen, note_color, stem_start, stem_end, 2) 

        # show the note name if necessary
        if show_key_id:
            text_position = Position(note.position.x + 10, note.position.y)           
            self.draw_text(self.screen, note.key_id, text_position, 20, font_color=text_color)

    def draw_staff_item_note(self, note:Note):
        #self.draw_note(self.default_note_duration, note.key_id, 40, 30, note.position)
        self.render_note(note, True, Color.BLACK, Color.BLACK)

    """ Draws notes that are on specific staff_item line/interval. """
    def draw_item_notes(self, staff_item):
        for note in staff_item.notes:
            self.draw_staff_item_note(note)

    def draw_rect_surface(self, screen, width, height, surface_color, alpha, position):  
        # Create a temporary surface with per-pixel alpha
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fill with background color but apply transparency
        rect_surface.fill((*surface_color, alpha))  # RGBA
        # Draw the transparent rectangle at (100, 100)
        screen.blit(rect_surface, (position.x, position.y))

    def get_registered_note_duration(self):
         note_duration = self.state.get_registered_key() 
         if note_duration is None:
            note_duration = self.default_note_duration 
         return note_duration