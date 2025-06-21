import pygame
from pygame import Rect
from ui import Window, MenuBar, MenuBarMenu, MenuItem, MenuItemDivider, InfoBar
import gamedata

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
    "heavyfill":"\u2593"
    }


# Parent class for screen data. This will be what controls windows, etc.
class ScreenState:
    def __init__(self, display, focus_text = "WHITE", unfocus_text = "LGREY", background = "BLUE", highlight_bg = "ORANGE", highlight_text = "BLACK")-> None:
        self.parent_display = display
        
        # Colour defaults
        self.focus_colour = focus_text
        self.unfocus_colour = unfocus_text
        self.background_colour = background
        self.highlight_bg_colour = highlight_bg
        self.highlight_txt_colour = highlight_text
        
        # Window management
        self.max_window_size = (display.columns-2, display.rows-3)
        self.windows = []
        self.active_window = 0 # Index of the active window in our window list

        # Menu bar, etc.:
        self.menubar = MenuBar()
        self.title_menus = {}

    def add_window(self, window:Window) -> None:
        # Adds a window to the screen state.
        if window.area.width > self.max_window_size[0] or window.area.height > self.max_window_size[1]:
            print(f"Window out of bounds! Unable to add window! {window.title}")
            return 
        self.active_window = len(self.windows) # Mark it as our active window.
        self.windows.append(window)

    def remove_window(self, window):
        windex = self.windows.index(window)
        self.windows[windex].queue_destroy()
        self.windows.pop(windex)

    def add_menu(self, menu_title) -> None:
        self.title_menus[menu_title] = self.menubar.add_child_menu(menu_title)

    def remove_menu(self, menu_title) -> None:
        self.menubar.remove_child(self.title_menus.pop(menu_title))

    def get_windows(self) -> list:
        # Returns a list of the windows, with the active one as the last entry
        outlist = []
        for w in range(len(self.windows)):
            if w != self.active_window:
                outlist.append(self.windows[w])
        outlist.append(self.windows[self.active_window])
        return outlist
    

    def tick(self, delta):
        pass

    def get_cursor_action(self, cursor_pos) -> list:
        # Check our windows and menu bar objects to see what the cursor is covering.
        # Returns a list of [function, **args]
        return [None, None]

# Cursor
class Cursor:
    def __init__(self, font_size, parent):
        self.position = [0,0] # position on the grid
        self.absolute_position =  Rect(self.position[0] * font_size[0], self.position[1] * font_size[1], font_size[0] , font_size[1])
        self.font_size = font_size
        self.max_area = [parent.columns - 1, parent.rows - 2] # keep the cursor in the window, minus the infobox
        self.bg = "ORANGE"
        self.fg = "WHITE"
        self.char = DRAWTILES["medfill"]
        self.show = True # If we should bother drawing it at all.
        self.blink = False
        self.blink_period = 400 # ms per blink
        self.blink_counter = 0 # running count of blinker
        self.action = None # What will the cursor do when activated
        self.action_parent = None # What object owns the action
        self.parent_screen = parent

    def get_abs_pos(self) -> Rect:
        # returns a rectangle of the cursor's absolute position in the window, probably good for mouse following?
        # assuming we are using half-width fonts
        self.absolute_position = Rect(self.position[0] * self.font_size[0], self.position[1] * self.font_size[1], self.font_size[0] , self.font_size[1])
        return self.absolute_position

    def update_blink(self, delta):
        if not self.blink:
            return False
        # says if we need to blink or not
        self.blink_counter += delta
        if self.blink_counter > self.blink_period * 2: # if we wrap around
            self.blink_counter = self.blink_counter - self.blink_period * 2
        elif self.blink_counter > self.blink_period:
            return True
        return False 

    def move_cursor(self, direction_vectors):
        # Moves the cursot position in the given direction by the given magnitude
        # Returns True if successful, false if it hits a barrier
        valid_move = True
        self.position[0] += direction_vectors[0]
        if self.position[0] < 0:
            self.position[0] = 0
            valid_move = False
        elif self.position[0] > self.max_area[0]:
            self.position[0] = self.max_area[0]
            valid_move = False
        self.position[1] += direction_vectors[1]
        if self.position[1] < 0:
            self.position[1] = 0
            valid_move = False
        if self.position[1] > self.max_area[1]:
            self.position[1] = self.max_area[1]
            valid_move = False
        return valid_move


    def determine_interaction(self, objects) -> None:
        # 
        # Takes a list of objects the cursor intersects, and determines which one has priority.
        if objects == []:
            self.action = [None, None]
            self.action_parent = None
        else: 
            self.action = [objects[-1].action, objects[-1].action_args]
            self.action_parent = objects[-1]


    def fire_action(self):
        if self.action and self.action[0] != None:
            
            if self.action[1]:
                self.action[0](*self.action[1])
            else:
                self.action[0]()

            if type(self.action_parent) == MenuItem and self.action_parent.close_menu_on_select:
                self.action_parent.parent_menu.collapse()
        self.parent_screen.check_cursor_intersects() # Refresh possible interactions.

