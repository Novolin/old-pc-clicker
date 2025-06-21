# Where things live for the game state, cabinets, properties, etc.

from pygame import Rect
import engine, ui
from random import randint, randrange, random


DAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
MONTHS = {"JAN":31, "FEB":28, "MAR":31, "APR":30, "MAY":31, "JUN":30, "JUL":31,"AUG":31, "SEP":30, "OCT":31, "NOV":30,"DEC":31} #months, # of days.
FIRST_NAMES = ["GARY"]
LAST_NAMES = ["CUSTOMER"]

class ArcadeProperty:
    def __init__(self) -> None:
        # TODO: Load from file/db or whatever
        self.popularity = 100
        self.base_price = 10000 # purchase price?? gotta figure out property market stuff
        self.max_cabinets = 5
        self.max_customers = 8
        self.cabinets = [Cabinet("FARTS")]
        # Tracking/stats stuff:
        self.purchase_date = 0
        self.income_history = []
        self.visit_history = []

class Customer:
    
    def __init__(self, first_name, last_name, age) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.preferences = None
        self.cash = 10.00
        self.patience = 50
        self.roughness = 1
        self.playing = False

    def play(self, cabinet):
        self.cash -= cabinet.play()

class Cabinet:
    def __init__(self, name) -> None:
        # TODO: Load from a db of cabinets. For now we'll just be generic
        self.name = name
        self.owned = False
        self.purchase_date = -1
        self.type = 0
        self.popularity = 100
        self.playercount = 1
        self.release_date = 0 # in-game day number.
        self.price = 0.25
        self.daily_earnings = []
        self.daily_plays = []
        self.maintenance_index = 1
        self.working = True
        self.active_players = 0 # How many players are on it at the moment

    def start_next_day(self):
        # Adds a new item to the daily plays, etc.
        self.daily_earnings.append(0)
        self.daily_plays.append(0)

    def play(self):
        # Called when a customer decides to play the cabinet
        self.active_players += 1
        self.daily_earnings[-1] += self.price
        self.daily_plays[-1] += 1
        return self.price


    def next_tick(self):
        self.active_players = 0

        
        

class GameDay:
    # A class to deal with the actual day.
    def __init__(self):
        self.expenses = 0.00 
        self.income = 0.00
        self.visits = 0
        self.cabinet_changes = {"Removed":[], "Added":[]}
        self.games_played = 0
        self.day_ended = False
        self.tick_counter = 0 
        self.tick_max = 184 # 5 minute chunks of a 12 hr day?
        self.current_customers = [] # Customers in the shop
        self.customers_past = [] # Customers that have left

    def do_tick(self):
        self.tick_counter += 1
        if self.tick_counter >= self.tick_max:
            self.day_ended = True
            return False
        return True


 # Parent Class for game state objects
class GameState:
    def __init__(self, display):
        self.name = "ARCADE NAME"
        self.money = 10.00
        self.property = ArcadeProperty()
        self.day = 0 # How many days you've completed.
        self.month = "JAN"
        self.year = 0
        self.month_day_counter = 1 # For calendar

        # For gameplay stuff
        self.active_day_obj = False
        self.ms_per_tick = 100 # how many ms per game logic tick
        self.tick_counter = 0 # How close ar we from our last logic tick
        
        # Display stuff:
        self.windows = display.windows
        self.menu_bar = display.menubar
        self.text_bar = display.infobar
        self.display = display


        

        # Set up the default menu bar:
        menu_bar = engine.MenuBar()
        filemenu = menu_bar.add_child_menu("FILE", 0)
        optionsmenu = menu_bar.add_child_menu("OPTIONS", 0)
        file_menu_opts = [
            engine.MenuItem("New...", filemenu, 0, ui.build_new_game_window, [self]),
            engine.MenuItem("Load...", filemenu, 0, print, ["LOAD"]),
            engine.MenuItem("Save!", filemenu, 0, print, ["SAVE"]),
            engine.MenuItem("Save As...", filemenu, 5, print, ["lol"]),
            engine.MenuItemDivider(filemenu),
            engine.MenuItem("Quit", filemenu, 0, exit)
        ]

        display.load_menu_bar(menu_bar)
        for mo in file_menu_opts:
            filemenu.add_child_item(mo)

        opt_menu_opts = [
            engine.MenuItem("Nothing lives here yet.", optionsmenu)
        ]
        for mo in opt_menu_opts:
            optionsmenu.add_child_item(mo)

    def add_window(self, window):
        # exists to parse commands from children right now
        self.display.add_window(window)

    

    def queue_destroy(self, object):
        # Queues the destruction of an object
        object.queue_destroy()

    def tick(self, delta):
        # Defined in active game states.
        pass


class MainMenu(GameState):
    def __init__(self, display):
        super().__init__(display)
        title_window = ui.Window(Rect(0,0,80,40), do_border = False)
        cool_logo = ui.TextBox([20,15], "WELCOME TO MY GAME\nITS JANK AS FUCK STILL")
        title_window.add_child(cool_logo)
        display.add_window(title_window)


