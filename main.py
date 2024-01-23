from aces_and_eights import AcesAndEightsGame
import shutil
import os

if __name__ == "__main__":
    """Run a game of Aces and Eights."""
    # Reinstantiate the folder for visualizations
    shutil.rmtree("visualization")
    os.makedirs("visualization")

    game = AcesAndEightsGame()
    game.deal_cards()

    # Assume 4 rounds for demonstration
    # Since that is the max needed to deduce anyone's cards
    for round_num in range(4):  
        print(f"\nRound {round_num + 1}:")

        game.make_announcements()
        if game.check_for_winners():
            break