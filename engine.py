import pygame
from ui import *

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


    


class Cursor:
    def __init__(self, maxrange):
        self.position = [0,0]
        self.bg = "ORANGE"
        self.fg = "BLACK"
        self.follow_mouse = True
        self.allow_blink = False # If False, cursor is always visible, set to True for text entry or w/e
        self.blink_timer = 0
        self.blink_speed = 500
        self.is_blinked = False # Is it hidden but blinking
        self.visible = True
        self.maxrange = maxrange
        self.held = False

    def move(self, vector_x = 0, vector_y = 0) -> list:
        # Returns old position
        oldpos = self.position.copy()

        self.position[0] += vector_x
        self.position[1] += vector_y
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] > self.maxrange[0]:
            self.position[0] = self.maxrange[0]
        
        if self.position[1] < 0:
            self.position[1] = 0
        elif self.position[1] > self.maxrange[1]:
            self.position[1] = self.maxrange[1]

        return oldpos
        
    def move_to_position(self, x, y)-> list:
        # Moves to a new position, returns the last position.
        start_pos = self.position.copy()
        if x < 0:
            self.position[0] = 0
        elif x > self.maxrange[0]:
            self.position[0] = self.maxrange[0]
        else:
            self.position[0] = x
        if y < 0:
            self.position[1] = 0
        elif y > self.maxrange[1]:
            self.position[1] = self.maxrange[1]
        else:
            self.position[1] = y
        return start_pos

    def blink(self, delta):
        if not self.allow_blink:
            return True
        self.blink_timer += delta
        if self.blink_timer > self.blink_speed * 2:
            self.blink_timer = self.blink_timer - self.blink_speed * 2
            return True
        elif self.blink_timer > self.blink_speed:
            return False
        return True
    
    


# Graphics management objects:
class GridTile:
    def __init__(self, fg:str, bg:str, hi:str, hi_bg:str, x:int, y:int) -> None:
        self.char = " "
        self.fg = fg # text colour
        self.bg = bg # Background colour
        self.location = [x,y]
        # Function related:
        self.function = None
        self.func_args = None
        self.cursor_hi = False 

        
    def change_char(self, char = None, fg = None, bg = None)-> None:
        # Change character and colours, all in one!!!!
        if char:
            self.char = char[0]
        if fg:
            self.fg = fg
        if bg:
            self.bg = bg

    def cursor_state(self, new_state):
        self.cursor_hi = new_state

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
        self.font_supports_progress_bars = False # If your font allows for 1/8th fill characters (unicode 0x2589 -> 0x258F)
        
        
        # Use our functions to build the grid and the surface itself.
        self.build_grid()
        self.build_surface()
        
    # Funcs related to construction or changing of grid itself:

    def build_surface(self):
        # (re)builds surface based on font parameters. Call any time you change font parameters (size, etc.)
        surf_size = [self.tile_size[0] * self.columns, self.tile_size[1] * self.rows]
        self.surface = pygame.Surface(surf_size)
        
    def build_grid(self):
        # (re)builds the grid of tiles, using the default fg/bg colour.
        # Build our grid
        for col in range(self.columns):
            self.grid.append([])
            for row in range(self.rows):
                self.grid[col].append(GridTile(self.default_fg, self.default_bg, self.default_hi, self.default_hi_bg, col, row))


    def change_default_colours(self, new_fg:str|None = None, new_bg:str|None = None, new_hi:str|None = None, new_hi_bg:str|None = None):
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

    def draw_square(self, area:pygame.Rect, 
                    char:str|None = None, fg:str|None = None, bg:str|None = None, 
                    func = None, func_args:list|tuple|None = None):
        # Draws a square, and sets the assigned function. If function/arguments are None, the function is cleared.


        # If colours aren't specified, use defaults:
        if fg == None:
            fg = self.default_fg
        if bg == None:
            bg = self.default_bg
        if char == None:
            char = " " # assume we want to blank it.
        
        for col in self.grid:
            for tile in col:
                if area.collidepoint(tile.location):
                    tile.change_char(char, fg, bg)
                    # Reset the function:
                    tile.clear_function()
                    tile.set_function(func, func_args)

    def set_char(self, x:int, y:int, char:str, fg:str|None = None, bg:str|None = None, func = None, func_args:list|tuple|None = None, clear_old_func = True):
        # Sets the individual grid square's character, and/or the function assigned to it:
        self.grid[x][y].change_char(char, fg, bg)
        if clear_old_func or func:
            self.grid[x][y].clear_function()
        if func:
            self.grid[x][y].set_function(func, func_args)
            

    def write_string(self, string_to_write:str, origin:list|tuple, fg = None, bg = None, func = None, func_args = None, clear_old_func = True):
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
            self.grid[origin[0] + char_index][origin[1]].change_char(string_to_write[char_index], fg, bg)
            if clear_old_func:
                self.grid[origin[0] + char_index][origin[1]].clear_function()
            self.grid[origin[0] + char_index][origin[1]].set_function(func, func_args)
            char_index += 1

    def write_infobar_string(self, left_text:str, right_text:str):
        # We already know what the infobar will be so just do this ding dang thang.
        char_index = 0
        while char_index < len(left_text) or len(right_text):
            if char_index < len(left_text):
                self.grid[char_index][self.rows - 1].change_char(left_text[char_index])
            if char_index < len(right_text):
                self.grid[self.columns - len(right_text) + char_index][self.rows - 1].change_char(right_text[char_index])
            char_index += 1

    def draw_hline(self, start, width, fg = None, bg = None, hi = None, hi_bg = None, char = DRAWTILES["horizontal"]):
        # Draws a horizontal line
        for i in range(width):
            self.grid[start[0] + i][start[1]].change_char(char, fg, bg)
        

    def draw_vline(self, start, height, fg = None, bg = None, hi = None, hi_bg = None, char = DRAWTILES["vertical"]):
        # Draws a vertical line
        for i in range(height):
            self.grid[start[0]][start[1] + i].change_char(char, fg, bg)
        

    def blank(self):
        # Fills the grid with default colour, space as a character.
        for x in self.grid:
            for y in x:
                y.change_char(" ", self.default_fg, self.default_bg)
    # Interaction stuff:

    def get_tile(self, x, y) -> GridTile:
        # Returns the tile with the index of x, y
        return self.grid[x][y]
    

    # Rendering:
    def update_screen(self, state) -> pygame.Surface:
        # re-draws each character, returning our surface.
        for col in range(self.columns):
            for row in range(self.rows):
                tile = self.grid[col][row]
                if tile.cursor_hi:
                    tsurf = self.font.render(tile.char, False, COLOURS[state.cursor.fg], COLOURS[state.cursor.bg])
                else:
                    tsurf = self.font.render(tile.char, False, COLOURS[tile.fg], COLOURS[tile.bg])
                self.surface.blit(tsurf, [self.tile_size[0] * col, self.tile_size[1] * row])
        return self.surface

