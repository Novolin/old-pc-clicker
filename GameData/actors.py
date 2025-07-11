# Assorted objects needed for the game, defined in one little place to keep the logic code
from pygame import Rect
from math import sqrt
from ui import Content
from GameData.windows import SPECIAL_CHARS
from collections import deque
from random import randint


MONTHS = {
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

class Cabinet:
    # loads from a csv of cabinet data.
    def __init__(self, file_data):

        self.name = file_data[0]
        self.price = 0.25
        self.description = file_data[1]
        self.release = int(file_data[2])
        self.genre = file_data[3]
        self.owned = False
        self.location = [-1,-1]
        
        self.players = int(file_data[4])
        self.play_locations = []
        self.next_play_pos = 0 # what is the next position available
        self.current_players = 0
        
        self.busy = False
        self.playtime = 5 # how many ticks does a single game last, on average

        self.historic_data = deque([],30) # Hold 30 days of historical data
        self.day_data = {"Day":0,"Plays":0,"Income":0.00}
        
    def set_position(self, new_position, property):
        self.location = new_position
        # Check what direction we can actually play from:
        self.play_locations = []
        placement_tries = self.players
        check_north = property.is_space_empty([self.location[0], self.location[1] -1])
        check_south = property.is_space_empty([self.location[0], self.location[1] +1])
        check_west = property.is_space_empty([self.location[0] - 1, self.location[1]])
        check_east = property.is_space_empty([self.location[0] + 1, self.location[1]])
        while len(self.play_locations) < self.players and len(self.play_locations) < 5:
            if placement_tries <= 0:
                break 
            placement_tries -= 1
            # check for our paired locations first:
            if len(self.play_locations) > 0:
                if [self.location[0], self.location[1] -1] in self.play_locations: # N/S
                    if check_south and [self.location[0], self.location[1] + 1] not in self.play_locations:
                        self.play_locations.append([self.location[0], self.location[1] + 1])
                        continue
                if [self.location[0] - 1, self.location[1]] in self.play_locations: #E/W
        
                    if check_west and [self.location[0] + 1, self.location[1]] not in self.play_locations:
                        self.play_locations.append([self.location[0] + 1, self.location[1]])
                        continue
            if check_north and [self.location[0], self.location[1] -1] not in self.play_locations:
                self.play_locations.append([self.location[0], self.location[1] - 1])
                continue
            if check_east and [self.location[0] - 1, self.location[1]] not in self.play_locations:
                self.play_locations.append([self.location[0] - 1, self.location[1]])
                continue
            if check_south and [self.location[0], self.location[1] + 1] not in self.play_locations:
                self.play_locations.append([self.location[0], self.location[1] + 1])
                continue
            if check_west and [self.location[0] + 1, self.location[1]] not in self.play_locations:
                self.play_locations.append([self.location[0] + 1, self.location[1]])

    def start_play(self, customer):
        self.current_players += 1
        self.next_play_pos += 1
        if self.current_players >= self.players:
            self.busy = True
        self.day_data["Plays"] += 1
        self.day_data["Income"] += self.price
        customer.money -= self.price
        

    def end_play(self, customer):
        if self.busy:
            self.busy = False
        self.current_players -= 1
        if self.play_locations.index(customer.location) < self.next_play_pos:
            self.next_play_pos = self.play_locations.index(customer.location)
        # This is where we would roll to see if it breaks.
    
class PropertyDoor:
    # A lil baby class for the entry/exit door of a property
    def __init__(self, x, y):
        self.location = [x,y]


class Customer:
    # TODO: load customer data from file
    def __init__(self, active_property):
        # Set per customer profile
        self.name = "LARRY"
        self.preference = "MAZE"
        self.money = 50.00
        self.patience = 100
        # To be set by the game as they play stuff:

        self.location = [-1,-1]
        self.playing = None
        self.play_timer = 0 # how long have we been playing our cabinet
        self.state = "ENTER" # What are they doing? 
        self.target = None
        self.target_loc = [0,0]
        self.act_timer = 0 # How long for our action to expire
        self.active_property = active_property
        # Visual representation:
        self.icon = Content(self.location, SPECIAL_CHARS["smiley"], "GREEN", "BLACK")
        # If they are ready to leave:
        self.destroy = False
        
    def enter_property(self, new_property):
        pass

    def set_location(self, new_location:list|tuple):
        self.location = list(new_location)
        self.icon.area.update(self.location, (1,1))
    
    def do_action(self) -> str:
        # Chooses and executes an action.
        if self.state == "PLAY":
            self.act_timer -= 1
            if self.act_timer < 1 and self.target != None:
                self.target.end_play(self)
                self.state = "WANDER"
                self.target = None
                self.act_timer = 3 # wander for 3 ticks before playing again
                self.wander()
                return "FINISH"
            return "PLAY"
        elif self.state == "WAIT":
            self.act_timer += 1
            if self.target and self.target.busy:
                self.patience -= self.act_timer # longer waits = higher patience penalty
                if self.act_timer > self.patience // 10: # they've been waiting too long
                    self.get_new_target()
                    return "WAIT_BAD"
                return "WAIT"

        elif self.state == "WANDER" or self.target == None:
            self.act_timer -= 1
            self.wander()
            if self.act_timer < 1:
                self.get_new_target()
            return "MOVE"
            
        elif self.state == "LEAVE":
            if self.move_to_target():
                self.destroy = True
                return "LEFT"
            return "MOVE"
        elif self.state == "MOVE":
            if self.target.busy:
                self.state ="WANDER"
                self.patience -= 5

            elif self.move_to_target():
                self.state = "PLAY"                
                self.target.start_play(self)
                return "PLAYSTART"
        elif self.state == "ENTER":
            if randint(0,10) < 7:
                self.get_new_target()
                if self.move_to_target():
                    self.state = "PLAY"
                    self.target.start_play(self)
                    return "PLAYSTART"
                    
            else:
                self.state = "WANDER"
                self.wander()
        return self.state

    def get_new_target(self):
        new_target = None

        for cab in self.active_property.cabinets:
            
            if cab.busy:
                continue # skip currently occupied cabinets
            elif new_target == None: # always take the first available cabinet, as a backup
                new_target = cab
            elif cab.genre == self.preference and new_target.genre != self.preference: # always prefer a cabinet in our favourite genre, even if further away
                new_target = cab
            elif get_distance(self.location, new_target.location) > get_distance(self.location, cab.location): # otherwise bias towards the closest cabinet
                new_target = cab

        if new_target == None:
            self.target = None
            self.state = "WANDER"
        else:
            self.state = "MOVE"
            self.target = new_target
            self.target_loc = new_target.play_locations[new_target.next_play_pos]
            if self.target.genre == self.preference:
                self.patience += 1 # make us a little happier if we see our faves!!
            

    def wander(self):
        self.target_loc = [randint(0,self.active_property.size[0]), randint(0,self.active_property.size[1])]
        self.move_to_target()

    def move_to_target(self)-> bool:
        # moves the customer towards their target
        if self.location != self.target_loc:
            # find the direction to go:
            move_x = 0
            move_y = 0
            if self.location[0] > self.target_loc[0]:
                move_x = -1
            elif self.location[0] < self.target_loc[0]:
                move_x += 1
            if self.location[1] > self.target_loc[1]:
                move_y = -1
            elif self.location[1] < self.target_loc[1]:
                move_y = 1
            try_location = [self.location[0] + move_x, self.location[1] + move_y]
            if self.active_property.is_space_empty(try_location):
                self.location = try_location
            elif self.active_property.is_space_empty([self.location[0] + move_x, self.location[1]]) and move_x != 0:
                self.location = try_location
            elif self.active_property.is_space_empty([self.location[0], self.location[1] + move_y]) and move_y != 0:
                self.location = try_location
        self.icon.area.update(self.location, (1,1))
        if self.location == self.target_loc:
            return True
        else:
            return False

class Property:
    # TODO: Pull data from file
    def __init__(self, game_data) -> None:
        # Pull the data from a JSON or whatever
        # but for now we only have one so just hard code it.
        self.size = [7,3] # how many tiles is it in x/y
        self.cabinets = []
        self.cab_max = 3
        self.name = "GARAGE"
        self.cab_positions = [[1,3], [3,3], [5,5]] # where are cabinets at.
        self.exit = PropertyDoor(self.size[0]//2, 1)
        self.capacity = 2 # how many people can be in here at once.
        self.popularity = 100 # how likely are people to come here.
        self.customers = []
        self.parent = game_data # The GameData object for our parent
        
    def add_cabinet(self, cabinet):
        cabinet.set_position(self.cab_positions[len(self.cabinets)], self)
        self.cabinets.append(cabinet)
        
    def add_customer(self, customer):
        customer.set_location(self.exit.location)
        self.customers.append(customer)
        

    def remove_customer(self, customer):
        if customer in self.customers:
            self.customers.remove(customer)

    def find_free_space(self, start_space:list|tuple):
        # Returns a coordinate with nothing inside of it.
        while True:
            
            space = [randint(0,self.size[0]), randint(0, self.size[1])]
            if space == list(start_space):
                valid_space = False
            else:
                valid_space = self.is_space_empty(space)
            if valid_space:
                break

        return space


    def is_space_empty(self, target:list):
        is_empty = True
        if target[0] < 0 or target[0] > self.size[0] or target[1] < 0 or target[1] > self.size[1]:
            return False # Out of bounds
        for cabinet in self.cabinets:
            if list(cabinet.location) == target:
                is_empty = False
        for customer in self.customers:
            if customer.location == target:
                is_empty = False
        return is_empty
    
def get_distance(point_one, point_two):
    # returns the distance between two points
    x_dist = abs(point_one[0] - point_two[0])
    y_dist = abs(point_one[1] - point_two[1])
    return sqrt(x_dist ** 2 + y_dist ** 2)
    



class Date:
    # A single day's worth of data:
    def __init__(self, absolute_day):
        self.absolute_day = absolute_day
        self.year = absolute_day // 365
        # Calculate the month/remaining day:
        self.month = "JAN"
        day_counter = absolute_day % 365
        while day_counter > MONTHS[self.month]:
            monthindex = list(MONTHS).index(self.month)
            day_counter -= MONTHS[self.month]
            self.month = list(MONTHS)[monthindex + 1]
        self.day = day_counter
        self.income = 0
        self.expenses = 0
        self.visitors = 0
        self.income_per_cabinet = {}


    def add_transaction(self, cabinet, amount):
        if cabinet in self.income_per_cabinet.keys():
            self.income_per_cabinet[cabinet] += amount
        else:
            self.income_per_cabinet[cabinet] = amount
        if amount > 0:
            self.income += amount
        else:
             self.expenses += amount