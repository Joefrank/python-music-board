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
            pygame.draw.rect(self.screen, item.background_color, 
                             (item.position.x, item.position.y, 
                              self.main_menu.item_width, self.main_menu.item_height), border_radius=20)
            
            text_position = Position(item.position.x, item.position.y + 7)
            self.draw_text(self.screen, item.text, text_position, MenuItemConfig.FONT_SIZE, 
                           self.main_menu.item_width, font_color = Color.WHITE, text_alignment="CENTER")
