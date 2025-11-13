
from Models.Menu.MenuItemStateStep import MenuItemStateStep


class MenuItemState:

    def __init__(self):
        self.steps = []       

    def add_step(self, step:MenuItemStateStep):
        self.steps.append(step)