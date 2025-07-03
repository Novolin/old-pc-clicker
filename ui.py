# Standardized User Interface objects, such as text, buttons, etc.

from pygame import Rect

DRAWTILES = { # enum for special characters, in case your editor doesn't support them all because you code in wingdings
    "topleft":"\u2554",     # ╔
    "topright":"\u2557",    # ╗
    "bottomleft":"\u255A",  # ╚
    "bottomright":"\u255D", # ╝
    "vertical":"\u2551",    # ║
    "horizontal":"\u2550",  # ═
    "ttop":"\u2566",        # ╦
    "tleft":"\u2560",       # ╠
    "tright":"\u2563",      # ╣
    "tbottom":"\u2559",     # ╙
    "tcenter":"\u256C",     # ╬
    "lightfill":"\u2591",   # ░
    "medfill":"\u2592",     # ▒
    "heavyfill":"\u2593",   # ▓
    "leftarrow":"\u2190",   # ←
    "uparrow":"\u2191",     # ↑
    "rightarrow":"\u2192",  # →
    "downarrow":"\u2193"    # ↓
    }

# Scroll bars for menus, etc.

class ScrollBar:
    def __init__(self, bar_size:int, total_lines, lines_per_screen, horizontal = False ):
        # Colours will be set by the window or object which has a scroll bar attached.
        self.current_position = 0
        self.bar_size = bar_size # A rect representing the space the scroll bar will live in.
        self.total_lines = total_lines
        self.lines_per_screen = lines_per_screen
        self.maxscroll = total_lines - lines_per_screen
        self.horizontal = horizontal
        self.astext = "" # how it will look as a string.
        self.visible = True # If we should bother to show the scroll bar at all.
        self.refresh_text()
        

    def refresh_text(self):
        newtext = ""
        if self.maxscroll <= 0:
            self.visible = False
       
        else:
            self.visible = True
            if self.horizontal:
                newtext += DRAWTILES["leftarrow"]
            else:
                newtext += DRAWTILES["uparrow"]

            lines_per_char = self.maxscroll / self.bar_size

            for i in range(self.bar_size - 1):
                if self.current_position > lines_per_char * (i + 1) or self.current_position < lines_per_char * i:
                    newtext += DRAWTILES["lightfill"]
                else:
                    newtext += DRAWTILES['heavyfill']
            if self.horizontal:
                newtext += DRAWTILES["rightarrow"]
            else:
                newtext += DRAWTILES["downarrow"]
            
        self.astext = newtext
        return newtext

    
    def scroll(self, amount):
        self.current_position += amount
        if self.current_position < 0:
            self.current_position = 0
        elif self.current_position > self.maxscroll:
            self.current_position = self.maxscroll
        self.refresh_text() # refresh our bar position
    
    def update_size(self, content_size):
        # updates the scrollbar to account for a change in window size
        self.total_lines = content_size
        self.maxscroll = content_size - self.lines_per_screen
        self.refresh_text()
        


        


# Top drop-down

class MenuItem:
    # An item in a dropdown menu
    def __init__(self, parent, text, highlight_char:int, func, func_args, fg = "BLACK", bg = "LGREY", hi = "WHITE", hi_bg = "GREY", shortcut_col = "WHITE" )-> None:
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.shortcut_col = shortcut_col
        self.index = -1 # de facto y position
        
        self.text = text
        self.highlight_char = highlight_char
        
        self.func = func
        self.func_args = func_args
        self.parent = parent

        self.enabled = False
        self.hovered = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def action(self):
        if self.enabled:
        # fires whatever the action is
            self.parent.collapse()
            if self.func_args:
                self.func(*self.func_args)
            else:
                self.func()

        
class MenuDivider(MenuItem):
    # A divider for segmenting a drop down menu
    def __init__(self, text = "------",  fg="BLACK", bg="LGREY", hi="WHITE", hi_bg="GREY", shortcut_col="WHITE") -> None:
        super().__init__(None, text, -1, None, None, fg, bg, hi, hi_bg, shortcut_col)

    def enable(self):
        pass # we can't enable a divider
