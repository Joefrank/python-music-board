import pygame
from datetime import datetime
from Models.Position import Position
from Configs.music_config import supported_clef_settings, supported_time_signatures, supported_modulations

from Configs.screen_config import GenericConfig, StaffConfig, staff_generic_settings
from Services.Utils import StaffUtils

class StaffRenderer:

    def __init__(self):
        self.start_time = datetime.now().time()        
        self.MODULATION_SPACING = 6
        self.STAFF_ITEM_LINE = 0
        self.STAFF_ITEM_INTERVAL = 1

    def render_staff(self, staff, screen):       
        for line in staff.lines:
            self.draw_line(line, screen)
        self.draw_staff_boundaries(staff, screen)
        clef_position = self.draw_staff_clef(screen, staff)
        print(f"Cleff position:{clef_position}")
        time_numerator, time_denominator = self.draw_time_signature(screen, staff.time_signature, Position(clef_position.x + 40, staff.top_position.y))
        print(f"time numerator: {time_numerator}")
        key_signature_position = Position(time_numerator[0] + 20, time_numerator[1])
        self.draw_key_signature(staff, screen, key_signature_position)
        
        print(clef_position)
        
    def draw_staff_boundaries(self, staff, screen):
        print(f"{staff.position_rect}")
        self.draw_line_from_point(staff.position_rect.top_left, staff.position_rect.bottom_left, screen, thickness=2)
        self.draw_line_from_point(staff.position_rect.top_right, staff.position_rect.bottom_right, screen, thickness=2)
    
    def draw_line(self, line, screen, color=(0, 0, 0), thickness=1):
        self.draw_line_from_point(line.start_position, line.end_position, screen, color, thickness)       

    def draw_line_from_point(self, start_point, end_point, screen, color=(0, 0, 0), thickness=1):
        pygame.draw.line(screen, color, (start_point.x, start_point.y),
                         (end_point.x, end_point.y), thickness)
        
    def draw_virtual_line(self, screen, line, position, color=(0, 0, 0), thickness=1, specified_line_width=40):
        half_line_width = (line.end_position.x - line.start_position.x) // 2
        start_x = line.start_position.x + (half_line_width - (specified_line_width // 2))
        end_x = start_x + specified_line_width
        pygame.draw.line(screen, color, (start_x, position.y),
                         (end_x,  position.y), thickness)

    """ 
        Draws text on screen. position: Position object
    """
    def draw_text(self, screen, text, position, font_size, font_color=(0, 0, 0)):
        font = pygame.font.SysFont(None, font_size)  # None = default font, 48 = font size
        text_renderer = font.render(text, True, font_color)
        screen.blit(text_renderer, (position.x, position.y))  # White color text

    """
        Draws the clef on the staff
    """
    def draw_staff_clef(self, screen, staff, font_color=(0, 0, 0)):
        clef_settings = supported_clef_settings[staff.clef]
        clef_size = clef_settings["size"]
        clef_font_size = pygame.font.Font(GenericConfig.BRAVURA_FONT_PATH, clef_size)
        clef = clef_font_size.render(clef_settings["font_code"], True, font_color)
        # Get clef rect to position it
        clef_rect = clef.get_rect()
        clef_position = StaffUtils.resolve_position_with_margins(staff.position_rect.top_left, clef_settings["margins"])
        clef_rect.center = (clef_position.x, clef_position.y)
        screen.blit(clef, clef_rect)
        return clef_position
    
    """
        Draws the time signature specified for the staff
    """
    def draw_time_signature(self, screen, time_signature, position, font_color=(0, 0, 0)):
        time_signature_fonts = supported_time_signatures[time_signature]["symbol"]
        item_size = supported_time_signatures[time_signature]["size"]
        item_margins = supported_time_signatures[time_signature]["margins"]
        item_font = pygame.font.Font(GenericConfig.BRAVURA_FONT_PATH, item_size)        
        time_numerator = item_font.render(time_signature_fonts[0], True, font_color)
        time_denominator = item_font.render(time_signature_fonts[1], True, font_color)
        # Get clef rect to position it
        numerator_rect = time_numerator.get_rect()
        denominator_rect = time_denominator.get_rect()
        numerator_rect.center = (position.x + item_margins[0], position.y + item_margins[1])
        denominator_rect.center = (position.x + item_margins[2], position.y + item_margins[3]  + (item_size // 2))
        screen.blit(time_numerator, numerator_rect)
        screen.blit(time_denominator, denominator_rect)
        return numerator_rect.center, denominator_rect.center

    
    """
        Draws the key signature of the staff
    """
    def draw_key_signature(self, staff, screen, reference_position):
        clef_settings = supported_clef_settings[staff.clef]
        signature_patterns =clef_settings["signature_position_pattern"]
        signature_details = signature_patterns[staff.key_signature]
        modulation_name, modulation_details = StaffUtils.find_key_signature_modulation(staff.key_signature, supported_modulations)
        modulation_font_code = modulation_details["font_code"]
        modulation_font_size =  modulation_details["font_size"]
        modulation_item_index = 1
        last_modulation_x_offset = 0 # needed to position next item (time signature)
        
        for pattern in signature_details:
            signature_item_positioning = next(iter(pattern.values()))
            staff_item_type = signature_item_positioning[0] # line/interval
            staff_item_position = None

            if staff_item_type == self.STAFF_ITEM_LINE: # line
                staff_item_position = StaffUtils.get_signature_item_coordinates_for_line(StaffConfig.STAFF_LINE_GAP, modulation_item_index,
                                                                modulation_font_size, staff.lines, signature_item_positioning[1], 
                                                                self.MODULATION_SPACING, reference_position.x)
            elif staff_item_type == self.STAFF_ITEM_INTERVAL: # interval
                staff_item_position = StaffUtils.get_signature_item_coordinates_for_interval(StaffConfig.STAFF_LINE_GAP, modulation_item_index,
                                                                                   modulation_font_size, staff.lines,
                                                                                   staff.intervals, signature_item_positioning[1], self.MODULATION_SPACING, reference_position.x)

            signature_position = (staff_item_position.x, staff_item_position.y)
            self.draw_modulation(screen, modulation_font_code, staff_generic_settings["MODULATION_FONT_SIZE"],
                                 signature_position)
            modulation_item_index += 1
            last_modulation_x_offset = staff_item_position.x

        return last_modulation_x_offset
    
    def draw_modulation(self, screen, modulation_font_code, modulation_font_size, position, modulation_color=(0, 0, 0)):
        modulation_font = pygame.font.Font(GenericConfig.BRAVURA_FONT_PATH, modulation_font_size)
        modulation = modulation_font.render(modulation_font_code, True, modulation_color)
        # Get clef rect to position it
        modulation_rect = modulation.get_rect()
        modulation_rect.center = position
        screen.blit(modulation, modulation_rect)