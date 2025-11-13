import pygame
from Configs.screen_config import Color, MenuItemConfig
from Models.DataModels.ApplicationState import ApplicationState
from Models.Menu import MainMenu
from Models.Position import Position
from Services.Renderer.BaseRenderer import BaseRenderer


class MenuRenderer(BaseRenderer):

    @property
    def main_menu(self):
        return self.state.main_menu

    def __init__(self, state:ApplicationState):
        super().__init__(state)

    def render_menu(self):
        #render the background of menu
        pygame.draw.rect(self.screen, self.main_menu.background_color, 
                         (self.main_menu.position.x, self.main_menu.position.y, 
                          self.main_menu.width, self.main_menu.height))
        #render items here
        for item in self.main_menu.items:
            dimension = item.dimensions
            pygame.draw.rect(self.screen, item.current_step.background_color, 
                             (dimension.left, dimension.top, dimension.width, 
                              dimension.height), border_radius=10)
            text_position = Position(dimension.left, dimension.top + 7)
           
            self.draw_text(self.screen, item.current_step.label, text_position, MenuItemConfig.FONT_SIZE, 
                           dimension.width, font_color = item.current_step.text_color, text_alignment="CENTER")
            
            if item.is_active() and item.sub_menu is not None:
                # render submenu background
                submenu_bg_x = item.sub_menu.position.x
                submenu_bg_y = item.sub_menu.position.y
                submenu_bg_width = item.sub_menu.width
                submenu_bg_height = item.sub_menu.height
                # pygame.draw.rect(self.screen, item.sub_menu.background_color, 
                #                  (submenu_bg_x, submenu_bg_y, submenu_bg_width, submenu_bg_height))
                # render submenu items
                for sub_item in item.sub_menu.items:
                    #print(f"subitem:{sub_item.current_step.label}")
                    # sub_dimension = sub_item.dimensions
                    # pygame.draw.rect(self.screen, sub_item.current_step.background_color, 
                    #                  (sub_dimension.left, sub_dimension.top, sub_dimension.width, 
                    #                   sub_dimension.height), border_radius=8)
                    # sub_text_position = Position(sub_dimension.left, sub_dimension.top + 3)
                    self.draw_text(self.screen, sub_item.current_step.label, item.sub_menu.position, 
                                    MenuItemConfig.FONT_SIZE - 4, item.dimensions.width // 2, 
                                   font_color = Color.BLACK, text_alignment="CENTER")
