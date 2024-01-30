import re
import networkx as nx
import matplotlib.pyplot as plt
import copy

# All possible states of the game, taking into account that A8 is the same as 8A.
all_states = ['AAAA88', 'AAA8A8', 'AAA888', 'AA88AA', 'AA88A8', 'AA8888', 'A8AAA8', 'A8AA88', 'A8A8AA', 'A8A8A8',
              'A8A888', 'A888AA', 'A888A8', '88AAAA', '88AAA8', '88AA88', '88A8AA', '88A8A8', '8888AA']


class KripkeModel(nx.Graph):
    """
    Kripke model based on the networkx DiGraph class.
    Also adjusts the nodes and edges to be called states and transitions.

    """

    def __init__(self):
        """Initialize a new Kripke model.

        Args:
        cards (list): A list of cards in the game.
        player_name (str): The name of the player associated with this model.
        """
        super().__init__()
        self.states = self.nodes
        self.transitions = self.edges

        self.round = 1
        self.initialize_model()
        self.pos = nx.spring_layout(self, iterations=500)
        
    def get_cards(self):
        """Get the cards currently held by the player.

        Returns:
        list: The list of cards held by the player.
        """
        return self.cards

    def add_state(self, state):
        """Add a new possible state to the Kripke model.

        Args:
        state (str): The state to add.
        """
        self.add_node(state)

    def remove_state(self, state):
        """Remove a state from the Kripke model.

        Args:
        state (str): The state to remove.
        """
        self.remove_node(state)

    def add_transition(self, start_state, end_state, player):
        """Add a transition between two states for a given player.

        Args:
        start_state (str): The starting state.
        end_state (str): The ending state.
        player (int): The player number.
        """
        self.add_edge(start_state, end_state, player=player)

    def remove_transition(self, start_state, end_state, player):
        """Remove a transition between two states for a given player.

        Args:
        start_state (str): The starting state.
        end_state (str): The ending state.
        player (int): The player number.
        """
        self.remove_edge(start_state, end_state, player=player)

    def initialize_model(self):
        """
        Initialize the model with all possible states and transitions at the start of the game.
        This takes into account that A8 is the same as 8A, reducing the number of states.
        """
        player_one_transitions = [(1, 8), (1, 16), (8, 16), (7, 15), (2, 10), (10, 18), (2, 18), (5, 13), (4, 12),
                                  (12, 19), (4, 19), (9, 17), (3, 11)]
        player_two_transitions = [(1, 3), (1, 6), (3, 6), (7, 10), (10, 13), (7, 13), (14, 19), (14, 17), (17, 19),
                                  (9, 12), (18, 15), (2, 5), (8, 11)]
        player_three_transitions = [(4, 5), (5, 6), (4, 6), (9, 10), (9, 11), (10, 11), (14, 15), (15, 16), (14, 16),
                                    (2, 3), (12, 13), (7, 8), (17, 18)]

        for state in all_states:
            self.add_state(state)

        players_transitions = [player_one_transitions, player_two_transitions, player_three_transitions]
        for player, transition in zip(range(1, 4), players_transitions):
            for start, end in transition:
                self.add_transition(all_states[start - 1], all_states[end - 1], player)

    def update_dont_know(self):
        """
        If no one knows, remove all states that are not reachable by everyone: then that would have been the 
        actual state (and someone would have known).
        """
        players = set(range(1, 4))
        total_reachable_states = set(self.states())

        # Determine states reachable for each player and take the intersection
        # in order to find the states reachable by all players.
        for player in players:
            reachable_states = set()
            for state in self.states():
                if any(self[state][neighbor].get('player') == player for neighbor in self.neighbors(state)):
                    reachable_states.add(state)

            total_reachable_states = total_reachable_states.intersection(reachable_states)

        # Remove all states that are not reachable by all players.
        states_to_remove = set(self.states()) - total_reachable_states

        for state in states_to_remove:
            self.remove_state(state)

    def display_graph(self):
        """
        Display the Kripke model graph using networkx and matplotlib.
        """
        view_graph = copy.deepcopy(self)

        fig, ax = plt.subplots(figsize=(14, 10))
        nx.draw(view_graph, self.pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, ax=ax)
        edge_labels = nx.get_edge_attributes(view_graph, 'player')
        nx.draw_networkx_edge_labels(view_graph, self.pos, edge_labels=edge_labels)

        plt.savefig(f"visualization/round_{self.round}.png", bbox_inches='tight', format='png')
        self.round += 1

        # plt.show() # Uncomment to show the graph in a window
        plt.clf()