class Menu:
    # One of the drop down menus for the menu bar
    def __init__(self, text, highlight_char:int, fg = "BLACK", bg = "LGREY", hi = "WHITE", hi_bg = "GREY", shortcut_col = "WHITE" ) -> None:
        self.text = text
        self.highlight_char = highlight_char
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.shortcut_col = shortcut_col
        self.area = Rect(0,0,len(self.text), 1) # Where is it located on the screen.
        
        
        self.expanded = False
        self.expand_width = len(self.text)

        self.children = []
        

    def add_child(self, object:MenuItem):
        object.index = len(self.children)
        self.children.append(object)
        if len(object.text) > self.expand_width:
            self.expand_width = len(object.text)
            for i in range(len(self.children)):
                self.children[i].area = Rect(self.area.left, self.area.top + i, self.expand_width, 1)
                

    def remove_child(self, index):
        self.children.pop(index)
        # Check if we have to adjust the width of our expand area:
        self.expand_width = len(self.text)
        for c in self.children:
            if len(c.text) > self.expand_width:
                self.expand_width = len(c.text)

    def expand(self):
        self.expanded = True
        for i in self.children:
            i.enable()

    def collapse(self):
        self.expanded = False
        for i in self.children:
            i.disable()
        

class MenuBar:
    # The bar at the top of the screen. Has its own set of default colours. 
    # Not yet implemented: keyboard shortcut stuff.
    def __init__(self, fg = "BLACK", bg = "LGREY", hi = "WHITE", hi_bg = "GREY", shortcut_col = "WHITE") -> None:
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.shortcut_col = shortcut_col # What colour the keyboard shortcut will appear as in a highlighted item.
        self.children = []
        self.child_offset = 2 # spaces between menus

    def add_child(self, menu:Menu):
        menu.area.move_ip(self.child_offset, 0)
        for i in self.children:
            menu.area.move_ip(i.area.width + self.child_offset, 0)
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

# The little bar at the bottom

class InfoBar:
    def __init__(self, init_text:str, grid_size:list|tuple, fg = "LGREY", bg = "BLACK"):
        self.fg = fg
        self.bg = bg
        self.area = Rect(0, grid_size[0] -1, grid_size[1], 1)
        self.left_text = init_text
        self.left_text_full = init_text
        self.location = [0,self.area.bottom]
        
        self.right_text = ""
        self.right_text_pos = [self.area.right - len(self.right_text), self.location[1]]

    def update_text(self, left_text:str | None = None, right_text:str | None = None):
        if left_text:
            self.left_text = left_text
            self.left_text_full = left_text
        if right_text:
            self.right_text = right_text
            self.right_text_pos = [self.area.right - len(right_text), self.location[1]]
        # Always clip text on the left to make room for text on the right:
        text_overlap = len(self.right_text) + len(self.left_text_full) - self.area.width
        if text_overlap > 0:

            self.left_text = self.left_text_full[0:self.area.width - len(self.right_text) - 1] + "~"


# Controls, parent class is for generic text

