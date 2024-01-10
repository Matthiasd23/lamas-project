# probably add libraries to create the kripke world models

from model import KripkeModel


class Player:
    def __init__(self, name, all_cards):
        self.name = name
        self.cards = []
        self.knows_cards = False
        self.model = KripkeModel(all_cards, name)
        self.model.initialize_model()

    def __str__(self):
        return self.name
    
    def print_cards(self):
        print(f"{self.name}'s cards: {self.cards}")

    def update_initial_model(self, cards):
        self.model.update_initial_cards(cards)
        self.deduce_cards()
    
    def print_knows_cards(self):
        if self.knows_cards:
            state = list(self.model.states)[0]
            location = int(self.name[-1])*2
            cards = state[location-2:location]
            print(f"{self.name} knows their cards: an " + cards[0] + " and an " + cards[1] + ".")
        else:
            print(f"{self.name} doesn't know their cards.")

    def set_knows_cards(self, knows_cards):
        self.knows_cards = knows_cards

    def deduce_cards(self):
        if len(self.model.states) == 1:
            self.set_knows_cards(True)

    def communicate(self):
        self.print_knows_cards()
        
        return self.knows_cards
    
    def update_dont_know(self):
        self.model.update_dont_know()
        self.deduce_cards()
        
        