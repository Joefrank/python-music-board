from typing import List
from Configs.screen_config import MenuItemConfig, MainMenuConfig
from Models.Menu.MainMenu import MainMenu
from Models.Menu.MenuItem import MenuItem
from Models.Menu.MenuData import MenuData
from Models.Position import Position

class MenuBuilder:

    def __init__(self):
        self.main_menu = MainMenu()

    def build_items(self, items_data:List[MenuData]):
        for data in items_data:
            menu_item = MenuItem(data.text, data.tooltip, data.click_action, 
                                 MenuItemConfig.BACKGROUND_COLOR, MenuItemConfig.TEXT_COLOR,
                                 MenuItemConfig.HOVER_COLOR, MenuItemConfig.SELECTED_COLOR)
            self.main_menu.add_item(menu_item)
        return self

    def set_menu_position(self, position:Position):
        self.main_menu.position = position
        return self
    
    def set_item_positions(self):
        no_of_items = len(self.main_menu.items)
        if no_of_items < 1:
            return None
        margin = MainMenuConfig.WIDTH // 100 #margin between menu items
        spacing = no_of_items * margin
        item_used_width = (MenuItemConfig.WIDTH * no_of_items) + spacing + margin
        padding_width = (MainMenuConfig.WIDTH - item_used_width) // 2 
        count = 0
        for item in self.main_menu.items:
            x = self.main_menu.position.x + padding_width + (count * (MenuItemConfig.WIDTH + margin))
            y = self.main_menu.position.y + ((MainMenuConfig.HEIGHT - MenuItemConfig.HEIGHT) // 2)
            item.position = Position(x,y)
            print(f"item pos:{item.position}")
            count += 1 
        return self

    def build(self): 
        self.main_menu.background_color = MainMenuConfig.BACKGROUND_COLOR
        self.main_menu.width = MainMenuConfig.WIDTH
        self.main_menu.height = MainMenuConfig.HEIGHT
        self.main_menu.item_width = MenuItemConfig.WIDTH
        self.main_menu.item_height = MenuItemConfig.HEIGHT
        return self.main_menu