class Content:
    # Generic object for text, parent of all other ui elements.
    def __init__(self, location:list|tuple, text:str, fg = None, bg = None, hi = None, hi_bg = None) -> None:
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.func = None
        self.func_args = None
        self.hi_on_hover = False # do we use the highlight colour if the cursor is interacting with it?
        self.highlighted = False
        self.handles_raw_text = False  # Can we pass a TextInput command to it. Only for controls that handle typed input.
        self.parent_control = None

        self.text_lines = text.splitlines()
        width = 0
        height = 0
        for i in self.text_lines:
            height += 1
            if len(i) > width:
                width = len(i)
        for line in range(len(self.text_lines)):
            while len(self.text_lines[line]) < width:
                self.text_lines[line] += " "
        
        self.area = Rect(location[0], location[1], width, height)
        self.absolute_area = self.area.copy()

    def set_parent(self, new_parent):
        self.parent_control = new_parent
        self.absolute_area.move_ip(new_parent.area.topleft)
        self.absolute_area.move_ip(1,1)


    def tick(self, delta):
        pass # use this func for things that need to get a time variable passed to them

    def update(self, new_loc:list|tuple|None = None, new_text:str|None = None, fg:str|None = None, bg:str|None = None, hi:str|None = None, hi_bg:str|None = None):
        # Update values/colour/etc.
        if new_loc != None:
            self.area.update(new_loc, self.area.size)
        if new_text and type(self.area) == Rect:
            self.text_lines = new_text.splitlines()
            text_len = 0
            for line in new_text.splitlines():
                if len(line) > text_len:
                    text_len = len(line)
            self.area.update(self.area.topleft, [text_len, len(self.text_lines)])
        if fg:
            self.fg = fg
        if bg:
            self.bg = bg
        if hi:
            self.hi = hi
        if hi_bg:
            self.hi_bg = hi_bg


class ProgressBar(Content):
    def __init__(self, location, size:int, start_value = 0, target_value = 100, fg="GREEN", bg="BLACK", hi="RED", hi_bg="YELLOW", font_does_eighths = False) -> None:
        super().__init__(location, " "*size, fg, bg, hi, hi_bg)
        self.font_does_eighths = font_does_eighths # If the font supports the 1/8th of a full char (\u2589 -> \u258F)
        self.size = size
        self.val = start_value
        self.target_val = target_value

        self.update_text() # change our string to represent the value    
        
    def update_text(self):
        updated_text = ""
        val_per_char = self.target_val / self.size
        for i in range(self.size):
            if self.val > val_per_char * (i+ 1):
                updated_text += "\u2588" # full
            elif self.val < val_per_char * i:
                updated_text += " " # fill with full bg colour
            else:
                amount = self.val - (val_per_char * i)
                # TODO: add a check for 1/8ths, if the font supports it
                if amount >= val_per_char / 2:
                    updated_text += "\u258C" # half-full char
                else:
                    updated_text += " " # Empty
        
        self.text_lines = [updated_text]


    
    def increment_value(self, amount:int) -> int:
        # adds amount to value and triggers an update. Use negatives to make it go lower.
        # Returns the new value.
        self.val += amount
        self.update_text()
        return self.val
    
    def set_value(self, new_val:int):
        # directly sets the value to the new one, forces a refresh.
        self.val = new_val
        self.update_text()

class Button(Content):
    # Fancy text that triggers a function on click
    def __init__(self, location, text: str, fg=None, bg=None, hi=None, hi_bg=None, func = None, func_args:list|tuple|None = None, highlight_on_hover = False) -> None:
        super().__init__(location, text, fg, bg, hi, hi_bg)
        self.func = func
        self.func_args = func_args
        self.hi_on_hover = highlight_on_hover

    def activate(self):
        if self.func and self.func_args:
            return self.func(*self.func_args)
        elif self.func:
            return self.func()
        return None


