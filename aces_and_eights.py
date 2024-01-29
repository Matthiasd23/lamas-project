import random
from model import KripkeModel
from player import Player

class AcesAndEightsGame:
    def __init__(self, num_players=3, num_cards=8):
        """Set up a new game of Aces and Eights.

        Args:
        num_players (int): The number of players in the game.
        num_cards (int): The total number of cards to be used.
        """
        self.num_players = num_players
        self.num_cards = num_cards
        self.cards = ["A"] * (num_cards // 2) + ["8"] * (num_cards // 2)
        self.players = [Player(f'Player {i+1}', self.cards) for i in range(num_players)]
        self.table = None
        self.model = KripkeModel()

    def deal_cards(self):
        """
        Give every player (and table) their cards and let all players save
        the other players' cards in their model.
        """
        random.shuffle(self.cards)
        print(f"Correct state: {(''.join(self.cards))[:-2]}")

        # Deal cards to players
        for i, player in enumerate(self.players):
            index = i * 2
            player.cards = self.cards[index:index+2]
            player.print_cards()
            player.set_knows_cards(False)
        self.table = self.cards

        # Let players save the other players' cards in their model
        for player in self.players:
            visible_cards = []
            for other_player in self.players:
                if other_player != player:
                    if other_player.cards == ["8", "A"]: # 8A is the same as A8
                        visible_cards += ["A", "8"]
                    else:
                        visible_cards += other_player.cards
                else:
                    visible_cards += [".", "."] # Regex for "don't know"
            player.set_state_regex(''.join(visible_cards))

    def make_announcements(self):
        """
        Have each player make an announcement about their knowledge state.
        """
        for player in self.players:
            player.communicate(self.model)
        self.model.display_graph()

    def check_for_winners(self):
        """Check if there are any winners and update models if the game continues."""

        winners = []
        for player in self.players:
            if player.knows_cards:
                winners.append(player)
        if len(winners) > 0:
            print(f"There is a winner! The winners are: {', '.join(winner.name for winner in winners)}!")
            return True

        # Let players update their model if no one knows their cards yet
        self.model.update_dont_know()
        print("No one knows their cards yet, playing another round.")
