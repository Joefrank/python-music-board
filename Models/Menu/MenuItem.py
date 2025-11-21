import pygame
from Configs.screen_config import Color
from Models.Events.MouseListener import MouseListener
from Models.Menu.MenuColorConfig import MenuColorConfig
from Models.Menu.MenuItemState import MenuItemState
from Models.Position import Position


class MenuItem(MouseListener):

    def __init__(self, state:MenuItemState, color_config:MenuColorConfig):
        self.state:MenuItemState = state
        self.position = None
        self.dimensions:pygame.Rect = None   
        self.active = False   
        self.current_step = state.steps[0]  
        self.sub_menu = None 
        self.color_config = color_config

    def set_dimensions(self, dimensions: pygame.Rect):
        self.dimensions = dimensions

    def on_mouse_over(self, mouse_position) -> bool:
        if self.active:
            return 
        if self.dimensions.collidepoint(mouse_position.get_tuple()):
            self.go_to_step_by_id("HoverMM") 
        else:           
            self.go_to_step_by_id("PlayMM")        
        
    def on_mouse_left_click(self, mouse_position) -> bool:
        if self.dimensions.collidepoint(mouse_position.get_tuple()):            
            self.active = not self.active
            self.current_step.click_action(self)
            print(self.current_step)
        
    def set_active(self):
        self.active = True

    def deactivate_item(self):        
        self.active = False 
        self.go_to_next_step()

    def is_active(self):
        return self.active
    
    def is_inactive(self):
        return not self.active 
    
    def get_current_step(self):
        return self.current_step
    
    def go_to_next_step(self):        
        current_index = self.state.steps.index(self.current_step)
        next_index = (current_index + 1) % len(self.state.steps)
        self.current_step = self.state.steps[next_index]

    def go_to_step_by_id(self, step_id:str):
        for step in self.state.steps:
            if step.identifier == step_id:
                self.current_step = step
                break
        
        
       