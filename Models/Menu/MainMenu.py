from Models.Menu import MenuItem
from Models.Position import Position


class MainMenu:

    def __init__(self):
        self.items = []
        self.background_color = None
        self.width = None
        self.height = None
        self.item_width = None
        self.item_height = None
        self.position = None

    def add_item(self, item: MenuItem):
        self.items.append(item)

    def add_items(self, items):
        self.items = items

    def set_position(self, position:Position):
        self.position = position