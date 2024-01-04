# probably add libraries to create the kripke world models

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.knows_cards = False

    def __str__(self):
        return self.name
    
    def print_cards(self):
        print(f"{self.name}'s cards: {self.cards}")
    
    def print_knows_cards(self):
        if self.knows_cards:
            print(f"{self.name} knows their cards: {self.knows_cards}")
        else:
            print(f"{self.name} doesn't know their cards.")

    def set_knows_cards(self, knows_cards):
        self.knows_cards = knows_cards

    def deduce_cards(self):
        pass

    def communicate(self, players):
        
        self.print_knows_cards()
        pass