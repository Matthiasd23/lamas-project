import re

all_states = ['AAAA88', 'AAA8A8', 'AAA888', 'AA88AA', 'AA88A8', 'AA8888', 'A8AAA8', 'A8AA88', 'A8A8AA', 'A8A8A8', 'A8A888', 'A888AA', 'A888A8', '88AAAA', '88AAA8', '88AA88', '88A8AA', '88A8A8', '8888AA']

class KripkeModel:
    def __init__(self, cards, player_name):
        self.player_name = player_name
        self.cards = cards
        self.states = set()
        self.transitions = {player: {} for player in range(1, 4)}
        self.initialize_model()
    
    def add_state(self, state):
        self.states.add(state)

    def remove_state(self, state):
        try:
            self.states.remove(state)
            for player in self.transitions:
                if state in self.transitions[player]:
                    del self.transitions[player][state]
                for states in self.transitions[player].values():
                    if state in states:
                        states.remove(state)
        except KeyError:
            pass

    def add_transition(self, start_state, end_state, player):
        if start_state not in self.transitions[player]:
            self.transitions[player][start_state] = set()
        self.transitions[player][start_state].add(end_state)

    def remove_transition(self, start_state, end_state, player):
        self.transitions[player][start_state].remove(end_state)
    
    def initialize_model(self):
        player_one_transitions = [(1, 8), (1, 16), (8, 16), (7, 15), (2, 10), (10, 18), (2, 18), (5, 13), (4, 12), (12, 19), (4, 19), (9, 17), (3, 11)]
        player_two_transitions = [(1, 3), (1, 6), (3, 6), (7, 10), (10, 13), (7, 13), (14, 19), (14, 17), (17, 19), (9, 12), (18, 15), (2, 5), (8, 11)]
        player_three_transitions = [(4, 5), (5, 6), (4, 6), (9, 10), (9, 11), (10, 11), (14, 15), (15, 16), (14, 16), (2, 3), (12, 13), (7, 8), (17, 18)]

        for state in all_states:
            self.add_state(state)

        players_transitions = [player_one_transitions, player_two_transitions, player_three_transitions]
        for player, transition in zip(range(1, 4), players_transitions):
            for start, end in transition:
                self.add_transition(all_states[start - 1], all_states[end - 1], player)

    def update_initial_cards(self, cards):
        card_regex = ''.join(cards)
        pattern = re.compile(card_regex)
        print(f"{self.player_name} knows's cards: {card_regex}")
        states = [state for state in self.states if not pattern.match(state)]

        for state in states:
            self.remove_state(state)
        
        print(f"{self.player_name} remaining states: {self.states}")

    def update_dont_know(self):
        states_to_remove = set()
        all_transitions = set(self.states)

        for player_transitions in self.transitions.values():
            all_transitions &= set(player_transitions.keys())

        for state in self.states:
            if state not in all_transitions:
                states_to_remove.add(state)

        for state in states_to_remove:
            self.remove_state(state)

        print(f"{self.player_name} remaining states: {self.states}")
