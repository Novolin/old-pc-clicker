from pygame import Rect
from engine import *
from ui import *
from GameData.windows import *
from GameData.actors import *
import random
import csv




DAY_START = 0
DAY_RUN = 1
DAY_END = 2



# Game-related fun stuff :)

class GameData:
    def __init__(self, parent_state:StateManager, from_file = False):
        # Engine stuff:
        self.screen = parent_state
        self.signals = [] # a list of signals we've received from children    


        # Economy
        self.money = 500.00
        self.property = Property(parent_state)
        self.customers = [] # customers currently in the arcade
        self.historic_data = deque([], 30) # 30 days of economic data



        # time
        self.day = 0
        self.month = "JAN"
        self.year = 0
        self.running_day_count = 0
        self.current_day = Date(self.running_day_count)
        

        self.day_state = DAY_START
        self.day_length = 40 * 1000 # how long in ms will a day last ??? 
        self.day_timer = 0 # counter for day length
        self.movement_rate_ms = 800 # how many ms between customer steps. keeping it slow for now.
        self.move_timer = 0
        
        
        if from_file:
            print("dunno how to load yet.")

        # Set windows:
        self.calendar = CalendarWindow(self, [0,1], self.month, self.day, self.year)
        self.status_window = StatusWindow(self)
        self.property_map = PropertyMap(self, self.property)
        self.feed_window = GraphWindow(self)

        

    def boot(self):
        self.screen.add_window(self.calendar)
        self.screen.add_window(self.status_window)
        self.screen.add_window(self.property_map)
        self.screen.add_window(self.feed_window)

    def increment_day(self, days = 1):
        self.day += days
        self.running_day_count += days
        if self.day > MONTHS[self.month]:
            self.day -= MONTHS[self.month]
            monthindex = list(MONTHS).index(self.month)
            monthindex += 1
            if monthindex > 11:
                monthindex = 0
                self.year += 1
            self.month = list(MONTHS)[monthindex]
        elif self.day < 1:
            monthindex = list(MONTHS).index(self.month)
            monthindex -=1
            if monthindex <0:
                monthindex = 12 + monthindex
                self.year -= 1
            self.month = list(MONTHS)[monthindex]
            self.day += MONTHS[self.month]



    def start_pre_day(self):
        # Starts the next day, opens the correct windows, etc.


        self.increment_day()
        self.calendar.set_date(self.month, self.day, self.year)
        self.property_map.draw_map()
        self.status_window.start_pre_day()


    def add_customer(self):
        # TODO: this is where you generate them i guess
        new_customer = Customer(self.property)
        self.customers.append(new_customer)
        self.property.add_customer(new_customer)


    def start_day(self):
        # First clean up the last day's mess:
        self.historic_data.appendleft(self.current_day)
        self.current_day = Date(self.running_day_count)
        # Then we start a fresh day!!!
        self.day_state = DAY_RUN
        self.status_window.start_day()

        
    
        

    def tick_day_logic(self, delta):
        self.day_timer += delta
        self.move_timer += delta
        if len(self.customers) < self.property.capacity:
            if self.property.popularity > random.randint(0,40):
                self.add_customer()
                self.feed_window.add_text_line(f"{self.customers[-1].name} came in!")
                self.current_day.visitors += 1
                
                    
                    
        if self.move_timer > self.movement_rate_ms:
            self.move_timer -= self.movement_rate_ms
            for cust in self.customers:
                cust.do_action()
        if self.day_timer <= self.day_length:
            self.status_window.tick_day()
        else:
            self.end_day()
        
        
        
        # get the customers to do things and report them in our text window:
        if self.move_timer > self.movement_rate_ms:
            self.move_timer -= self.movement_rate_ms
            for cust in self.customers:
                if cust.destroy:
                    self.customers.remove(cust)
                    continue
                action = cust.do_action()
                if action == "PLAYSTART":
                    self.feed_window.add_text_line(f"{cust.name} started playing {cust.target.name}!")
                    self.money += cust.target.price
                    self.current_day.add_transaction(cust.target, cust.target.price)
                elif action == "LEFT":
                    self.feed_window.add_text_line(f"{cust.name} left!")


                self.property_map.place_customer(cust)
        # Draw property window:
        self.property_map.draw_map() 


        
    def end_day(self):
        print("DAY OVER")
        self.day_state = DAY_END

        #TODO: spawn end of day windows, etc.

