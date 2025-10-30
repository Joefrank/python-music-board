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

    def set_dimensions(self, dimensions: pygame.Rect):
        self.dimensions = dimensions

    def on_mouse_over(self, mouse_position) -> bool:
        self.set_background_by_event(self.hover_color, mouse_position)

    def on_mouse_left_click(self, mouse_position) -> bool:
        self.set_background_by_event(self.selected_color, mouse_position)

    def set_background_by_event(self, color: Color, mouse_position:Position):
        self.background_color = color \
            if self.dimensions.collidepoint(mouse_position.get_tuple()) \
            else self.unmutable_background
