import pygame
from Configs.screen_config import Color
from Models.Events.MouseListener import MouseListener
from Models.Position import Position


class MenuItem(MouseListener):

    def __init__(self, text, tooltip, click_action, background_color, text_color, hover_color, selected_color):
        self.text = text
        self.tooltip = tooltip
        self.click_action = click_action
        self.unmutable_background = self.background_color = background_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.selected_color = selected_color
        self.position = None
        self.dimensions:pygame.Rect = None   
        self.active = False      

    def set_dimensions(self, dimensions: pygame.Rect):
        self.dimensions = dimensions

    def on_mouse_over(self, mouse_position) -> bool:
        if self.active:
            return        
        self.background_color = self.hover_color \
            if self.dimensions.collidepoint(mouse_position.get_tuple()) \
            else self.unmutable_background
        
    def on_mouse_left_click(self, mouse_position) -> bool:
        if self.dimensions.collidepoint(mouse_position.get_tuple()):
            self.background_color = self.selected_color
            self.click_action(self)
            self.active = True
        
    def deactivate_item(self):
        self.active = False
        self.background_color = self.unmutable_background