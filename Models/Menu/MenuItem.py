from Models.Position import Position


class MenuItem:

    def __init__(self, text, tooltip, click_action, background_color, text_color, hover_color, selected_color):
        self.text = text
        self.tooltip = tooltip
        self.click_action = click_action
        self.background_color = background_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.selected_color = selected_color
        self.position = None

    def set_position(self, position:Position):
        self.position = position