
from Configs.screen_config import Color


class MenuItemStateStep:

    def __init__(self, identifier:str, label:str, tooltip:str, next_step, background_color:Color, 
                 text_color:Color, click_action:callable, hover_action:callable=None):
        self.identifier = identifier
        self.label = label
        self.tooltip = tooltip
        self.click_action = click_action
        self.hover_action = hover_action
        self.next_step = next_step
        self.background_color = background_color
        self.text_color = text_color

    def set_next_step(self, step):
        self.next_step = step

    def get_next_step(self):
        return self.next_step
    
    def set_colors(self, background_color, text_color):
        self.background_color = background_color
        self.text_color = text_color

    def __str__(self):
        return f"MenuItemStateStep(id:{self.identifier}, label:{self.label}, tooltip:{self.tooltip}, bg_color:{self.background_color}, text_color:{self.text_color})"