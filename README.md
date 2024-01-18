# AcesAndEights Game

## Overview

This project implements the card game "Aces and Eights" and includes several classes to model the game, players, and a Kripke model in order to reason about player knowledge.

## Files

### `main.py`

This file should be used to run the game. It runs the four rounds necessary for a complete game. This is how the game can be run:

```python
pip install -r requirements.txt
python3 main.py
```

### `aces_and_eights_game.py`

This file contains the main class `AcesAndEightsGame`. This class initializes the game with a specified number of players (3) and cards (8). It provides methods for dealing cards, making announcements, and checking for winners.

### `player.py`

The `Player` class is defined in this file. Each player keeps track of their cards, knowledge of the game state (by updating their KripkeModel), and interacts with others by commmunicating their knowledge of their cards.

### `model.py`

The `KripkeModel` class (based on NetworkX) is in here. It gives a Kripke model for modeling player knowledge in the game. The model can be updated when all players announce "I don't know my cards" and checked for the true state, based on the player's knowledge of the possible states (given by the other player's cards).

## Dependencies
- NetworkX
- Matplotlib