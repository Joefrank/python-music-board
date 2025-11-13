from typing import List

import pygame
from Configs.screen_config import MenuItemConfig, MainMenuConfig, SubMenuConfig
from Models.DataModels.ApplicationState import ApplicationState
from Models.Menu.MainMenu import MainMenu
from Models.Menu.MenuItem import MenuItem
from Models.Menu.MenuData import MenuData
from Models.Menu.SubMenu import SubMenu
from Models.Position import Position

class MenuBuilder:

    def __init__(self):
        self.main_menu = MainMenu()

    def build_items(self, items_data:List[MenuData]):
        for data in items_data:# data item is made of state and submenu (potentially)
            menu_item = MenuItem(data.menu_item_state, data.color_config)
            if data.submenu_data is not None:
                menu_item.sub_menu = SubMenu(menu_item)
                for sub_menu_item_data in data.submenu_data:
                    sub_menu_item = MenuItem(sub_menu_item_data.menu_item_state, sub_menu_item_data.color_config)
                    menu_item.sub_menu.add_item(sub_menu_item)


            # menu_item = MenuItem(data.text, data.alternate_text, data.tooltip, data.click_action, 
            #                      MenuItemConfig.BACKGROUND_COLOR, MenuItemConfig.TEXT_COLOR,
            #                      MenuItemConfig.HOVER_COLOR, MenuItemConfig.SELECTED_COLOR)
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
        sub_count = 0
        for item in self.main_menu.items:
            x = self.main_menu.position.x + padding_width + (count * (MenuItemConfig.WIDTH + margin))
            y = self.main_menu.position.y + ((MainMenuConfig.HEIGHT - MenuItemConfig.HEIGHT) // 2)
            item.set_dimensions(pygame.Rect(x,y, MenuItemConfig.WIDTH, MenuItemConfig.HEIGHT))           
            count += 1 
            # how about sub-items positions
            if item.sub_menu is not None:
                item.sub_menu.set_position(Position(item.dimensions.x, item.dimensions.y + MainMenuConfig.HEIGHT + MainMenuConfig.PADDING))
                for sub_item in item.sub_menu.items:
                    x = item.dimensions.x + padding_width + (sub_count * (MenuItemConfig.WIDTH // 2) + margin)
                    y = item.dimensions.y + MenuItemConfig.HEIGHT 
                    sub_item.set_dimensions(pygame.Rect(x, y, MenuItemConfig.WIDTH // 2, MenuItemConfig.HEIGHT // 2))
                    sub_count += 1

        return self

    def register_items_listeners(self, state:ApplicationState):
        for item in self.main_menu.items:
            state.mouse_hover.listeners.append(item)
            state.mouse_click.listeners.append(item)
            if item.sub_menu is not None:
                for sub_item in item.sub_menu.items:
                    state.mouse_hover.listeners.append(sub_item)
                    state.mouse_click.listeners.append(sub_item)

        return self

    def build(self): 
        self.main_menu.background_color = MainMenuConfig.BACKGROUND_COLOR
        self.main_menu.width = MainMenuConfig.WIDTH
        self.main_menu.height = MainMenuConfig.HEIGHT
        self.main_menu.item_width = MenuItemConfig.WIDTH
        self.main_menu.item_height = MenuItemConfig.HEIGHT
        for item in self.main_menu.items:
            if item.sub_menu is not None:
                item.sub_menu.background_color = SubMenuConfig.BACKGROUND_COLOR
                item.sub_menu.Height = SubMenuConfig.HEIGHT
                item.sub_menu.item_width = MenuItemConfig.WIDTH // 2
                item.sub_menu.item_height = MenuItemConfig.HEIGHT // 2

        return self.main_menu