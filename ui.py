# Standardized User Interface objects, such as text, buttons, etc.

from pygame import Rect

DRAWTILES = {
    "topleft":"\u2554",
    "topright":"\u2557",
    "bottomleft":"\u255A",
    "bottomright":"\u255D",
    "vertical":"\u2551",
    "horizontal":"\u2550",
    "ttop":"\u2566",
    "tleft":"\u2560",
    "tright":"\u2563",
    "tbottom":"\u2559",
    "tcenter":"\u256C",
    "lightfill":"\u2591",
    "medfill":"\u2592",
    "heavyfill":"\u2593",
    'prog50':"\u258C", # Half full 
    "prog100":"\u2588" # Basically a soace but with the foreground colour.
    }




class MenuItem:
    # An item in a dropdown menu
    def __init__(self, text, shortcut_index:int, func, func_args, fg = "BLACK", bg = "GREY", hi = "WHITE", hi_bg = "BLACK", shortcut_col = "WHITE" )-> None:
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.shortcut_col = shortcut_col
        
        self.text = text
        self.shortcut_index = shortcut_index
        
        self.func = func
        self.func_args = func_args

        self.enabled = False
        self.selected = False
        
class MenuDivider(MenuItem):
    # A divider for segmenting a drop down menu
    def __init__(self, text = "------",  fg="BLACK", bg="GREY", hi="WHITE", hi_bg="BLACK", shortcut_col="WHITE") -> None:
        super().__init__(text, -1, None, None, fg, bg, hi, hi_bg, shortcut_col)


class Menu:
    # One of the drop down menus for the menu bar
    def __init__(self, text, shortcut_index:int, fg = "BLACK", bg = "GREY", hi = "WHITE", hi_bg = "BLACK", shortcut_col = "WHITE" ) -> None:
        self.text = text
        self.shortcut_index = shortcut_index
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.shortcut_col = shortcut_col

        self.expanded = False
        self.expand_width = len(self.text)

        self.children = []
        

    def add_child(self, object:MenuItem):
        self.children.append(object)
        if len(object.text) > self.expand_width:
            self.expand_width = len(object.text)

    def remove_child(self, index):
        self.children.pop(index)
        # Check if we have to adjust the width of our expand area:
        self.expand_width = len(self.text)
        for c in self.children:
            if len(c.text) > self.expand_width:
                self.expand_width = len(c.text)

    def expand(self):
        # There's probably other stuff I'll need to do, but idk what it is yet.
        self.expanded = True

    def collapse(self):
        self.expanded = False
        

class MenuBar:
    # The bar at the top of the screen. Has its own set of default colours. 
    # Not yet implemented: keyboard shortcut stuff.
    def __init__(self, fg = "BLACK", bg = "GREY", hi = "WHITE", hi_bg = "BLACK", shortcut_col = "WHITE") -> None:
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.shortcut_col = shortcut_col # What colour the keyboard shortcut will appear as in a highlighted item.
        self.children = []

    def add_child(self, menu:Menu):
        self.children.append(menu)

    def remove_child(self, menu):
        menu.collapse()
        index = self.children.index(menu)
        self.children.pop(index)

    def expand_menu(self, menu:Menu):
        for m in self.children:
            if m == menu:
                m.expand()
            else:
                m.collapse() # only let one be open at a time.

    def collapse_all(self):
        for m in self.children:
            m.collapse()


class InfoBar:
    def __init__(self, init_text, fg = "LGREY", bg = "BLACK"):
        self.fg = fg
        self.bg = bg
        self.text = init_text



class Content:
    # Generic object for text, parent of all other ui elements.
    def __init__(self, location, text:str, fg = None, bg = None, hi = None, hi_bg = None) -> None:
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.func = None
        self.func_args = None

        self.text_lines = text.splitlines()
        width = 0
        for i in self.text_lines:
            if len(i) > width:
                width = len(i)

        self.area = Rect(location[0], location[1], width, len(self.text_lines))
    


class Window:
    def __init__(self, area:Rect, title, fg = None, bg = None, hi = None, hi_bg = None, border = "LGREY", show_close = False, allow_scroll = True, always_on_top = False):
        self.area = area
        self.viewport = Rect(0,0,self.area.width -2, self.area.height - 2)
        self.children = []

        self.visible = True
        self.always_on_top = always_on_top
        self.allow_scroll = allow_scroll
        self.show_close = show_close
        self.destroy = False


        self.title = title
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.border = border


    def add_child(self, child:Content):
        self.children.append(child)

    def draw(self, target_grid):
        # Draws the window and its contents to the given grid manager

        # start with a blank square
        target_grid.draw_square(self.area, " ", self.fg, self.bg, self.hi, self.hi_bg)
        # Borders:
        target_grid.draw_hline(self.area.topleft, self.area.width, self.border)
        target_grid.draw_hline(self.area.bottomleft, self.area.width, self.border)
        target_grid.draw_vline(self.area.topleft, self.area.height, self.border)
        target_grid.draw_vline(self.area.topright, self.area.width, self.border)
        # corners:
        target_grid.set_char(self.area.left, self.area.top, DRAWTILES["topleft"], self.border)
        target_grid.set_char(self.area.left, self.area.bottom, DRAWTILES["bottomleft"], self.border)
        target_grid.set_char(self.area.right, self.area.top, DRAWTILES["topright"], self.border)
        target_grid.set_char(self.area.right, self.area.bottom, DRAWTILES["bottomright"], self.border)

        # Title bar:
        if len(self.title) > self.area.width - 4:
            draw_title = self.title[0:self.area.width - 5] + "~"
        else:
            draw_title = self.title
        target_grid.write_string(draw_title, [self.area.left + 1, self.area.top], self.bg, self.border)

        if self.show_close:
            target_grid.set_char(self.area.right - 1, self.area.top, "X", fg = "RED", func = self.queue_destroy)

        # Contents:
        
        for child in self.children:
            # Get the child's absolute position
            child_start_x = child.area.left - self.viewport.left + self.area.left + 1
            child_start_y = child.area.top - self.viewport.top + self.area.top + 1
            for y_range in range(child.area.height):
                if child_start_y + y_range < self.area.bottom and child_start_y + y_range > self.area.top:
                    # Only print within the window area
                    for x_range in range(child.area.width):
                        if child_start_x + x_range < self.area.right and child_start_x + x_range> self.area.left:
                            target_grid.set_char(child_start_x + x_range, child_start_y + y_range, child.text_lines[y_range][x_range], child.fg, child.bg, child.hi, child.hi_bg, child.func, child.func_args)



    def queue_destroy(self):
        self.children = []
        self.destroy = True