# State/interactables:

class StateManager:
    # Manages windows, menus, cursor, etc. 
    def __init__(self, grid:GridManager) -> None:
        self.grid = grid
        self.grid_size = [grid.columns, grid.rows-2] # pull out our menu bar and infobar space
        self.windows = []
        self.menubar = MenuBar()
        self.infobar = InfoBar("V0.2", [self.grid.columns, self.grid.rows])
        self.cursor = Cursor([self.grid.columns-1, self.grid.rows - 2])
        self.key_mode = 0
        self.run = True # Do we kill the process?
        self.input_target = None # What object are we targeting keyboard inputs to?
        

    # Windows:

    def add_window(self, window:Window):
        self.windows.append(window)
        # maybe do some stuff around management in here?

    def draw_windows(self, delta):
        for win in self.windows:
            win.draw(self.grid, delta)


    def purge_windows(self):
        # Close any windows that are flagged as open
        if len(self.windows) >= 1:
            for w in self.windows:
                if w.destroy:
                    self.windows.remove(w)

    # Menu Bar:

    def draw_menu_bar(self):
        self.grid.draw_hline([0,0], self.grid.columns, self.menubar.fg, self.menubar.bg, self.menubar.hi, self.menubar.hi_bg, char= " ")
        for menu in self.menubar.children:
            if not menu.expanded:
                self.grid.write_string(menu.text, menu.area.topleft, func = self.menubar.expand_menu, func_args=[menu])
                self.grid.get_tile(menu.area.left + menu.highlight_char, menu.area.top).change_char(fg=menu.hi)
            else:
                self.grid.write_string(menu.text, menu.area.topleft, func = menu.collapse, func_args=None, fg = menu.hi, bg = menu.hi_bg)

                for child in menu.children:
                    if child.hovered:
                        self.grid.draw_square(Rect(menu.area.left - 1, child.index + 1, menu.expand_width + 1, 1), fg = menu.hi, bg = menu.hi_bg, func=child.action)
                    else:
                        self.grid.draw_square(Rect(menu.area.left - 1, child.index + 1, menu.expand_width + 1, 1), fg = menu.fg, bg = menu.bg, func=child.action)
                    self.grid.write_string(child.text, [menu.area.left, child.index + 1], clear_old_func= False)
                    self.grid.set_char(menu.area.left + child.highlight_char, child.index + 1, child.text[child.highlight_char], child.hi, clear_old_func=False)


    def add_menu(self, menu:Menu):
        self.menubar.add_child(menu)

    def draw_infobar(self):
        self.grid.draw_hline([0,self.grid.rows-1], self.grid.columns, fg = self.infobar.fg, bg = self.infobar.bg, char = " ")
        self.grid.write_infobar_string(self.infobar.left_text, self.infobar.right_text)
    
    # Cursor Stuff:

    def move_cursor(self, vector_x, vector_y):
        self.grid.get_tile(self.cursor.position[0], self.cursor.position[1]).cursor_hi = False
        self.cursor.move(vector_x, vector_y)
        

    def cursor_blink(self, delta):
        curs_tile = self.grid.get_tile(self.cursor.position[0], self.cursor.position[1])
        curs_tile.cursor_hi = self.cursor.blink(delta)


    # Input:           
    def handle_keypress(self, key):
        # This is our big master list of key press options
        # If you're subclassing, consider passing to this from another input handling function to avoid having to redeclare all of this
        # These are just "suggested" key shortcuts.
        if self.key_mode == 0:
            if key == pygame.K_ESCAPE: # TEMP: exit the game on escape.
                self.run = False
                print("BYE BYE (escape pressed)")
            if key == pygame.K_UP:
                self.move_cursor(0,-1)
            if key == pygame.K_DOWN:
                self.move_cursor(0,1)
            if key == pygame.K_LEFT:
                self.move_cursor(-1,0)
            if key == pygame.K_RIGHT:
                self.move_cursor(1,0)

            if key == pygame.K_RETURN or key == pygame.K_KP_ENTER or key == pygame.K_SPACE:
                tile = self.grid.get_tile(self.cursor.position[0], self.cursor.position[1])
                tile.activate()
            
            self.unhandled_input(key)
        elif self.key_mode == 1 and self.input_target:
            if key == pygame.K_RETURN:
                if self.input_target.allow_linebreak:
                    self.input_target.add_linebreak()
                else:
                    self.release_input_target()
            if key == pygame.K_BACKSPACE:
                self.input_target.do_backspace()
            if key == pygame.K_UP:
                self.input_target.move_cursor(y=-1)
            if key == pygame.K_DOWN:
                self.input_target.move_cursor(y=1)
            if key == pygame.K_LEFT:
                self.input_target.move_cursor(x=-1)
            if key == pygame.K_RIGHT:
                self.input_target.move_cursor(x=1)
            if key == pygame.K_TAB:
                pass # select next control??


    def event_handler(self, event_list):
        for event in event_list:
            if event.type == pygame.TEXTINPUT and self.input_target:
                self.input_target.text_input(event.text)
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                self.handle_keypress(event.key)
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                self.mouse_moved(mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.key_mode == 1 and self.input_target:
                    self.release_input_target()
                self.mouse_released(event)

    def set_input_target(self, control):
        self.input_target = control
        self.key_mode = 1 # Switch to input passthrough.
        control.refresh_contents()
        #TODO: move the cursor.


    def unhandled_input(self, key):
        pass # Replace this in your subclass if you need to add other input stuff.


    def mouse_moved(self, mouse_pos):
        if self.cursor.follow_mouse:
            mouse_x = mouse_pos[0] // self.grid.tile_size[0]
            mouse_y = mouse_pos[1] // self.grid.tile_size[1]
            move = self.cursor.move_to_position(mouse_x, mouse_y)
            self.grid.get_tile(move[0], move[1]).cursor_hi = False
            
        

    def mouse_released(self, m_event):
        mouse_x = m_event.pos[0] // self.grid.tile_size[0]
        mouse_y = m_event.pos[1] // self.grid.tile_size[1]
        mouse_tile = self.grid.get_tile(mouse_x, mouse_y)
        mouse_tile.activate()

    def check_cursor_intersects(self):
        # Check if we are hovering on a control, and if that control wants to highlight on hover
        for w in self.windows:
            for control in w.children:
                if control.hi_on_hover and control.absolute_area.collidepoint(self.cursor.position):
                    control.highlighted = True
                else:
                    control.highlighted = False
                
    def release_input_target(self):
        if self.input_target:
            self.input_target.release_focus()
            self.input_target = None
            self.key_mode = 0

    # Logic:
    def tick(self, delta):
        # Basic draw logic, todo: add game update here.
        # Game logic lives here:
        self.program_logic(delta)


        # Reset our canvas, clear out dead windows
        self.grid.blank()
        self.purge_windows()

        # Cursor position stuff:
        self.check_cursor_intersects()

        self.draw_windows(delta)

        self.draw_menu_bar()

        self.cursor_blink(delta)
    
        self.draw_infobar()

    
    def program_logic(self, delta):
        pass # Replace with any subclassed logic stuff you want to do
    def quit(self):
        self.run = False
