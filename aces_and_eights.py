import random
from cardvalue import CardValue
from player import Player

class AcesAndEightsGame:
    def __init__(self, num_players=3, num_cards=8):
        self.num_players = num_players
        self.num_cards = num_cards
        self.cards = ["A"] * (num_cards // 2) + ["8"] * (num_cards // 2)
        self.players = [Player(f'Player {i+1}', self.cards) for i in range(num_players)]
        self.table = None

    def deal_cards(self):
        random.shuffle(self.cards)
        print(f"Cards: {''.join(self.cards)}")

        for i, player in enumerate(self.players):
            index = i * 2
            player.cards = self.cards[index:index+2]
            player.print_cards()
            player.set_knows_cards(False)
        self.table = self.cards

        for player in self.players:
            visible_cards = []
            for other_player in self.players:
                if other_player != player:
                    if other_player.cards == ["8", "A"]: # 8A is the same as A8
                        visible_cards += ["A", "8"]
                    else:
                        visible_cards += other_player.cards
                else:  # Use regex for correct search?
                    visible_cards += [".", "."]
            player.update_initial_model(visible_cards)

    def make_announcements(self):
        for player in self.players:
            player.communicate()

    def check_for_winners(self):
        for player in self.players:
            if player.knows_cards:
                print(f"{player} wins!")
                return True
        for player in self.players:
            player.update_dont_know()
        print("No one knows there cards yet, playing another round.")