class TextEntry(Content):
    # Single line of text entry
    def __init__(self, location, width:int, lines:int, state_control, default_text:str = "", max_input:int = -1, fg=None, bg=None, hi=None, hi_bg=None, retain_placeholder = False) -> None:
        super().__init__(location, " "*width, fg, bg, hi, hi_bg)
        self.handles_raw_text = True
        if len(default_text) >= width:
            default_text = default_text[0:width - 1]
        self.default_text = default_text
        

        self.lines = lines
        self.allow_linebreak = False
        if lines > 1:
            self.area.update(self.area.left, self.area.top, self.area.width, lines)
            self.allow_linebreak = True
            while len(self.text_lines) < lines:
                self.text_lines.append(" ")
        
        self.max_input_width = max_input # How many characters to limit the input to.
        self.text_as_str = ""
        if retain_placeholder:
            self.text_as_str = default_text
        self.focused = False # Are we focused on the box.
        self.state_control = state_control # What state object is managing our stuff. Used to tie it to the active input flag
        self.func = self.focus_box
        
        # Text cursor:
        self.text_cursor_pos = 0 # What character are we modifying
        self.vis_cursor_pos = [0,0] # What is the x/y position of it in the visual representation.
        self.cursor_blink_ms = 500 # how many ms per blink
        self.cursor_timer = 0 # ms since our last blink
        self.cursor_blinked = False 
        self.cursor_char = DRAWTILES["medfill"]

        self.refresh_contents()


    def tick(self, delta):
        if self.focused:
            self.cursor_timer += delta
            if self.cursor_timer > self.cursor_blink_ms * 2:
                self.cursor_blinked = True
                self.cursor_timer -= self.cursor_blink_ms * 2
            elif self.cursor_timer > self.cursor_blink_ms:
                self.cursor_blinked = False
        self.refresh_contents()

    def focus_box(self): 
        # Focus on the entry box.
        abs_cursor_loc = self.state_control.cursor.position
        cursor_location = [ abs_cursor_loc[0] - self.absolute_area.left -1, abs_cursor_loc[1] - self.absolute_area.top -1]
        if not self.focused:
            self.focused = True
            self.state_control.set_input_target(self)
            self.highlighted = True
            self.cursor_blink = True
        if cursor_location[0] >= len(self.text_lines[cursor_location[1]]):
            cursor_location[0] = len(self.text_lines[cursor_location[1]]) -1
        txt_loc = 0
        chars_left = cursor_location[0]
        for line in self.text_lines[0:cursor_location[1]]:
            line_size = len(line)
            if chars_left > line_size:
                txt_loc += line_size # includes the "\n"
            else:
                txt_loc += chars_left
                break # we're at the 0 point, get out.
        self.text_cursor_pos = txt_loc
        self.align_cursor_pos() # align the cursor to where it actually is in the text
        

    def align_cursor_pos(self):
        # align the visual position to the text position.
        new_vis_pos = [0,0]
        curs_count = 0
        while curs_count < self.text_cursor_pos and curs_count < len(self.text_as_str):
            if self.text_as_str[curs_count] == "\n":
                new_vis_pos[1] += 1
                new_vis_pos[0] = 0
                curs_count += 1
            else:
                new_vis_pos[0] += 1
                curs_count += 1
        self.vis_cursor_pos = new_vis_pos
        

    
    def refresh_contents(self): # TODO reset
        if self.text_as_str == "" and not self.focused: 
            # Nothing entered into an unfocused box:
            placeholder = self.default_text
            while len(placeholder) < self.area.width:
                placeholder += DRAWTILES["lightfill"]
            self.text_lines[0] = placeholder
            for line in range(len(self.text_lines)):
                while len(self.text_lines[line]) < self.area.width:
                    self.text_lines[line] += DRAWTILES["lightfill"]
            
            return
        placeholder = self.text_as_str.splitlines()
        if not self.focused: # text is entered, but not focused
            while len(placeholder) < self.lines:
                placeholder.append(DRAWTILES["lightfill"] * self.area.width)
            for line in range(len(placeholder)):
                while len(placeholder[line]) <= self.area.width:
                    placeholder[line] += DRAWTILES["lightfill"]
        else: # Text box is focused.
            while len(placeholder) < self.lines:
                placeholder.append(" " * self.area.width)
            for line in range(len(placeholder)):
                if line == self.vis_cursor_pos[1] and not self.cursor_blinked:
                    newline = placeholder[line][0:self.vis_cursor_pos[0]] + self.cursor_char + placeholder[line][self.vis_cursor_pos[0] + 1:]
                    placeholder[line] = newline
                while len(placeholder[line]) < self.area.width:
                    placeholder[line] += " "
            
        self.text_lines = placeholder
            

    def text_input(self, text:str):
        self.text_as_str = self.text_as_str[0:self.text_cursor_pos] + text + self.text_as_str[self.text_cursor_pos:]
        self.text_cursor_pos += len(text)
        
        self.align_cursor_pos()
        self.refresh_contents()
        


    def release_focus(self):
        self.focused = False
        self.cursor_blink = False
        self.cursor_timer = 0

    def do_backspace(self):
        if self.text_cursor_pos > 0:
            self.text_as_str = self.text_as_str[0:self.text_cursor_pos - 1] + self.text_as_str[self.text_cursor_pos:]
            self.move_cursor(-1,0)
        else:
            print("NO!!!")

    def add_linebreak(self):
        if self.allow_linebreak:
            self.text_input("\n")
        else:
            self.release_focus()

    def move_cursor(self, x = 0, y = 0):
        
        if x:
            self.text_cursor_pos += x
            if self.text_cursor_pos > len(self.text_as_str):
                self.text_cursor_pos = len(self.text_as_str)
            if self.text_cursor_pos < 0:
                self.text_cursor_pos = 0
            self.align_cursor_pos()
        if y:
            target_cursor_pos = self.vis_cursor_pos
            target_cursor_pos[1] += y
            while self.vis_cursor_pos != target_cursor_pos:
                if y > 0:
                    self.text_cursor_pos += 1
                else:
                    self.text_cursor_pos -= 1
                self.align_cursor_pos()
            
    def clear(self):
        # Clears the contents of the box.
        self.text_as_str = ""
        self.refresh_contents()
        
