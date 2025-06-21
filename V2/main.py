import pygame

# Default colours, commonly used special characters:
COLOURS = { #Shorthand names for colours
    "BLACK":(0,0,0),
    "BLUE":(0,0,170),
    "GREEN":(0,170,0),
    "CYAN":(0,170,170),
    "RED":(170,0,0),
    "MAGENTA":(170,0,170),
    "ORANGE":(170,85,0),
    "LGREY":(170,170,170),
    "GREY":(85,85,85),
    "LBLUE":(85,85,255),
    "LGREEN":(85,255,85),
    "LCYAN":(85,255,255),
    "LRED":(255,85,85),
    "LPURP":(255,85,255), 
    "YELLOW":(255,255,85), 
    "WHITE":(255, 255, 255)
    }
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

pygame.init()


# Graphics management objects:
class GridTile:
    def __init__(self, fg:str, bg:str, hi:str, hi_bg:str, x:int, y:int) -> None:
        self.char = " "
        self.fg = fg # text colour
        self.bg = bg # Background colour
        self.hi = hi # Highlighted text Colour
        self.hi_bg = hi_bg # Highlighted Background Colour
        self.highlighted = False
        self.location = [x,y]
        # Function related:
        self.function = None
        self.func_args = None

        
    def change_char(self, char = None, fg = None, bg = None, hi = None, hi_bg = None)-> None:
        # Change character and colours, all in one!!!!
        if char:
            self.char = char[0]
        if fg:
            self.fg = fg
        if bg:
            self.bg = bg
        if hi:
            self.hi = hi
        if hi_bg:
            self.hi_bg = hi_bg

    def toggle_highlight(self)-> bool:
        self.highlighted = not self.highlighted
        return self.highlighted
    
    def set_function(self, new_func = None, new_args = None)-> None:
        if new_func:
            self.function = new_func
        if new_args != None:
            self.func_args = new_args
    
    def clear_function(self, just_args:bool = False)-> None:
        if not just_args:
            self.function = None
        self.func_args = None
    
    def activate(self, args = None) -> None:
        if self.function == None:
            return # No assigned function.
        # Fires the assigned function
        if args != None:
            self.function(*args)
        elif self.func_args:
            self.function(*self.func_args)
        else:
            self.function()


