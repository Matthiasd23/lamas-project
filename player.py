from model import KripkeModel


class Player:
    def __init__(self, name, all_cards):
        """Create a new Player with a given name and set of all possible cards.

        Args:
        name (str): The name of the player.
        all_cards (list): A list of all possible cards in the game.
        """
        self.name = name
        self.cards = []
        self.knows_cards = False
        self.model = KripkeModel(all_cards, name)

    def __str__(self):
        """Provide a string representation of the Player, which is their name."""
        return self.name
    
    def print_cards(self):
        """Print the player's cards to the console."""
        print(f"{self.name}'s cards: {self.cards}")

    def set_model_state_regex(self, state_regex):
        """Set the state regex for this player's Kripke model to reflect known card information.

        Args:
        state_regex (str): A regex pattern representing the cards this player can see.
        """
        self.model.set_state_regex(state_regex)
    
    def print_knows_cards(self):
        """Print a statement to the console indicating whether the player knows their cards."""
        if self.knows_cards:
            cards = self.model.get_cards()
            print(f"{self.name} knows their cards: an " + cards[0] + " and an " + cards[1] + ".")
        else:
            print(f"{self.name} doesn't know their cards.")

    def set_knows_cards(self, knows_cards):
        """Set the knows_cards attribute to reflect whether the player knows their cards.

        Args:
        knows_cards (bool): True if the player knows their cards, False otherwise.
        """
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
        # self.model.display_graph() # Commented out to not spam the console
        return self.knows_cards
    
    def update_dont_know(self):
        """
        If everyone announces they don't know their cards, update the Kripke model.
        """
        self.model.update_dont_know()
        self.deduce_cards()
        
        