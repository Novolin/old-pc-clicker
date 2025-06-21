from pygame import Rect


# Commonly needed bits of data:
PROGCHARS = [" ","\u258C","\u2588"] # Progress bar characters. Other fonts may have more than just 0, 50 and 100% :()
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
MONTHS = {"JAN":31, "FEB":28, "MAR":31, "APR":30, "MAY":31, "JUN":30, "JUL":31,"AUG":31, "SEP":30, "OCT":31, "NOV":30,"DEC":31}
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
DRAWTILES = { # Special characters for boxes, etc.
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
DEFAULT_FG = "LGREY"
DEFAULT_BG = "BLUE"
DEFAULT_TXT_HI = "WHITE"
DEFAULT_HI = "ORANGE"

# Menu Bar items

class MenuItem:
    # The option in a dropdown
    def __init__(self, text:str,parent_menu, highlight = -1, what_it_do = None, action_args = None) -> None:
        self.text = text
        self.highlight_char = highlight
        self.parent_menu = parent_menu
        self.action = what_it_do
        self.action_args = action_args
        self.enabled = False
        self.selected = False 
        self.selectable = True
        self.area = Rect(0,0,0,0)
        self.close_menu_on_select = True # If it will close the parent menu when selected

    def disable(self) -> None:
        self.enabled = False
        self.selectable = False

    def enable(self) -> None:
        self.enabled = True
        self.selectable = True

    def set_position(self, parent_position:Rect, index:int, expand_size) -> None:
        self.area.update(parent_position.x, parent_position.y + index + 1, expand_size, 1)
 
class MenuItemDivider(MenuItem):
    # unselectable option, for dividing sections

    def __init__(self,parent_menu, blank = False) -> None:
        if blank:
            super().__init__(" ", parent_menu )
        else:
            super().__init__("------", parent_menu)
        self.enabled = False
        self.selectable = False

class MenuBarMenu:
    def __init__(self, title:str, start_x, highlight_char:int = -1, shortcut_key = False ):
        # Visual
        self.title = title
        self.highlight_char = highlight_char
        self.start_x = start_x
        self.width = len(title) # How wide is it when collapsed
        self.expand_width = len(title) # How wide will it be when we are fully expanded?
        self.area = Rect(self.start_x, 0, self.width, 1)
        self.expanded_area = Rect(self.start_x, 1, self.expand_width, 1) # The rect we will draw when the window is expanded
        self.open = False
        self.selected = False # Is it highlighted?
        
        self.shortcut_key = shortcut_key
        
        # Interaction:
        self.action = self.expand
        self.action_args = None
        self.state_just_changed = True

        self.child_objects = []
        
    
    
    def add_child_item(self, item:MenuItem):
        new_index = len(self.child_objects)
        # Check if it will change our expanded box size, update if needed.
        if len(item.text) >= self.expand_width:
            self.set_expand_width(len(item.text))
        self.child_objects.append(item)
        item.set_position(self.area, new_index, self.expand_width)
        

    def set_expand_width(self, new_width:int):
        # Sets the expansion width for this, all children.
        self.expand_width = new_width
        for c in self.child_objects:
            c.set_position(self.area, self.child_objects.index(c), new_width)

    def expand(self):
        if not self.open:
            self.state_just_changed = True
            self.open = True
            self.action = self.collapse
            for c in self.child_objects:
                c.enable()

    def collapse(self):
        if self.open:
            self.state_just_changed = True
            self.open = False
            self.action = self.expand
            for c in self.child_objects:
                c.disable()

class MenuBar:
    # The bar at the top of the screen, holds File, Options, etc. menus.
    def __init__(self, text_colour = "BLACK", bg_colour = "LGREY", disabled_colour = "GREY", highlight_colour = "WHITE" ) -> None:
        self.text_colour = text_colour
        self.bg_colour = bg_colour
        self.children = []
        self.padding = 2 # How many squares between each menu option?
        self.highlight_colour = highlight_colour
        self.new_child_start = self.padding # where will the next child be placed
        

    def sort_children(self):
        # Sorts all child objects by their index, adjusts areas, etc.
        self.new_child_start = self.padding
        for c in self.children:
            c.start_x = self.new_child_start
            self.new_child_start += c.width + self.padding

    
    def add_child_menu(self, child_text = "", highlight = -1, shortcut = False):
        # inits child, shifts our placement stuff.
        child_menu = MenuBarMenu(child_text, self.new_child_start, highlight, shortcut)
        self.children.append(child_menu)
        self.new_child_start += self.padding + len(child_text)
        return child_menu

    def remove_child(self, child_menu):
        child_menu.collapse() # Make sure it's closed!
        self.children.remove(child_menu)
        # Re-sort our existing child objects to fit.
    

    
    def clear_children(self):
        # Removes all children.
        for c in self.children: # make sure they're closed first.
            c.collapse()
        self.children = []

    def collapse_all(self):
        for c in self.children:
            c.collapse()

# The little bar at the bottom
class InfoBar:
    # The bar that lives on the bottom of the screen.
    # Mostly displays tooltips and shit!
    def __init__(self):
        self.bg_colour = "BLACK"
        self.fg_colour = "GREY"
        self.text = "WELCOME TO MY GAME"
        self.right_text = "v0.1"
    
    def update_text(self, new_text_left:str = "", new_text_right:str = "", new_colour = None, new_bg = None):
        if new_text_left != "":
            self.text = new_text_left

        if new_text_right != "":
            self.right_text = new_text_right

        if new_colour in COLOURS:
            self.fg_colour = new_colour
        if new_bg in COLOURS:
            self.bg_colour = new_bg

# Main class for windows

class Window:
    # An object representing a window and its contents.
    # Once I know how i want to do contents, then we'll handle that 
    def __init__(self, area:Rect, title:str = "", close_button = False, allow_scroll = True, always_on_top = False,fg = DEFAULT_FG, bg = DEFAULT_BG, txt_hi = DEFAULT_TXT_HI, bg_hi = DEFAULT_HI) -> None:
        # Location/Display info:
        self.area = area # Absolute position of the window, including borders
        self.view_area = Rect(0,0,area.width - 2, area.height - 2) # What segment of the content are we showing
        self.fg = fg
        self.bg = bg
        self.hi_fg = txt_hi
        self.hi_bg = bg_hi
        self.scrolling = allow_scroll # If False: viewport will be locked, children will be clipped if they go beyond the window
        self.show_close_button = close_button # If the close button is visible
        self.always_on_top = always_on_top # If True, display over all other windows
        max_title_size = self.area.width - 2 
        if self.show_close_button:
            max_title_size -= 2 # Give a space to close
        if len(title) > max_title_size:
            self.title = title[0:max_title_size - 1] + "~"
        else:
            self.title = title
        
        # Flags for interactions:
        self.destroy = False
        self.allow_input = True # Can we interact with its children?
        self.focused = False
        self.shortcuts = {} # When focused, what does a shortcut key do?

        # Child controls:
        self.children = []
        self.scroll_bar = False
        if close_button:
            self.close_button = Button(self, [self.area.right-1, 0], "X", action=self.queue_destroy)
        else:
            self.close_button = None
        
    def get_draw_data(self):
        # Returns a list of draw data tuples for all children in the window's viewport
        # Includes ref to the child itself so we can get colour/highlight info
        data_to_draw = []
        for child in self.children:
            if self.view_area.contains(child.area): # Fully contained in the viewport
                x_pos = child.area.left - self.view_area.left + self.area.left + 1
                y_pos = child.area.top - self.view_area.top + self.area.top
                data_to_draw.append((x_pos, y_pos, child.text_lines, child))
            elif self.view_area.colliderect(child.area): #Partially contained
                # How many lines/cols do we need to trim. Left/right trims will handle differently.
                lines_out = []
                x_clip = 0 
                y_clip = 0 
                # Find what corner is contained:
                if self.view_area.collidepoint(child.area.topleft):
                    # Easiest, just cut off the string where it clips
                    x_pos = child.area.left - self.view_area.left + self.area.left + 1
                    y_pos = child.area.top - self.view_area.top + self.area.top 
                    if child.area.right > self.view_area.right:
                        x_clip = self.view_area.width + 1 - child.area.right # index we will end our string at
                    if child.area.bottom > self.view_area.bottom:
                        y_clip = self.view_area.bottom -1 - child.area.bottom # How many lines we will display
                    
                    for i in range(child.area.height):
                        if i < y_clip and x_clip != 0: # We're clipping off the right side
                            lines_out.append(child.text_lines[i][:x_clip])
                        elif i < y_clip: # If the whole line fits
                            lines_out.append(child.text_lines[i])
                elif self.view_area.collidepoint(child.area.topright): # Off the left side
                    x_pos = self.area.left
                    y_pos = child.area.top - self.view_area.top + self.area.top
                    x_clip = self.view_area.left - child.area.left # The difference is how many charactes are cut off, so we can index from there
                    if child.area.bottom > self.view_area.bottom:
                        # We also go off the bottom:
                        y_clip = self.view_area.bottom + 1 - child.area.bottom
                    for i in range(len(child.text_lines)):
                        if y_clip < i or y_clip == 0:
                            lines_out.append(child.text_lines[i][x_clip:])
                elif self.view_area.collidepoint(child.area.bottomleft): # Off the top of the screen
                    x_pos = child.area.left - self.view_area.left + self.area.left
                    if child.area.right > self.view_area.right:
                        x_clip = self.view_area.width + 1 - child.area.right
                    y_pos = 0 # we're starting at the top since that's where it's cut off
                    lines_to_print = child.area.bottom - self.view_area.top
                    for i in range(lines_to_print + 1):
                        if x_clip != 0:
                            lines_out.append(child.text_lines[-i][:x_clip])
                        else:
                            lines_out.append(child.text_lines[-i])
                    lines_out.reverse()

                elif self.view_area.collidepoint(child.area.bottomright):
                    x_pos = child.area.left - self.view_area.left
                    y_pos = 0
                    pass # Bottom right, the worst of all worlds
                #TODO
                else:
                    x_pos = 0
                    y_pos = 0
                    pass # why would you make a control larger than its window. you are a monster.
                data_to_draw.append((x_pos, y_pos, lines_out, child))
                
    
        return data_to_draw


    def move_viewport(self, x_move = 0, y_move = 0):
        self.view_area.move_ip(x_move, y_move)

    def add_child(self, child_obj):
        # Adds a child object to the window, then sets its absolute screen position.
        self.children.append(child_obj)
        return child_obj 
    
    def queue_destroy(self):
        # Destroys the window
        self.children = []
        self.destroy = True


# Special object for scroll bars
class ScrollBar:
    def __init__(self, parent, is_vertical = True) -> None:
        pass


# Main class for content that lives in a window
# Plus subclasses for common types of content.

class Content: # AKA text box
    def __init__(self, parent:Window, pos:list, text:str,  fg = None, bg = None, thickness = 1):
        # Inherit colours from parent window unless otherwise specified.
        if fg:
            self.fg = fg
        else: 
            self.fg = parent.fg
        if bg:
            self.bg = bg
        else:
            self.bg = parent.bg
        # Just import highlight colours. If we want to change them, we will.
        self.hi_fg = parent.hi_fg
        self.hi_bg = parent.hi_bg
        
        self.text = text
        self.text_lines = text.splitlines()
        # Always expand vertically to fit # of lines
        if len(self.text_lines) > thickness:
            thickness = len(self.text_lines)
        
        # Positioning within the window.
        width = 0
        for l in self.text_lines:
            if len(l) > width:
                width = len(l)
        self.area = Rect(pos[0], pos[1], width, thickness)
        
        self.action = None
        self.action_args = None

    
class Button(Content):
    def __init__(self, parent:Window, pos:list, text:str, thickness = 1, toggle = False, action = None, action_args = [], fg = None, bg = None):
        button_string = "[" + text + "]"
        super().__init__(parent, pos, button_string, fg, bg, thickness)
        self.action = action
        self.action_args = action_args
        self.toggle = toggle
        self.selected = False
        # Default our highlighted colours to inverted.
        self.hi_fg = bg
        self.hi_bg = fg

    def get_draw_data(self):
        if self.selected:
            return (self.text, self.hi_fg, self.hi_bg)
        else:
            return (self.text, self.fg, self.bg)
        
    def activate(self):
        if self.action:
            self.action(self.action_args)

class ProgressBar(Content):
    # A progress bar that fills or depletes, using the foreground and background colours.
    def __init__(self, parent:Window, pos:list, start_val:int = 0, end_val:int = 100, size = 10, tie_to_var = False, fg = "GREEN", bg = "BLACK"):
        self.value = start_val
        self.end_val = end_val
        self.size = size
        self.tie_to_var = tie_to_var
        self.step_size = end_val // size # How many points in a full character width
        # Wait until we can calculate some kind of bar string to init the parent class
        super().__init__(parent, pos, self.get_bar_string(), fg, bg)


    def update_value(self, new_val, increment = False):
        # Updates the value. If increment is true, it adds rather than replacing. 
        # Returns true if the bar is full.
        if increment:
            self.value += new_val
        else:
            self.value
        self.get_bar_string()
        if self.value >= self.end_val:
            return True
        else:
            return False


    def get_bar_string(self):
        outstring = ""
        for i in range(self.size):

            if self.value > (i + 1) * self.step_size:
                outstring += PROGCHARS[2] # It is enough to fill the space.
            elif self.value <= i * self.step_size:
                outstring += " " # doesn't reach there
            else:
                get_char = (self.value - (i * self.step_size)) * 2 // self.step_size
                outstring += PROGCHARS[get_char]
        self.text = outstring
        return outstring
    
    def get_draw_data(self):
        return (self.get_bar_string(), self.fg, self.bg)
    

class TextEntry(Content): 
    # Sets a text entry box.
    def __init__(self, parent:Window, pos: list, text: str, fg="GREEN", bg="BLACK", thickness=1):
        super().__init__(parent, pos, text, fg, bg, thickness)
        self.contained_text = ""
        self.in_focus = False
        self.text_cursor_pos = [0,0] # What position is our text cursor in?    
    


#TODO: Move these to a game-specific file.
# Prefab windows for certain states/functions
class Calendar(Window):
    def __init__(self, location:list, month:str, year, highlight_day = 1, bg = "BLUE", fg = "LGREY") -> None:
        super().__init__(Rect(location[0], location[1], 30,12), f"{month} YEAR {year}",fg=fg, bg = bg)
        self.daylabel = Content(self, [2,1], "MON TUE WED THU FRI SAT SUN", fg, bg)
        self.month = month
        self.year = year
        self.highlight_day = highlight_day
        self.build_calendar()

    def build_calendar(self):
        self.add_child(self.daylabel) # Start with our day title thing.
        # Calculate where we're starting our month:
        day_start_offset = self.year % 7 # January 1 moves one day per year.
        for m in MONTHS:
            if m == self.month:
                break # Kill the loop if we're on the correct month.
            day_start_offset += MONTHS[m]%7
        days = MONTHS[self.month] # how many days to place on the calendar
        grid_pos = [0,3]
        next_day_to_place = 1
        while day_start_offset >= next_day_to_place:
            self.add_child(Content(self, [3 + grid_pos[0]* 4, grid_pos[1]], "XX", fg = "GREY", bg = self.bg))
            day_start_offset -= 1
            grid_pos[0] += 1

        while next_day_to_place < days:
            if next_day_to_place == self.highlight_day: # invert the colours on the current day
                next_day_box = Content(self, [3 + grid_pos[0] * 4, grid_pos[1]], str(next_day_to_place), fg =self.bg, bg=self.fg )
            else:
                next_day_box = Content(self, [3 + grid_pos[0] * 4, grid_pos[1]], str(next_day_to_place), bg =self.bg, fg=self.fg )
            
            self.add_child(next_day_box)
            next_day_to_place += 1
            grid_pos[0] += 1
            if grid_pos[0] >= 7:
                grid_pos[0] = 0
                grid_pos[1] += 2
            
        # Done placing the days, fill in the rest of the grid.
        while grid_pos[0] < 7:
            self.add_child(Content(self, [3 + grid_pos[0]* 4, grid_pos[1]], "XX", fg = "GREY", bg = self.bg))
            grid_pos[0] += 1
        
class ArcadeThumbnail(Window):
    # A little animated thumbnail for showing what's going on.
    # NOT IMPLEMENTED
    def __init__(self, area:Rect, title:str = "ARCADE"):
        super().__init__(area, title)
        self.add_child(Content(self, [2,1], "DONT LOOK"))
        

class DayStatus(Window):
    def __init__(self, origin:list, window_width, ticks_per_day, title: str = "DAY IN PROGRESS") -> None:
        area = Rect(origin[0], origin[1], window_width-2, 20 )
        super().__init__(area, title)
        self.day_complete = False
        self.day_income = 0.00
        self.games_played = 0
        self.visitors = 0
        self.day_progress = ProgressBar(self, [2,2], size = 15, end_val = ticks_per_day)
        self.add_child(Content(self, [2,1], "Time Remaining:"))
        self.add_child(self.day_progress)
        self.income_text = Content(self, [2,4], f"INCOME:      ${self.day_income:.2f}")
        self.play_text = Content(self, [2,5], f"GAMES PLAYED: {self.games_played}")
        self.visit_text = Content(self, [2,6], f"VISITORS:     {self.visitors}")
        self.add_child(self.play_text)
        self.add_child(self.income_text)
        self.add_child(self.visit_text)

    def update(self, ticks_completed, income, plays, visitors):
        self.day_progress.value = ticks_completed
        self.day_income = income
        self.games_played = plays
        self.visitors = visitors
        self.income_text.text = f"INCOME:      ${self.day_income:.2f}"
        self.play_text.text = f"GAMES PLAYED: {self.games_played}"
        self.visit_text.text = f"VISITORS:     {self.visitors}"

class DayEnd(Window):
    def __init__(self, area: Rect, gamestate) -> None:
        super().__init__(area, "END OF DAY")
        self.summary = Content(self, [2,2], f"NOT DONE BUT U MADE ${gamestate.active_day_obj.income}")
        self.okbutton = Button(self, [5,4], "OK", bg = "GREEN", action=gamestate.advance_day)
        self.add_child(self.summary)
        self.add_child(self.okbutton)



def build_new_game_window(gamestate_target):
    # returns a Window obj for starting a new game
    win = Window(Rect(10, 4, 30, 10), "NEW GAME")
    text_1 = Content(win, [5,2], "Start a new game?")
    win.add_child(text_1)
    text_2 = Content(win, [2,3], "Unsaved data will be lost!")
    win.add_child(text_2)
    okbutt = Button(win,[5,5], "OK", action = gamestate_target.display.start_new_game, fg = "WHITE", bg = "GREEN")
    win.add_child(okbutt)
    cancelbutt = Button(win,[10,5], "Cancel", action = win.queue_destroy, fg = "BLACK", bg = "LRED")
    win.add_child(cancelbutt)
    
    gamestate_target.add_window(win)
    gamestate_target.menu_bar.collapse_all()
    gamestate_target.display.refreshall = True


def build_day_start_windows(gamestate):
    # Builds all the windows for the start of day state.
    # get some placement stuff:
    window_width = gamestate.display.columns - 2
    halfway = window_width // 2
    quarter = halfway // 2
    # Main information window
    info_window = Window(Rect(1,1,window_width, 10), f"DAY {gamestate.day}")
    info_window.add_child(Content(info_window, [2,1], f"{DAYS[gamestate.day%7]} {gamestate.month} {gamestate.month_day_counter}, Year {gamestate.year}"))
    info_window.add_child(Content(info_window, [halfway - len(gamestate.name) // 2, 2], gamestate.name))
    info_window.add_child(Content(info_window, [2,3], "FUNDS:"))
    info_window.add_child(Content(info_window, [halfway,3], f"${gamestate.money:.2f}"))
    info_window.add_child(Content(info_window, [2,4], "CABINET STATUS:"))
    info_window.add_child(Content(info_window, [halfway, 4], f'{len(gamestate.property.cabinets)} Active, 0 Inactive'))
    info_window.add_child(Content(info_window, [2,5], "LOCATION:"))
    info_window.add_child(Content(info_window, [halfway, 5], "idk what to put here"))
    info_window.add_child(Button(info_window, [quarter - 5, 7], "START DAY", fg="BLACK", bg = "GREEN" , action=gamestate.start_day))
    info_window.add_child(Button(info_window, [quarter + halfway - 6, 7 ], "SAVE + QUIT", bg = "RED", action=quit))


    # Other sub screens:
    cal_window = Calendar([1,12], gamestate.month, gamestate.year)

    gamestate.add_window(cal_window)
    gamestate.add_window(info_window)

def build_day_run_windows(gamestate, ticks_per_day):
    # Returns the window with the state data or w/e
    state_window = DayStatus([1,1], gamestate.display.columns, ticks_per_day)

    return state_window 

def build_day_summary_windows(gamestate):
    # Returns a set of windows to display the end-of-day summary
    summary_window = DayEnd(Rect(4,4,15, 10), gamestate)
    return summary_window


def build_test_window():
    # Builds a clipping test
    test_window = Window(Rect(3,2,13,13), "TEST WINDOW")
    test_top = Content(test_window, [5,0],  "VCLIP\nTEST!\nABCDE\nFGHIJ")
    test_window.add_child(test_top)
    test_left = Content(test_window, [0,5], "LEFT\nSIDE\nTEST")
    test_window.add_child(test_left)
    test_right = Content(test_window, [11,5], "RIGHT\nCLIP \nTEST")
    test_window.add_child(test_right)
    test_bottom = Content(test_window, [6,11], "BOTTOM\nTEST!!")
    test_window.add_child(test_bottom)
    test_noclip = Content(test_window, [5,7], "no  \nflip")
    test_window.add_child(test_noclip)
    test_window.move_viewport(3,2)
    return test_window