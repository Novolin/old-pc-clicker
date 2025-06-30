from pygame import Rect
from engine import *
from ui import *
from GameData.windows import *

DAY_START = 0
DAY_RUN = 1
DAY_END = 2

# Game-related fun stuff :)

class GameData:
    def __init__(self, parent_state, from_file = False):
        # Economy
        self.money = 0.00
        self.cabinets = []
        self.property = []
        # time
        self.day = 0
        self.month = 0
        self.year = 0
        self.day_state = DAY_START
        if from_file:
            print("dunno how to load yet.")
    def start_pre_day(self):
        # Starts the next day, opens the correct windows, etc.
        self.day += 1


class GameState(StateManager):
    # Specifically for my arcadey game thing.
    def __init__(self, grid: GridManager) -> None:
        super().__init__(grid)
        self.game_data = []
        
        self.test_var = 0
        self.test_dir = 0
        self.target = 300 # should be 5 seconds worth of time.
        self.bar = None
        self.boot()

    def unhandled_input(self, key):
        if key == pygame.K_f:
            self.test_var += 5
            if self.test_var > self.target:
                self.test_var = 0
            if self.bar:
                self.bar.set_value(self.test_var)
                
                

    def boot(self):
        # Builds the menus and windows for initial boot:
        filemenu = Menu("FILE", 0)
        newgame = MenuItem(filemenu, "New...", 0, open_new_game_menu, [self])
        loadgame = MenuItem(filemenu, "Load...", 0, print, ["ass"])
        savegame = MenuItem(filemenu, "Save...", 0, print, ["save..."])
        savegame.enabled = False
        quit = MenuItem(filemenu, "Exit", 1, self.quit, None)
        
        filemenu.add_child(newgame)
        filemenu.add_child(loadgame)
        filemenu.add_child(savegame)
        filemenu.add_child(quit)

        self.add_menu(filemenu)
    

        hellowindow = Window(Rect(10,15,40, 10), "")
        hello_text = Content([5,2], "WELCOME TO THE THING I GUESS")
        hellowindow.add_child(hello_text)
        self.add_window(hellowindow)
        self.DEBUG_draw_cool_windows()

    def program_logic(self, delta):
        if self.bar:
            self.test_var += 1 
            if self.test_var > self.target + 100:
                self.test_var = 0
            self.bar.set_value(self.test_var)
            
                



    def DEBUG_draw_cool_windows(self):
        self.windows = []
        # Draws a handful of windows to test stuff
        cal = CalendarWindow([1,1], "JAN", 20, 1)
        data_window = Window(Rect(cal.area.right + 1, cal.area.top, 20,14), "data testin", allow_scroll= True)
        pbar = ProgressBar([1,0], 10, self.test_var, self.target)
        data_window.add_child(pbar)
        some_text = Content([1,1], "PROGRESS BAR")
        data_window.add_child(some_text)
        text_entry = TextEntry([1,3], 10, 1, self, "placeholder", 10, bg = "LBLUE")
        data_window.add_child(text_entry)
        ent_label = Content([1,4], "TEXT ENTERER")
        data_window.add_child(ent_label)
        mline = TextEntry([1,5], 10, 4, self, "MLINE", bg = "YELLOW", fg = "BLACK")
        data_window.add_child(mline)
        self.add_window(cal)
        self.add_window(data_window)
        self.bar = pbar
        scrollwindow = Window(Rect(1,11,10,5), "SCROLL TEST", "RED", "LRED", allow_scroll = True, show_close= True)
        a_thing = Content([1,0], "one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten")
        scrollwindow.add_child(a_thing)
        self.add_window(scrollwindow)



def open_new_game_menu(state_target:GameState):
    # Opens the new game menu
    center = [state_target.grid_size[0] // 2, state_target.grid_size[1] // 2]
    newgame = ConfirmWindow(Rect(center[0] - 18,center[1] -4,35,6), "START NEW GAME?", "Start a new game?\nUnsaved progress will be lost!", state_target.DEBUG_draw_cool_windows) 

    state_target.add_window(newgame)

