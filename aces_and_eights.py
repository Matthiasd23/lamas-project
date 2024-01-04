import random
from cardvalue import CardValue
from player import Player

class AcesAndEightsGame:
    def __init__(self, num_players=3, num_cards=8):
        self.num_players = num_players
        self.num_cards = num_cards
        self.cards = [CardValue.ACE] * (num_cards // 2) + [CardValue.EIGHT] * (num_cards // 2)
        self.players = [Player(f'Player {i+1}') for i in range(num_players)]
        self.table = None

    def deal_cards(self):
        random.shuffle(self.cards)
        for player in self.players:
            player.cards = random.sample(self.cards, 2)
            for card in player.cards:
                self.cards.remove(card)
            player.set_knows_cards(False)
        self.table = self.cards

    def make_announcements(self):
        for player in self.players:
            player.communicate()

    def check_for_winners(self):
        for player in self.players:
            if player.knows_cards:
                print(f"{player} wins!")
                return
        print("No one knows there cards yet, playing another round.")