class CheckBox(Content): #TODO
    def __init__(self, location: list | tuple, text, tied_var = None, start_selected = False, fg=None, bg=None, hi=None, hi_bg=None) -> None:
        self.checkbox_text = "[ ]"
        
        super().__init__(location, text, fg, bg, hi, hi_bg)
        self.selected  = start_selected
        


        
class SelectMenu(Content):
    # A menu to select multiple items
    def __init__(self, location, items:list, fg=None, bg=None, hi=None, hi_bg=None) -> None:
        
        super().__init__(location, "test", fg, bg, hi, hi_bg)
# Window object

class Window:
    def __init__(self, parent, area:Rect, title, fg = None, bg = None, hi = None, hi_bg = None, border = "LGREY", show_close = False, allow_scroll = False, always_on_top = False):
        self.area = area
        self.viewport = Rect(0,0,self.area.width -2, self.area.height - 2)
        self.children = []
        self.full_content_area = self.viewport.copy() # at the start, assume everything fits the window area.
        self.parent = parent

        self.visible = True
        self.always_on_top = always_on_top
        self.show_close = show_close
        self.destroy = False


        # Scrolling related:
        self.v_scroll_bar = None
        self.h_scroll_bar = None
        self.allow_scroll = allow_scroll

        # looks:
        self.title = title
        self.fg = fg
        self.bg = bg
        self.hi = hi
        self.hi_bg = hi_bg
        self.border = border


        self.DEBUG_FUNCTIONS = False


    def add_child(self, child:Content):
        self.children.append(child)
        child.set_parent(self)
        if child.area.bottom > self.viewport.bottom and self.allow_scroll:
            self.full_content_area.update(self.full_content_area.left, self.full_content_area.top, self.full_content_area.width, child.area.bottom)
            if self.v_scroll_bar:
                self.v_scroll_bar.update_size(self.full_content_area.bottom)
            else:
                self.v_scroll_bar = ScrollBar(self.area.height - 2, self.full_content_area.bottom, self.viewport.height)
        if child.area.right > self.area.right and self.allow_scroll:
            self.full_content_area.update(self.full_content_area.left, self.full_content_area.top, child.area.right, self.full_content_area.height)
            if self.h_scroll_bar:
                self.h_scroll_bar.update_size(self.full_content_area.right)
            else:
                self.h_scroll_bar = ScrollBar(self.area.width - 2, self.full_content_area.right, self.viewport.width, True)


    def scroll_view(self, x:int = 0, y:int = 0):
        # scrolls the view by x, y amounts
        self.viewport.move_ip(x, y)
        if self.viewport.bottom > self.full_content_area.bottom:
            self.viewport.move_ip(0,-1)
        if self.viewport.right > self.full_content_area.right:
            self.viewport.move_ip(-1,0)
        if self.viewport.top < self.full_content_area.top: # could potentially be negative if you're doing wacky stuff.
            self.viewport.move_ip(0,1)
        if self.viewport.left < self.full_content_area.left:
            self.viewport.move_ip(1,0)
        # recalculate scroll bars:
        # do both because we may do a shift in both x and y
        if self.v_scroll_bar:
            self.v_scroll_bar.scroll(y)
        if self.h_scroll_bar:
            self.h_scroll_bar.scroll(x)



    def exec_and_destroy(self, func, args:list = []):
        # Use this if a button or something needs to call a function, but also set this window to be destroyed.
        if type(args) != list:
            func(args)
        else:
            func(*args)
        self.queue_destroy() # do this last since it purges the child list.



    def draw(self, target_grid, delta):
        # Draws the window and its contents to the given grid manager

        
        # start with a blank square
        target_grid.draw_square(self.area, " ", self.fg, self.bg)
        # Borders:
        target_grid.draw_hline(self.area.topleft, self.area.width, self.border, self.bg)
        target_grid.draw_hline(self.area.bottomleft, self.area.width, self.border, self.bg)
        target_grid.draw_vline(self.area.topleft, self.area.height, self.border, self.bg)
        if self.v_scroll_bar and self.v_scroll_bar.visible:
            for i in range(self.v_scroll_bar.bar_size):
                if i == 0:
                    target_grid.set_char(self.area.right, self.area.top + 1 + i, self.v_scroll_bar.astext[i], self.border, self.bg, func = self.scroll_view, func_args = [0,-1])    
                else:
                    target_grid.set_char(self.area.right, self.area.top + 1 + i, self.v_scroll_bar.astext[i], self.border, self.bg)
            target_grid.set_char(self.area.right, self.area.top + self.v_scroll_bar.bar_size + 1, self.v_scroll_bar.astext[-1], self.border, self.bg, func= self.scroll_view, func_args = [0,1])
                    
        else:
            target_grid.draw_vline(self.area.topright, self.area.height, self.border)
        # corners:
        target_grid.set_char(self.area.left, self.area.top, DRAWTILES["topleft"], self.border, self.bg)
        target_grid.set_char(self.area.left, self.area.bottom, DRAWTILES["bottomleft"], self.border, self.bg)
        target_grid.set_char(self.area.right, self.area.top, DRAWTILES["topright"], self.border, self.bg)
        target_grid.set_char(self.area.right, self.area.bottom, DRAWTILES["bottomright"], self.border, self.bg)

        # Title bar:
        if len(self.title) > self.area.width - 4:
            draw_title = self.title[0:self.area.width - 5] + "~"
        else:
            draw_title = self.title
        target_grid.write_string(draw_title, [self.area.left + 1, self.area.top], self.border, self.bg)

        if self.show_close:
            target_grid.set_char(self.area.right - 1, self.area.top, "X", fg = "RED", func = self.queue_destroy)

        # Contents:
        
        for child in self.children:
            child.tick(delta) # pass our delta time to the child
            # Get the child's absolute position
            child_start_x = child.area.left - self.viewport.left + self.area.left + 1
            child_start_y = child.area.top - self.viewport.top + self.area.top + 1
            for y_range in range(child.area.height):
                if child_start_y + y_range < self.area.bottom and child_start_y + y_range > self.area.top:
                    # Only print within the window area
                    for x_range in range(child.area.width):
                        if child_start_x + x_range < self.area.right and child_start_x + x_range> self.area.left:
                            if child.highlighted:
                                target_grid.set_char(child_start_x + x_range, child_start_y + y_range, 
                                                 child.text_lines[y_range][x_range], 
                                                 child.hi, child.hi_bg, child.func, child.func_args
                                                 )
                            else:
                                target_grid.set_char(child_start_x + x_range, child_start_y + y_range, 
                                                 child.text_lines[y_range][x_range], 
                                                 child.fg, child.bg,
                                                 child.func, child.func_args)


    def queue_destroy(self):
        self.children = []
        self.destroy = True