class GridManager:
    def __init__(self, columns, rows) -> None:
        self.font = pygame.font.Font("ibmfont.ttf", 32) # Default font.
        self.tile_size = self.font.size(" ")
        self.columns = columns
        self.rows = rows
        self.grid = []
        self.default_fg = "WHITE"
        self.default_bg = "BLUE"
        self.default_hi = "BLACK"
        self.default_hi_bg = "ORANGE"
        
        # Use our functions to build the grid and the surface itself.
        self.build_grid()
        self.build_surface()
        
    # Funcs related to construction or changing of grid itself:

    def build_surface(self):
        # (re)builds surface based on font parameters. Call any time you change font parameters (size, etc.)
        surf_size = [self.tile_size[0] * self.columns, self.tile_size[1] * self.rows]
        print(surf_size)
        self.surface = pygame.Surface(surf_size)
        
    def build_grid(self):
        # (re)builds the grid of tiles, using the default fg/bg colour.
        # Build our grid
        for col in range(self.columns):
            self.grid.append([])
            for row in range(self.rows):
                self.grid[col].append(GridTile(self.default_fg, self.default_bg, self.default_hi, self.default_hi_bg, col, row))


    def change_default_colours(self, new_fg = None, new_bg = None, new_hi = None, new_hi_bg = None):
        # Sets the default colours to the new values, and updates any grid tiles that are using the old defaults.
        old_fg = False
        old_bg = False
        old_hi = False
        old_hi_bg = False

        if new_fg:
            old_fg = self.default_fg
            self.default_fg = new_fg
        if new_bg:
            old_bg = self.default_fg
            self.default_bg = new_bg
        if new_hi:
            old_hi = self.default_hi
            self.default_hi = new_hi
        if new_hi_bg:
            old_hi_bg = self.default_hi_bg
            self.default_hi_bg = new_hi_bg
        for col in self.grid:
            for tile in  col:
                if tile.fg == old_fg:
                    tile.fg = new_fg
                if tile.bg == old_bg:
                    tile.bg = new_bg
                if tile.hi == old_hi:
                    tile.hi = new_hi
                if tile.hi_bg == old_hi_bg:
                    tile.hi_bg = new_hi_bg


    # Drawing functions:

    def draw_square(self, area:pygame.Rect, char = None, fg = None, bg = None, hi = None, hi_bg = None, func = None, func_args = None):
        # Draws a square, and sets the assigned function. If function/arguments are None, the function is cleared.


        # If colours aren't specified, use defaults:
        if fg == None:
            fg = self.default_fg
        if bg == None:
            bg = self.default_bg
        if hi == None:
            hi = self.default_hi
        if hi_bg == None:
            hi_bg = self.default_hi_bg
        if char == None:
            char = " " # assume we want to blank it.
        
        for col in self.grid:
            for tile in col:
                if area.collidepoint(tile.location):
                    tile.change_char(char, fg, bg, hi, hi_bg)
                    # Reset the function:
                    tile.clear_function()
                    tile.set_function(func, func_args)

    def set_char(self, x, y, char, fg = None, bg = None, hi = None, hi_bg = None, func = None, func_args = None, clear_old_func = True):
        # Sets the individual grid square's character, and/or the function assigned to it:
        self.grid[x][y].change_char(char, fg, bg, hi, hi_bg)
        if clear_old_func or func:
            self.grid[x][y].clear_function()
        if func:
            self.grid[x][y].set_function(func, func_args)

    def write_string(self, string_to_write:str, origin:list, fg = None, bg = None, hi = None, hi_bg = None, func = None, func_args = None, clear_old_func = True):
        # Writes a string to a series of tiles, optionally changing colour and assigning a function
        if origin[0] >= self.columns or origin[1] >= self.rows:
            print(f"OUT OF BOUNDS! CANNOT PRINT STRING: '{string_to_write}'")
            return

        if "\n" in string_to_write:
            string_to_write = string_to_write.splitlines()[0] # fuck you only one line at a time.
        char_index = 0
        while char_index < len(string_to_write):
            if origin[0] + char_index > self.columns: # don't try to write outside the screen.
                continue
            self.grid[origin[0] + char_index][origin[1]].change_char(string_to_write[char_index], fg, bg, hi, hi_bg)
            if clear_old_func:
                self.grid[origin[0] + char_index][origin[1]].clear_function()
            self.grid[origin[0] + char_index][origin[1]].set_function(func, func_args)
            char_index += 1

    # Interaction stuff:

    def get_tile(self, x, y) -> GridTile:
        # Returns the tile with the index of x, y
        return self.grid[x][y]
    
    # Rendering:
    def update_screen(self) -> pygame.Surface:
        # re-draws each character, returning our surface.
        for col in range(self.columns):
            for row in range(self.rows):
                tile = self.grid[col][row]
                if tile.highlighted:
                    tsurf = self.font.render(tile.char, False, tile.hi, tile.hi_bg)
                else:
                    tsurf = self.font.render(tile.char, False, tile.fg, tile.bg)
                self.surface.blit(tsurf, [self.tile_size[0] * col, self.tile_size[1] * row])
        return self.surface

# State/interactables:

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
    def __init__(self, text, fg = "BLACK", bg = "GREY", hi = "WHITE", hi_bg = "BLACK", shortcut_col = "WHITE") -> None:
        self.text = text
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


class StateManager:
    def __init__(self, grid:GridManager) -> None:
        self.grid = grid
        self.grid_size = [grid.columns, grid.rows-2] # pull out our menu bar and infobar space
        




# Actually running the stuff now:


grid = GridManager(80,30)

running = True
clock = pygame.time.Clock()


screen = pygame.display.set_mode(grid.surface.get_size())
_delta = 0 # time since last frame



while running:
    # Check inputs
    keys = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blank
    screen.fill((0,0,0))
    screen.blit(grid.update_screen(), [0,0])


    pygame.display.flip()
    _delta = clock.tick(60) / 1000
    