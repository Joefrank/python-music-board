from Models.Menu import MainMenu
from Models.Menu.MainMenu import MainMenu
from Models.Menu.MenuItem import MenuItem


class SubMenu(MainMenu):

    def __init__(self, parent:MenuItem):
        super().__init__()
        self.parent:MenuItem = parent