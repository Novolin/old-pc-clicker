# Game-related windows and whatnot.

from pygame import Rect
from ui import *

SPECIAL_CHARS = {
    "cab":"\u221A",         # √ 
    "wallHor":"\u2500",     # ─
    "wallVert":"\u2502",    # │
    "wallTL":"\u250C",      # ┌
    "wallTR":"\u2510",      # ┐
    "wallBL":"\u2514",      # └
    "wallBR":"\u2518",      # ┘
    "smiley":"\u263a",      # ☺
    "smileyfull":"\u263b"   # ☻
}

class CalendarWindow(Window):
    def __init__(self, parent, location, month:str, day:int, year:int, size = [24, 9], fg = "WHITE", bg = "BLUE", hi = "BLUE", hi_bg = "LGREY"):
        self.month_list = {
            "JAN":31,
            "FEB":28,
            "MAR":31,
            "APR":30,
            "MAY":31,
            "JUN":30,
            "JUL":31,
            "AUG":31,
            "SEP":30,
            "OCT":31,
            "NOV":30,
            "DEC":31
            }
        self.weekdays = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
        self.day = day
        self.month = month
        self.year = year
        self.day_offset = 0
        title = f"{month}, Year {self.year}"
        super().__init__(parent, Rect(location, size), title,fg, bg, hi, hi_bg,  allow_scroll= False)
        self.build_window()

    def get_start_offset(self):
        # Determines where the calendar needs to start, depending on day/month, etc.
        day_count = self.year * 365 # leap years are for fools
        for m in self.month_list:
            if m != self.month:
                day_count += self.month_list[m]
            else:
                break # we are where we want to be
        
        
        self.day_offset = day_count % 7

    def build_window(self):
        # Fills the window with the correct children, based on our day
        weektitle = Content([1,0],"MO TU WE TH FR SA SU")
        day_list = []
        day_num = 1
        self.get_start_offset()
        next_location = [1 + (self.day_offset * 3),1]
        if self.day_offset == 0:
            next_location[1] += 1
        while day_num <= self.month_list[self.month]:
            next_day = Content(next_location, f"{day_num:2}", fg = self.fg, bg = self.bg, hi = self.hi, hi_bg = self.hi_bg)
            if day_num == self.day:
                next_day.highlighted = True
            day_list.append(next_day)
            day_num += 1
            next_location[0] += 3
            if next_location[0] >= 21:
                next_location[0] = 1
                next_location[1] += 1
        self.add_child(weektitle)
        for item in day_list:
            self.add_child(item)
            
    def set_date(self, month:str, day:int, year:int):
        self.year = year
        self.month = month
        self.day = day
        self.children = []
        self.build_window()
        

    
                
class PropertyMap(Window):
    def __init__(self, parent, property):
        self.parent = parent
        self.property = property
        # pull the property's map data:
        super().__init__(parent, Rect(0,11,24,17),property.name, fg = "WHITE", bg = "BLACK", hi = "RED", hi_bg = "BLACK")
        self.customer_icons = []
        self.entry_location = [self.property.size[0] // 2, 0]
        # draw the walls:
        


    def draw_map(self):
        # Blanks the map and redraws it.
        self.children = []
        
        x_offset = (18 - self.property.size[0] ) // 2 # offset to center our property in the window
        top_wall = SPECIAL_CHARS["wallTL"]
        door = self.property.size[0] // 2
        index = 0
        while len(top_wall) < self.property.size[0] + 1:
            if index == door -1:
                top_wall += "[_]"
                index += 3
            else:
                top_wall += SPECIAL_CHARS["wallHor"]
                index += 1
        top_wall += SPECIAL_CHARS["wallTR"]
        toptext = Content([x_offset, 1], top_wall, "GREY", "BLACK")
        bottomText = Content([x_offset, 2 + self.property.size[1]], SPECIAL_CHARS["wallBL"] + SPECIAL_CHARS["wallHor"] * self.property.size[0] + SPECIAL_CHARS["wallBR"], "GREY", "BLACK")
        self.add_child(toptext)
        self.add_child(bottomText)
        vwall = SPECIAL_CHARS["wallVert"] + " " * self.property.size[0] + SPECIAL_CHARS["wallVert"] + "\n"
        vwalltext = Content([x_offset, 2], vwall * self.property.size[1], "GREY", "BLACK")
        self.add_child(vwalltext)
        

        for cabinet in self.property.cabinets:
            cab_loc = [cabinet.location[0] + x_offset, cabinet.location[1] + 1]
            cab_char = Content(cab_loc, SPECIAL_CHARS["cab"], fg = "GREEN", bg = "BLACK")
            self.add_child(cab_char)

        for c in self.customer_icons:
            self.add_child(c)

    def place_customer(self, customer):
        # TODO: colour code their frustration
        self.customer_icons.append(customer.icon)


class StatusWindow(Window):
    def __init__(self, parent, area: Rect = Rect(25,1,54,9)):
        super().__init__(parent, area, "FINANCES", fg = "LGREY", bg = "BLUE")
        # build the content, also pass data to it i guess.
        self.day_progress_bar = ProgressBar([2,1],49, 0, parent.day_length)
        self.money_label = Content([1,1], f"FUNDS: ${self.parent.money:,.2f}")


    def start_pre_day(self):
        self.children = []
        self.money_label = Content([1,1], f"FUNDS: ${self.parent.money:,.2f}")
        self.add_child(self.money_label)

        cablist = Content([1,2], f"Cabinets Owned: {len(self.parent.property.cabinets)}")
        cab_details = Button([20,2], "Details...", "BLUE", "LGREY", func=print, func_args=[self.parent.screen])
        self.add_child(cablist)
        self.add_child(cab_details)

        start_day_button = Button([10,4], "START DAY", "BLACK", "WHITE", "WHITE", "BLACK", self.parent.start_day, highlight_on_hover= True)
        self.add_child(start_day_button)

    def start_day(self):
        self.children = []
        self.day_progress_bar.set_value(0)
        self.add_child(self.day_progress_bar)
        self.money_label = Content([2,3], f"Today's Income: ${self.parent.current_day.income}")
        self.add_child(self.money_label)
        self.customer_label = Content([2,4], f"Customers: {self.parent.current_day.visitors}")
        
    def tick_day(self):
        self.day_progress_bar.set_value(self.parent.day_timer)
        self.money_label.update(new_text = f"Income: {self.parent.current_day.income}")
        self.customer_label.update(new_text = f"Customers: {self.parent.current_day.visitors}")


class GraphWindow(Window):
    def __init__(self, parent):
        super().__init__(parent, Rect(25,11,54,17), "DATA FEED",fg = "GREY", bg = "BLUE", allow_scroll= True)
        self.background = ColourBlock(Rect(0,0,52,16), ".", fg = "BLACK", bg= "BLACK")
        self.text_content = Content([1,1], "DATA FEED LIVES HERE", "WHITE", "BLACK")
        self.add_child(self.background)
        self.add_child(self.text_content)



    def add_text_line(self, new_text:str):
        new_text = self.text_content.raw_text + "\n" + new_text.format()
        
        text_size = len(new_text.splitlines())
        size_diff = text_size - self.text_content.area.height
        self.text_content.update(new_text = new_text)
        if size_diff >= 0 and text_size > self.background.area.height:
            
            self.background.change_size(Rect(self.background.area.topleft, [self.background.area.width, text_size]))
        
            self.scroll_view(y= -size_diff)


