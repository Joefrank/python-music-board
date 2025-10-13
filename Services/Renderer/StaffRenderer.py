import pygame
import math
from datetime import datetime
from Models import GrandStaff, Interval, MusicScore
from Models.Line import Line
from Models.Position import Position
from Configs.music_config import supported_clef_settings, supported_time_signatures, supported_modulations
from Configs.screen_config import GenericConfig, StaffConfig, staff_generic_settings
from Models.Staff import Staff
from Services.Renderer.BaseRenderer import BaseRenderer
from Services.Utils import StaffUtils


class StaffRenderer(BaseRenderer):

    def __init__(self, state):
        super().__init__(state) 
        self.start_time = datetime.now().time()        
        self.MODULATION_SPACING = 6
        self.STAFF_ITEM_LINE = 0
        self.STAFF_ITEM_INTERVAL = 1
        self.music_score = None
        #self.state = state
        self.Grey = (100, 100, 100)
      
    def render_grand_staff(self, grand_staff, screen):
        previous_staff = None
        for staff in grand_staff.staves:
            self.render_staff(staff, screen)
            if previous_staff is not None:
                self.bind_staves(previous_staff, staff, screen)
            previous_staff = staff

    def bind_staves(self, top_staff, bottom_staff, screen):
        self.draw_line_from_point(top_staff.top_position, bottom_staff.top_position, screen, thickness=2)

    """
        Renders all items like notes on lines and intervals
    """
    def render_staff_all_collaterals(self, screen, staff, last_x_offset):
        for line in staff.lines:
            self.draw_line(line, screen)            
            self.draw_staff_item_collaterals(screen, line, last_x_offset)

        for interval in staff.intervals:
            self.draw_staff_item_collaterals(screen, interval, last_x_offset)

        for line in staff.virtual_lines:
            self.draw_staff_item_collaterals(screen, line, last_x_offset, nearest_staff=staff)            

        for interval in staff.virtual_intervals:
            self.draw_staff_item_collaterals(screen, interval, last_x_offset, nearest_staff=staff)


    def render_staff(self, staff, screen): 
        self.draw_staff_boundaries(staff, screen)        
        clef_position = self.draw_staff_clef(screen, staff)
        key_signature_position = Position(clef_position.x + 20, clef_position.y)
        last_offset_x = self.draw_key_signature(staff, screen, key_signature_position)
        last_offset_x += 30
        _, _, end_offset = self.draw_time_signature(screen, staff.time_signature, Position(last_offset_x, staff.top_position.y))  
        # Collaterals are every music symbols to be drawn on or around the staff. 
        end_offset += 30            
        self.render_staff_all_collaterals(screen, staff, end_offset)

    """
        Draws any items in ApplicationState that collide with the line
    """
    def draw_staff_item_collaterals(self, screen, staff_item, last_item_x_offset, nearest_staff=None):
        if self.state.current_mouse_over_position is None:
            return
        
        if staff_item.mouse_hovering_around(self.state.current_mouse_over_position, StaffConfig.STAFF_ITEM_THRESHOLD):
            self.render_mouse_tracker(screen, self.state.current_mouse_over_position, staff_item.key_id)
            mouse_position = Position(self.state.current_mouse_over_position.x, self.state.current_mouse_over_position.y)           

            if staff_item.is_virtual and nearest_staff is not None:
                moving_factor = 0
                # check if position is top or bottom of staff
                if mouse_position.is_above_position(nearest_staff.top_position):
                    start_position = mouse_position
                    end_position = nearest_staff.top_position
                    moving_factor = 1
                elif mouse_position.is_below_position(nearest_staff.bottom_position):
                    start_position = mouse_position
                    end_position = nearest_staff.bottom_position
                    moving_factor = -1

                if isinstance(staff_item, Line):
                    self.draw_virtual_lines(screen, moving_factor, start_position, nearest_staff, include_colliding_line=True)
                elif isinstance(staff_item, Interval):
                    self.draw_virtual_lines(screen, moving_factor, start_position, nearest_staff)

            self.state.previous_mouse_over_position = self.state.current_mouse_over_position
            self.state.current_mouse_over_position = None
            return self.state.previous_mouse_over_position
        
    """
        Draws all virtual lines from position on top or bottom of staff all the way to it.
        moving_factor: direction in which we draw virtual lines. moving down (1) or up (-1), 
        mouse_position: last recorded position of the mouse (in state), 
        nearest_staff: closest staff to the mouse_position, 
        include_colliding_line: tells if we draw the line on mouse_position (True for lines and False for intervals)
    """
    def draw_virtual_lines(self, screen, moving_factor, mouse_position, nearest_staff, include_colliding_line = False):
        for line in nearest_staff.virtual_lines:# we only draw lines. intervals are visible between lines
            virtual_line_position = Position(mouse_position.x, line.start_position.y)
            # if mouse position is on top of staff
            if ((moving_factor == 1 and line.is_above_position(nearest_staff.top_position) 
                and line.is_below_position(mouse_position))  
                or (include_colliding_line and line.contains_position(mouse_position))): 
                self.draw_virtual_line(screen, virtual_line_position, color=(255,0,0))
            # if the mouse_position is below the staff
            elif ((moving_factor == -1 and line.is_below_position(nearest_staff.bottom_position)
                   and line.is_above_position(mouse_position)) 
                   or (include_colliding_line and line.contains_position(mouse_position))):
                self.draw_virtual_line(screen, virtual_line_position, color=(0,0,255))           

    def render_mouse_tracker(self, screen, position, key_id):
        self.draw_note(screen, self.default_note_duration, key_id, 40, 30, position)


    def draw_staff_boundaries(self, staff, screen):
        #print(f"{staff.position_rect}")
        self.draw_line_from_point(staff.position_rect.top_left, staff.position_rect.bottom_left, screen, thickness=2)
        self.draw_line_from_point(staff.position_rect.top_right, staff.position_rect.bottom_right, screen, thickness=2)

    """
        Draws a virtual line at the top or bottom of the staff
        line: the line matching/holding our point/position
        position: the center of our virtual line (mouse position) 
    """ 
    def draw_virtual_line(self, screen, position, color=(0, 0, 0), thickness=1, specified_line_width=20):            
        start_x = position.x - specified_line_width #- (specified_line_width // 2)
        end_x = start_x + specified_line_width
        #print(f"line start: {start_x,position.y} - End: {end_x,  position.y} - mouse position:{position}") 
        pygame.draw.line(screen, color, (start_x, position.y),
                         (end_x,  position.y), thickness) 
  
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
        next_x_offset = position.x + item_size
        return numerator_rect.center, denominator_rect.center, next_x_offset
    
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