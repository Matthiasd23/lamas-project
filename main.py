from aces_and_eights import AcesAndEightsGame

if __name__ == "__main__":
    game = AcesAndEightsGame()
    game.deal_cards()

    for round_num in range(3):  # Assuming 3 rounds for demonstration
        print(f"\nRound {round_num + 1}:")

        game.make_announcements()