class ConfirmWindow(Window):
    # A window with an ok/cancel button situation going on
    # TODO: when active, make "RETURN" and "ESCAPE" do OK/CANCEL, respectively.
    def __init__(self, parent, area: Rect, title:str, prompt:str, confirm_func, confirm_args:list|None = None, cancel_func = None, cancel_args:list|None = None, fg = None, bg = None, border="LGREY", show_close=False, allow_scroll=False, always_on_top=True):
        super().__init__(parent,area, title, border, show_close, allow_scroll, always_on_top)
        # Get some measurements:
        ok_location = (self.area.width // 4) - 1 # 1/4 of the window, centering text
        cancel_location = ok_location + (self.area.width // 2) - 2 # 3/4 of the window, centered
        prompt_list = prompt.splitlines()
        linecount = 0
        for line in prompt_list:
            # Center the text per line:
            linecount += 1
            text_content = Content([self.area.width//2 - len(line)//2, linecount], line, fg = fg, bg = bg)
            self.add_child(text_content)
        ok_funcs = []
        ok_funcs.append(confirm_func)
        if confirm_args:
            ok_funcs += confirm_args
        ok_button = Button([ok_location, linecount + 2], "OK", "WHITE", "GREEN", "GREEN", "BLACK", self.exec_and_destroy, ok_funcs, True)
        if cancel_func == None:
            cancel_func = self.queue_destroy
        cancel_button = Button([cancel_location, linecount + 2], "CANCEL", "WHITE", "RED", "RED", "BLACK", func = cancel_func,func_args=cancel_args, highlight_on_hover=True)

        self.add_child(ok_button)
        self.add_child(cancel_button)


class TextEntryWindow(Window):
    # A generic window you can use to prompt a user with
    def __init__(self, parent, area: Rect, title, prompt:str, confirm_func,  cancel_func = None, cancel_args:list|None = None, default_text:str = "", fg=None, bg=None, hi=None, hi_bg=None, border="LGREY", show_close=False, always_on_top=False):
        super().__init__(parent,area, title, border, show_close, always_on_top)
        # Get some measurements:
        ok_location = (self.area.width // 4) - 1 # 1/4 of the window, centering text
        cancel_location = ok_location + (self.area.width // 2) - 2 # 3/4 of the window, centered
        prompt_list = prompt.splitlines()
        linecount = 0
        for line in prompt_list:
            # Center the text per line:
            linecount += 1
            text_content = Content([self.area.width//2 - len(line)//2, linecount], line, fg = fg, bg = bg)
            self.add_child(text_content)

        self.confirm_func = confirm_func
        ok_button = Button([ok_location, linecount + 3], "OK", "WHITE", "GREEN", "GREEN", "BLACK", self.submit_text, highlight_on_hover=True)
        if cancel_func == None:
            cancel_func = self.queue_destroy
        cancel_button = Button([cancel_location, linecount + 3], "CANCEL", "WHITE", "RED", "RED", "BLACK", func = cancel_func,func_args=cancel_args, highlight_on_hover=True)

        self.add_child(ok_button)
        self.add_child(cancel_button)

        self.text_prompt = TextEntry([2, linecount + 1], self.area.width - 4, 1, self.parent, default_text, fg = "BLACK", bg = "LGREY")
        
        self.add_child(self.text_prompt)
        
    def submit_text(self):
        entered_text = self.text_prompt.text_as_str
        self.exec_and_destroy(self.confirm_func, [entered_text])


def DEBUG_test_windows(state):
    # opens a bunch of windows to test things
    test_test = TextEntryWindow(state, Rect(1,1,40,8), "TEXT ENTRY", "test text entry", print)
    conf_test = ConfirmWindow(state, Rect(1,11,10,10), "CONFIRM", "CONFIRM?", print, ["CONFIRMED!"], print, ["CANCELED!", "NO!"])
    state.add_window(test_test)
    state.add_window(conf_test)