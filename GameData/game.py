from pygame import Rect
from engine import *
from ui import *
from GameData.windows import *
from GameData.actors import *

DAY_START = 0
DAY_RUN = 1
DAY_END = 2



# Game-related fun stuff :)

class GameData:
    def __init__(self, parent_state:StateManager, from_file = False):
        # Engine stuff:
        self.screen = parent_state
        
        # Economy
        self.money = 500.00
        self.cabinets = [Cabinet("PARK MAN", 0.25, 0)]
        self.property = []
        self.customers = [] # customers currently in the arcade




        # time
        self.day = 0
        self.month = "JAN"
        self.year = 0
        self.day_state = DAY_START
        self.day_length = 2 * 60 * 1000 # how long in ms will a day last
        self.day_timer = 0 # counter for day length
        
        
        if from_file:
            print("dunno how to load yet.")

        


    def start_pre_day(self):
        # Starts the next day, opens the correct windows, etc.
        for w in self.screen.windows:
            w.queue_destroy()
        self.day += 1
        
        calwindow = CalendarWindow(self, [0,1], self.month, self.day, self.year )
        self.screen.add_window(calwindow)

        financewindow = Window(self, Rect(25,1,40,9), "FINANCES")
        self.screen.add_window(financewindow)

        cashlabel = Content([1,1], f"FUNDS: ${self.money:,.2f}")
        financewindow.add_child(cashlabel)

        cablist = Content([1,2], f"Cabinets Owned: {len(self.cabinets)}")
        cab_details = Button([20,2], "Details...", "BLUE", "LGREY", func=DEBUG_test_windows, func_args=[self.screen])
        financewindow.add_child(cablist)
        financewindow.add_child(cab_details)
        startdaywindow = Window(self, Rect(1,12,70, 10), "")
        start_day_button = Button([30,2], "START DAY")

        startdaywindow.add_child(start_day_button)
        self.screen.add_window(startdaywindow)



    def start_day(self):
        self.day_state = DAY_RUN
        # now we do the real calculations

    def tick_day_logic(self):
        # Don't worry about frame rate
        pass


class GameState(StateManager):
    # Specifically for my arcadey game thing.
    def __init__(self, grid: GridManager) -> None:
        super().__init__(grid)
        self.game_data = GameData(self)
        self.boot()

    def unhandled_input(self, key):
        pass
                
                

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
    

        optionsmenu = Menu("OPTIONS", 0)
        textsize = MenuItem(optionsmenu, "Text Size", 0, print, ["Not Implemented Yet :("])
        optionsmenu.add_child(textsize)

        self.add_menu(optionsmenu)

        hellowindow = Window(self,Rect(5,5,40, 10), "")
        hello_text = Content([5,2], "WELCOME TO THE THING I GUESS")
        hellowindow.add_child(hello_text)
        self.add_window(hellowindow)
        

    def program_logic(self, delta):
        if self.game_data.day_state == DAY_RUN:
            pass # Tick the logic
            
                
    def start_new_game(self):
        self.game_data = GameData(self)
        self.game_data.start_pre_day()




def open_new_game_menu(state_target:GameState):
    # Opens the new game menu
    center = [state_target.grid_size[0] // 2, state_target.grid_size[1] // 2]
    newgame = ConfirmWindow(state_target, Rect(center[0] - 18,center[1] -4,35,6), "START NEW GAME?", "Start a new game?\nUnsaved progress will be lost!", state_target.start_new_game) 

    state_target.add_window(newgame)



