class MenuData:
    def __init__(self, text:str, tooltip:str, click_action:callable):
        self.text = text
        self.tooltip = tooltip
        self.click_action = click_action