# Grid data objects

class GridTile:
    def __init__(self, font, character = " ", bg = "BLUE", fg = "WHITE") -> None:
        self.character = character
        self.bg = COLOURS[bg]
        self.fg = COLOURS[fg]
        self.blink = False
        self.highlighted = False
        self.font = font
        self.surface = font.render(character, 0, self.bg, self.fg)
        self.changed = True # Do we need to redraw the tile?
        self.highlight_fg = "WHITE"
        self.highlight_bg = "ORANGE"
        self.cursor_highlighted = False
        self.cursor_highlight_col = "ORANGE" # what colour to use if we highlight with the cursor
        self.cursor_blink = False
    
    def get_surface(self) -> pygame.Surface:
        # Returns the tile's surface data:
        if self.cursor_highlighted and self.cursor_blink:
            self.surface = self.font.render(DRAWTILES["medfill"], 0, self.highlight_fg, self.cursor_highlight_col)
        elif self.cursor_highlighted:
            self.surface = self.font.render(self.character, 0, self.highlight_fg, self.highlight_bg)
        elif self.highlighted:
            self.surface = self.font.render(self.character, 0, self.highlight_fg, self.bg)
        else:
            self.surface = self.font.render(self.character, 0, self.fg, self.bg)
        self.changed = False # flag it has having been read
        return self.surface
    
    def enable_highlight(self, fg = None, bg = None):
        # Toggle highlighting and change highlight colour if desired
        if fg != None:
            self.highlight_fg = fg
        if bg != None:
            self.highlight_bg = bg
        self.highlighted = True
        self.changed = True
    
    def disable_highlight(self):
        self.highlighted = False
        self.changed = True

    def enable_cursor_highlight(self, new_col = False):
        if new_col:
            self.cursor_highlight_col = new_col
        self.cursor_highlighted = True
        self.changed = True

    def disable_cursor_highlight(self):
        self.cursor_highlighted = False
        self.changed = True

    def toggle_cursor_blink(self, state):
        if self.cursor_blink != state:
            self.cursor_blink = state
            self.changed = True

    def set_character(self, character, fg = None, bg = None) -> bool:
        # Change the tile's character
        # Returns True if character changes
        if fg or bg:
            self.set_colour(fg, bg)
        if self.character != character:
            self.character = character
            self.changed = True
            return True
        return False

    def set_colour(self, fg = None , bg = None) -> bool:
        # update tile colour data
        # Returns true if colour changes
        changed = False
        if self.bg != bg and bg != None:
            self.bg = COLOURS[bg]
            changed = True
        if self.fg != fg and fg != None:
            self.fg = COLOURS[fg]
            changed = True
        if changed:
            self.changed = True
            return True
        return False # no changes made
    
# Main screen stuff, how it renders

