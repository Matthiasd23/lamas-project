# probably add libraries to create the kripke world models

from model import KripkeModel


class Player:
    def __init__(self, name, all_cards):
        self.name = name
        self.cards = []
        self.knows_cards = False
        self.model = KripkeModel(all_cards, name)

    def __str__(self):
        return self.name
    
    def print_cards(self):
        print(f"{self.name}'s cards: {self.cards}")

    def set_model_state_regex(self, state_regex):
        self.model.set_state_regex(state_regex)
    
    def print_knows_cards(self):
        if self.knows_cards:
            cards = self.model.get_cards()
            print(f"{self.name} knows their cards: an " + cards[0] + " and an " + cards[1] + ".")
        else:
            print(f"{self.name} doesn't know their cards.")

    def set_knows_cards(self, knows_cards):
        self.knows_cards = knows_cards

    def deduce_cards(self):
        """
        Use the model to (possibly) deduce the cards the player has.
        """
        if self.model.deduce_state():
            self.set_knows_cards(True)

    def communicate(self):
        """
        Try to deduce cards and tell other players what you know.
        """
        self.deduce_cards()
        self.print_knows_cards()
        self.model.display_graph() # Comment out to get faster results
        return self.knows_cards
    
    def update_dont_know(self):
        """
        If everyone announces they don't know their cards, update the model.
        """
        self.model.update_dont_know()
        self.deduce_cards()
        
        