class GamePlay(GameState):
    def __init__(self, display, game_source = "new"):
        super().__init__(display)
        self.active_day_obj = GameDay()
        self.active_day_obj.day_ended = True # init with a dead day
        # On init this should clear the display of all existing windows:
        for w in display.windows:
            w.queue_destroy()
        default_window = ui.Window(Rect(1,1,display.columns -2, display.rows - 3))
        if game_source == "load":
            # This is where you would load data from file and shit.
            default_window.title = "WELCOME BACK"
            default_window.add_child(ui.TextBox([5,1],"I don't have game loading working yet, so this is a new game.\nSorry, but you knew that going in."))
            default_window.add_child(ui.Button([12,5], "OK", action = default_window.queue_destroy, bg= "GREEN", fg = "BLACK"))
        
        if game_source == "new":
            default_window.title = "WELCOME!"
            default_window.add_child(ui.TextBox([5,1], "Welcome to the game,\nThis will be a real thing later."))
            default_window.add_child(ui.Button([12,5], "OK", action= default_window.queue_destroy, bg="GREEN", fg = "BLACK"))
        
        ui.build_day_start_windows(self)

        self.add_window(default_window)
        

    def start_day(self):
        # CLEAR THE FIELD
        for w in self.windows:
            w.queue_destroy()
        # Start a new day
        self.active_day_obj = GameDay()
        for cab in self.property.cabinets:
            cab.start_next_day()
        self.game_window = ui.build_day_run_windows(self, self.active_day_obj.tick_max)
        self.add_window(self.game_window)


    def tick(self, delta):
        # If we've reached our time threshold, do a logic tick.
        if self.active_day_obj.day_ended:
            return # Day is over, we don't need to do logic tick stuff.
        self.tick_counter += delta
        if self.tick_counter < self.ms_per_tick:
            return # Not ready to do logic tick yet.
        self.tick_counter -= self.ms_per_tick # shift our logic tick over
        if not self.active_day_obj.do_tick():
            self.end_day() # We've reached the end of the day, do end of day shit.
        
        # Check if a customer will come to the shop or leave:
        customers_leaving = []
        # First find any customers with no money:
        for c in self.active_day_obj.current_customers:
            if c.cash < .25:
                customers_leaving.append(c)
            elif c.patience <= 0: # or with no patience left.
                customers_leaving.append(c)
        # Get them out of the list
        self.active_day_obj.customers_past += customers_leaving
        for cust in customers_leaving:
            del self.active_day_obj.current_customers[self.active_day_obj.current_customers.index(cust)]

        # Then check how busy we are, and see if we need to nuke anyone else
        busy_ratio = len(self.active_day_obj.current_customers) / self.property.max_customers
        if busy_ratio > 0:
            chosen_customer = 0
            # If we're busy, find the most impatient customer and make them leave
            for c in self.active_day_obj.current_customers:
                if c.patience < self.active_day_obj.current_customers[chosen_customer].patience:
                    chosen_customer = self.active_day_obj.current_customers.index(c)
            if self.active_day_obj.current_customers[chosen_customer].patience < 10 * busy_ratio: # compare with our busy ratio
                self.active_day_obj.customers_past.append(self.active_day_obj.current_customers.pop(chosen_customer))

        # See if anyone wants to come
        if randrange(0,100) < self.property.popularity * 1/1+busy_ratio: #TODO: Tweak this as we go
            self.active_day_obj.current_customers.append(Customer("JOHN", "JOHNSON", randint(10,80)))


        # Clean up our cabinets:
        for cab in self.property.cabinets:
            cab.next_tick()
        
        # Assign players to cabinets:
        for cust in self.active_day_obj.current_customers:
            # TODO: check if customers want to actually play the damn things
            for cab in self.property.cabinets:
                if cab.active_players < cab.playercount and cab.price < cust.cash:
                    if randint(0,20) > 10:
                        cust.play(cab)
                        self.active_day_obj.income += cab.price
                        self.active_day_obj.games_played += 1 

        self.game_window.update(self.active_day_obj.tick_counter, self.active_day_obj.income, self.active_day_obj.games_played, len(self.active_day_obj.current_customers))


        


            
            
        

    def end_day(self):
        self.add_window(ui.build_day_summary_windows(self))

    def advance_day(self):
        for w in self.windows:
            w.queue_destroy()
        
        self.day += 1
        self.month_day_counter += 1
        if self.month_day_counter > MONTHS[self.month]:
            monthindex = list(MONTHS).index(self.month)
            monthindex += 1
            if monthindex >= len(MONTHS):
                monthindex = 0
            self.month = list(MONTHS)[monthindex]
            self.month_day_counter = 0
        
        self.add_window(ui.build_day_start_windows(self))