class ScreenRenderer:
    # Object which handles the display itself. Responsible for managing menus, and returning the image data so the engine can draw to the screen.
    def __init__(self, columns, rows, font) -> None:
        self.font = font # for now, use a default font, change when we care about screen resizing.
        self.columns = columns
        self.rows = rows
        self.grid = []
        self.refresh_all = False # Do we need to refresh every tile in the grid?
        self.tilesize = self.font.size(" ") # The font class lets us cheat a bit :)
        self.res = (self.tilesize[0] * self.columns, self.tilesize[1] * self.rows)
        self.surface = pygame.Surface(self.res)
        self.infobar = InfoBar()
        # Cursor stuff:
        self.cursor = Cursor(self.font.size(" "), self)
        self.cursor_action = None
        self.cursor_action_args = [None]
        self.shortcuts = {} # What keyboard shortcuts should do which actions
        
        # Fill the grid with blank spaces.
        self.blank_data = {"char":" ", "fg":"WHITE", "bg":"BLUE"} # Default square data
        for i in range(self.columns):
            self.grid.append([])
            for n in range(self.rows):
                self.grid[i].append(GridTile(font, self.blank_data["char"], fg = self.blank_data["fg"], bg = self.blank_data["bg"]))

        # Then initialize the screen state: 
        self.state = ScreenState(self)
        self.menubar = self.state.menubar


    # menu and info bar setup:

    def load_menu_bar(self, new_bar) -> None:
        self.menubar.clear_children()
        self.menubar = new_bar
        

    # Grid manip/graphics drawing stuff:

    def game_tick(self, delta) -> pygame.Surface:
        # Polls each cell and blits its character to the correct place in our holding screen
        # Returns the surface, so it can be used blit to the main page, or altered in post or whatever

        for chunk in self.grid:
            for square in chunk:
                square.set_character(self.blank_data["char"], self.blank_data["fg"], self.blank_data["bg"])

        self.state.tick(delta)

        # Check the cursor's blink state, etc.
        self.check_cursor_blink(delta)



        # Evaluate the windows for destruction:
        for w in self.state.windows:
            if w.destroy:
                self.draw_box(w.area)
                self.state.windows.remove(w)
        # Then draw whatever is left. This is proably the least efficient method lmao
        for w in self.state.windows:
                self.draw_window(w)

                
        
        # Then the title bar
        self.draw_title_bar() 

        # Then the infobar, which is highest priority:
        self.draw_info_bar()

        for y in range(self.rows):
            for x in range(self.columns):
                next_tile = self.grid[x][y]
                if next_tile.changed:
                    self.surface.blit(next_tile.get_surface(), (self.tilesize[0] * x, self.tilesize[1] * y))
        self.refresh_all = False


        return self.surface
    
    def draw_box(self, area:Rect, fg = "WHITE", bg = "BLUE", char = " "):
        # draw a blank box in a given area.
        for x in range(self.columns):
            for y in range(self.rows):
                if area.collidepoint(x, y):
                    self.grid[x][y].set_character(char, fg, bg)


    def draw_window(self, window:Window):
        # Fill the area of the window with the bg colour:
        self.draw_box(window.area, window.fg, window.bg)
        self.grid[window.area.x][window.area.y].set_character(DRAWTILES["topleft"], fg = window.fg)
        self.grid[window.area.right][window.area.bottom].set_character(DRAWTILES["bottomright"], fg = window.fg)
        self.grid[window.area.x][window.area.bottom].set_character(DRAWTILES["bottomleft"], fg = window.fg)
        self.grid[window.area.right][window.area.y].set_character(DRAWTILES["topright"], fg = window.fg)

        # Left/right:
        for i in range(window.area.height - 1):
            self.grid[window.area.x][window.area.y + i + 1].set_character(DRAWTILES["vertical"], fg = window.fg)
            self.grid[window.area.right][window.area.y + i + 1].set_character(DRAWTILES["vertical"], fg = window.fg)

        # Bottom and top:        
        for i in range(window.area.width - 1):
            self.grid[window.area.x + i + 1][window.area.bottom].set_character(DRAWTILES["horizontal"], fg = window.fg)
            # Check the top for title size:
            if i < len(window.title):
                tchar = window.title[i]
                self.grid[window.area.x + i + 1][window.area.top].set_character(tchar, fg = window.bg, bg = window.fg)
            else:
                self.grid[window.area.x + i + 1][window.area.top].set_character(DRAWTILES["horizontal"], fg = window.fg)
            
            # TODO: Close button.

        # Draw content in the window area:
        for data in window.get_draw_data():
            l = 0
            for line in range(len(data[2])): # For each line in the data:
                self.write_string(data[2][line], [data[0], data[1] + l])
                l += 1
        

    def write_string(self, string:str, target, highlight = -1, fg = None, bg = None, highlight_fg = None, highlight_bg = None): 
        # Write a string to a target area
        target_y = target[1]
        target_x_offset = 0
        for i in range(len(string)):
            if string[i] == "\n":
                target_x_offset = 0
                target_y += 1
            else:
                self.grid[target[0] + target_x_offset][target_y].set_character(string[i], fg, bg)
                
                if highlight == i:
                    self.grid[target[0] + target_x_offset][target_y].set_colour(highlight_fg, highlight_bg)
                target_x_offset += 1

    def draw_title_bar(self):
        for c in range(self.columns):
            self.grid[c][0].set_colour(self.menubar.text_colour, self.menubar.bg_colour)
        x_pos = self.menubar.padding
        for child in self.menubar.children:
            self.write_string(child.title, (x_pos, 0), child.highlight_char, self.menubar.text_colour, self.menubar.bg_colour, self.menubar.highlight_colour)
            x_pos += len(child.title) + self.menubar.padding
            if child.open:
                child.state_just_changed = False
                for c in child.child_objects:
                    self.draw_box(c.area, bg = "LGREY")
                    self.write_string(c.text, [child.area.x, child.child_objects.index(c) + 1], c.highlight_char, self.menubar.text_colour, self.menubar.bg_colour, self.menubar.highlight_colour)
                
            elif child.state_just_changed:
                # make sure we blank the area behind it on the next frame, probably not the best but hopefully it works
                self.refresh_all = True
    def expand_title_item(self, item):
        for menu in self.menubar.children:
            if menu == item: # brute force: just check against title text?
                menu.expand()
            else:
                menu.collapse() # only allow one open menu item at a time.

    def draw_info_bar(self):
        for c in range(self.columns):
            self.grid[c][self.rows-1].set_colour(self.infobar.fg_colour, self.infobar.bg_colour)
        self.write_string(self.infobar.text, (1, self.rows-1))
        
    # Cursor methods:
    def move_cursor(self, vect_direction = None, target_coord = None, source = None) -> None:
        # moves the cursor a direction
        valid_move = None
        self.grid[self.cursor.position[0]][self.cursor.position[1]].disable_cursor_highlight()
        if target_coord:
            # calculate vector difference between target and present:
            vect_direction = [target_coord[1] - self.cursor.position[0], target_coord[1] - self.cursor.position[1]]
        valid_move = self.cursor.move_cursor(vect_direction)
        self.grid[self.cursor.position[0]][self.cursor.position[1]].enable_cursor_highlight()
        if not valid_move and source != "mouse":
            pass # do a bonk noise or something here.
        # Update our cursor action:
        cursor_action = self.state.get_cursor_action(self.cursor.position)
        if cursor_action == [None]:
            self.cursor_action = None
        
        
    def do_cursor_action(self):
        # Does the action assigned to the cursor's position.
        if self.cursor_action != None:
            if self.cursor_action_args == [None]:
                self.cursor_action()
            else:
                self.cursor_action(*self.cursor_action_args)
        
    def check_cursor_blink(self, delta):
        blink_state = self.cursor.update_blink(delta)
        self.grid[self.cursor.position[0]][self.cursor.position[1]].toggle_cursor_blink(blink_state)
    
    def change_font_size(self, new_size):
        pass # Changes the font size but scales all objects to match.
