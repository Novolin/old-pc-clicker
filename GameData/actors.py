# List of actors for my lil arcadey game
from pygame import Rect


class Cabinet:
    # TODO: load from file
    def __init__(self, name, price, release):
        self.name = name
        self.price = price
        self.release = release
        


class Customer:
    # TODO: load customer data from file
    def __init__(self):
        self.name = "LARRY"
        self.preference = "ACTION"
        self.money = 50.00
        self.patience = 100
        self.location = [0,0]
        self.playing = False
        


class EconomyDay:
    # An object to represent the economic things that happened on a given day
    def __init__(self, day_id) -> None:
        self.income = 0.00
        self.expenses = 0.00
        self.customer_count = 0
        self.customer_list = []
        self.cabinet_incomes = {} # Dict of cabinet objects as keys, amount of income as values
        

class Property:
    def __init__(self, data) -> None:
        # Pull the data from a JSON or whatever
        # but for now we only have one so just hard code it.

        self.cabinets = []
        self.cab_max = 3
        self.name = "GARAGE"
        self.cab_positions = [(1,1), (1,4), (4,1)] # where are cabinets at.
        self.door_position = [(4,4)] # Where do customers enter
        
        