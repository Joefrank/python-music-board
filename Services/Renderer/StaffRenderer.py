import pygame
import math
from datetime import datetime
from Models import GrandStaff, MusicScore
from Models.Position import Position
from Configs.music_config import supported_clef_settings, supported_time_signatures, supported_modulations
from Configs.screen_config import GenericConfig, StaffConfig, staff_generic_settings
from Models.Staff import Staff
from Services.Utils import StaffUtils


class StaffRenderer:

    def __init__(self, state):
        self.start_time = datetime.now().time()        
        self.MODULATION_SPACING = 6
        self.STAFF_ITEM_LINE = 0
        self.STAFF_ITEM_INTERVAL = 1
        self.music_score = None
        self.state = state
        self.Grey = (100, 100, 100)
        
    def render_music_score(self, screen, music_score):
        for staff in music_score.staves_sequence:
            if  isinstance(staff, GrandStaff):
                self.render_grand_staff(staff, screen)
            elif isinstance(staff, Staff):
                self.render_staff(staff, screen)
        highest_y_offset = self.render_score_credit(screen, music_score)
        position = Position(music_score.top_left_position.x, highest_y_offset - 60)
        self.render_score_title(music_score.title, position, music_score.score_width, screen)
    
    def render_score_credit(self, screen, score):
        score_credit = score.credits
        top_left = score.top_left_position
        score_width = score.score_width
        column_width = math.ceil(score_width / len(score_credit))
        no_of_columns = len(score_credit)
        font_size = 20
        highest_y_offset = top_left.y # this is used to set title position

        for i in range(no_of_columns):           
            score_credit[i].reverse()
            reversed_array = score_credit[i]
            if i == no_of_columns -1: # align text to right in this case
                text_alignment="RIGHT"
                x_offset = top_left.x + score_width
            else:
                text_alignment="LEFT"
                x_offset = top_left.x + (i * column_width)

            for y in range(len(reversed_array)): 
                position = Position(x_offset, top_left.y - (y * font_size) - 30)  
                if position.y < highest_y_offset:
                    highest_y_offset = position.y             
                self.draw_text(screen, reversed_array[y], position, font_size, text_alignment=text_alignment)
                
        return highest_y_offset
    
    def render_score_title(self, title, position, container_width, screen):
        font_size = 40
        self.draw_text(screen, title, position, font_size, container_width, text_alignment="CENTER")

    def render_grand_staff(self, grand_staff, screen):
        previous_staff = None
        for staff in grand_staff.staves:
            self.render_staff(staff, screen)
            if previous_staff is not None:
                self.bind_staves(previous_staff, staff, screen)
            previous_staff = staff

    def bind_staves(self, top_staff, bottom_staff, screen):
        self.draw_line_from_point(top_staff.top_position, bottom_staff.top_position, screen, thickness=2)

    def render_staff(self, staff, screen): 
        for line in staff.lines:
            self.draw_line(line, screen)            
            self.draw_line_collaterals(screen, line)

        self.draw_staff_boundaries(staff, screen)        
        clef_position = self.draw_staff_clef(screen, staff)
        #print(f"clef position: {clef_position}")
        key_signature_position = Position(clef_position.x + 20, clef_position.y)
        last_offset_x = self.draw_key_signature(staff, screen, key_signature_position)
        self.draw_time_signature(screen, staff.time_signature, Position(last_offset_x + 30, staff.top_position.y))

    """
        Draws any items in ApplicationState that collide with the line
    """
    def draw_line_collaterals(self, screen, line):
        if self.state.current_mouse_over_position is None:
            return 
        
        if line.contains_position(self.state.current_mouse_over_position):
            self.render_mouse_tracker(screen, self.state.current_mouse_over_position)
            self.state.previous_mouse_over_position = self.state.current_mouse_over_position
            self.state.current_mouse_over_position = None

    def render_mouse_tracker(self, screen, position):
        pygame.draw.circle(screen, self.Grey, position.get_tuple(), 5)

    def draw_staff_boundaries(self, staff, screen):
        #print(f"{staff.position_rect}")
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
            #print((position.x + text_block_x, position.y))
        else:
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