class GameState(StateManager):
    # Specifically for my arcadey game thing.
    def __init__(self, grid: GridManager) -> None:
        super().__init__(grid)
        self.game_data = GameData(self)
        self.cabinets = [] # big list of cabinets
        self.customers = [] # big list of customers
        self.boot()
        
    # Redefined parent funcs:

    def unhandled_input(self, key):
        pass
                
                
    def program_logic(self, delta):
        if self.game_data.day_state == DAY_RUN:
            self.game_data.tick_day_logic(delta)
            
    # Setup functions:

    def boot(self):
        # Builds the menus and windows for initial boot:
        self.filemenu = Menu("FILE", 0)
        newgame = MenuItem(self.filemenu, "New...", 0, open_new_game_menu, [self])
        loadgame = MenuItem(self.filemenu, "Load...", 0, print, ["ass"])
        savegame = MenuItem(self.filemenu, "Save...", 0, print, ["save..."])
        savegame.enabled = False
        quit = MenuItem(self.filemenu, "Exit", 1, self.quit, None)
        
        self.filemenu.add_child(newgame)
        self.filemenu.add_child(loadgame)
        self.filemenu.add_child(savegame)
        self.filemenu.add_child(quit)

        self.add_menu(self.filemenu)
    

        self.optionsmenu = Menu("OPTIONS", 0)
        textsize = MenuItem(self.optionsmenu, "Text Size", 0, print, ["Not Implemented Yet :("])
        self.optionsmenu.add_child(textsize)

        self.add_menu(self.optionsmenu)

        hellowindow = Window(self,Rect(5,5,40, 10), "")
        hello_text = Content([5,2], "WELCOME TO THE GAME")
        start_button = Button([10,4], "START NEW GAME", "GREEN", "GREY", func=open_new_game_menu, func_args=[self])
        hellowindow.add_child(hello_text)
        hellowindow.add_child(start_button)
        self.add_window(hellowindow)
        self.load_data()
        


    def load_data(self):
        # Load the data for the game itself
        load_screen = Window(self, Rect(1,2,78, 27), "")
        load_bar = ProgressBar([10,10],50)
        load_label = Content([10,9], "Loading...")
        load_type = Content([10,11], "Preloading...")
        self.add_window(load_screen)
        load_screen.add_child(load_bar)
        load_screen.add_child(load_label)
        load_screen.add_child(load_type)
        self.force_screen_refresh() # draw our window instantly.

        # Todo: have a big list of customers
        custlist = []
        cablist = []
        
        with open("GameData/cabinetlist.csv", "r") as cabfile:
            cabreader = csv.reader(cabfile, delimiter = ";")
            for line in cabreader:
                cablist.append(line)
        total_items = len(custlist) + len(cablist)
        load_bar.target_val = total_items + 10

        load_type.update(new_text = "Loading Cabinets...")
        load_bar.set_value(8)
        self.force_screen_refresh()
        for c in cablist:
            load_bar.increment_value(1)
            self.force_screen_refresh()
            self.cabinets.append(Cabinet(c))
        load_screen.queue_destroy()

    def start_new_game(self):
        self.game_data = GameData(self)
        self.game_data.property.add_cabinet(self.cabinets[0])
        self.game_data.boot()
        self.game_data.start_pre_day()


def open_new_game_menu(state_target:GameState):
    # Opens the new game menu
    center = [state_target.grid_size[0] // 2, state_target.grid_size[1] // 2]
    newgame = ConfirmWindow(state_target, Rect(center[0] - 18,center[1] -4,35,6), "START NEW GAME?", "Start a new game?\nUnsaved progress will be lost!", state_target.start_new_game) 

    state_target.add_window(newgame)

