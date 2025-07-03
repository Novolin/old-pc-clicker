# Game-related windows and whatnot.

from pygame import Rect
from ui import *

class CalendarWindow(Window):
    def __init__(self, parent, location, month:str, day:int, year:int, size = [24, 9], fg=None, bg=None, hi=None, hi_bg=None):
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
        self.get_start_offset()
        title = f"{month}, Year {self.year}"
        super().__init__(parent, Rect(location, size), title, fg, bg, hi, hi_bg, allow_scroll= False)
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
        next_location = [1 + (self.day_offset * 3),1]
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
        
                
class PropertyMap(Window):
    def __init__(self):
        pass

class FinanceInfo(Window):
    def __init__(self, parent, area: Rect = Rect(24,1,26,9)):
        super().__init__(parent, area, "FINANCES")
        # build the content, also pass data to it i guess.