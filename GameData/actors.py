# List of actors for my lil arcadey game

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


    