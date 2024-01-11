import re
import networkx as nx
import matplotlib.pyplot as plt

all_states = ['AAAA88', 'AAA8A8', 'AAA888', 'AA88AA', 'AA88A8', 'AA8888', 'A8AAA8', 'A8AA88', 'A8A8AA', 'A8A8A8', 'A8A888', 'A888AA', 'A888A8', '88AAAA', '88AAA8', '88AA88', '88A8AA', '88A8A8', '8888AA']

class KripkeModel:
    def __init__(self, cards, player_name):
        self.player_name = player_name
        self.cards = cards
        self.states = set()
        self.transitions = {player: {} for player in range(1, 4)}
        self.initialize_model()
        self.state_regex = ""

    def __str__(self):
        model_str = f"Player Name: {self.player_name}\n"
        model_str += f"Player Cards: {self.cards}\n"
        model_str += f"States: {', '.join(self.states)}\n"

        for player, transitions in self.transitions.items():
            model_str += f"\nTransitions for Player {player}:\n"
            for start_state, end_states in transitions.items():
                for end_state in end_states:
                    model_str += f"{start_state} -> {end_state}\n"

        return model_str

    def set_state_regex(self, state_regex):
        self.state_regex = state_regex

    def get_cards(self):
        return self.cards

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

    def deduce_states(self):
        if self.state_regex:
            print(f"{self.player_name} state regex: {self.state_regex}")
            pattern = re.compile(self.state_regex)
            states = [state for state in self.states if not pattern.match(state)]
            all_states = self.states

            for state in states:
                all_states.remove(state)

            if len(all_states) == 1:
                correct_state = list(all_states)[0]
                location = int(self.player_name[-1])*2
                cards = correct_state[location-2:location]
                self.cards = cards
                return True

        return False

    def update_dont_know(self):
        states_to_remove = set()
        all_transitions = set(self.states)

        # This is not correct: 88AAA8
        for idx, player_transitions in enumerate(self.transitions.values()):
            states_to_keep = set()
            for key, values in player_transitions.items():
                if len(values) > 0:
                    states_to_keep.add(key)
                for value in values:
                    states_to_keep.add(value)
            # print(f"Player {idx + 1} transitions: {player_transitions.items()}")
            # print(f"Player {idx + 1} transitions: {player_transitions.values()}")
            all_transitions &= states_to_keep

        for state in self.states:
            if state not in all_transitions:
                states_to_remove.add(state)

        for state in states_to_remove:
            self.remove_state(state)

        print(f"{self.player_name} removing states: {states_to_remove}")
        print(self)

    def display_graph(self):
        G = nx.DiGraph()
        for state in self.states:
            G.add_node(state)
        for player, transitions in self.transitions.items():
            for start_state, end_states in transitions.items():
                for end_state in end_states:
                    G.add_edge(start_state, end_state, player=player)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000)
        edge_labels = nx.get_edge_attributes(G, 'player')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()
