from Models.Menu.MenuColorConfig import MenuColorConfig
from Models.Menu.MenuItemState import MenuItemState

class MenuData:
    def __init__(self, state:MenuItemState, color_config:MenuColorConfig, submenu_data=None):
        self.menu_item_state = state
        self.submenu_data = submenu_data
        self.color_config = color_config