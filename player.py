import re
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
        self.state_regex = ""
        self.actual_cards = []

    def __str__(self):
        """Provide a string representation of the Player, which is their name."""
        return self.name
    
    def print_cards(self):
        """Print the player's cards to the console."""
        print(f"{self.name}'s cards: {self.cards}")

    def set_state_regex(self, state_regex):
        """Set the state regex for this player's Kripke model to reflect known card information.

        Args:
        state_regex (str): A regex pattern representing the cards this player can see.
        """
        self.state_regex = state_regex
    
    def print_knows_cards(self):
        """Print a statement to the console indicating whether the player knows their cards."""
        if self.knows_cards:
            print(f"{self.name} knows their cards: an " + self.actual_cards[0] + " and an " + self.actual_cards[1] + ".")
        else:
            print(f"{self.name} doesn't know their cards.")

    def set_knows_cards(self, knows_cards):
        """Set the knows_cards attribute to reflect whether the player knows their cards.

        Args:
        knows_cards (bool): True if the player knows their cards, False otherwise.
        """
        self.knows_cards = knows_cards

    def deduce_cards(self, model: KripkeModel):
        """
        Deduce actual state by removing states that don't match the state regex (cards a player knows) 
        and checking whether there is only one state left.

        Returns:
        bool: True if the state could be deduced, False otherwise.
        """
        if self.state_regex:
            pattern = re.compile(self.state_regex)
            states = [state for state in model.states if not pattern.match(state)]
            all_states = list(model.states)

            for state in states:
                all_states.remove(state)

            if len(all_states) == 1:
                correct_state = list(all_states)[0]
                location = int(self.name[-1]) * 2
                cards = correct_state[location - 2:location]
                self.actual_cards = cards
                self.knows_cards = True

    def communicate(self, model: KripkeModel):
        """
        Try to deduce cards and tell other players what you know.
        """
        self.deduce_cards(model)
        self.print_knows_cards()
        return self.knows_cards
        
        