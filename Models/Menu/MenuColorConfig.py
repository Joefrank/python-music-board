from Configs.screen_config import Color


class MenuColorConfig:

    def __init__(self, background_color:Color, hover_background_color:Color, selected_background_color:Color, 
                 text_color:Color, text_hover_color:Color=None, text_selected_color:Color=None):
        self.background_color = background_color
        self.text_color = text_color
        self.hover_background_color = hover_background_color
        self.selected_background_color = selected_background_color
        self.text_hover_color = text_color if text_hover_color is None else text_hover_color
        self.text_selected_color = text_selected_color