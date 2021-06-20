import chess
import random
import time
import copy
from strategies import MinimalEngine
from engine_wrapper import EngineWrapper
import logging
import math
import chess.pgn

logger = logging.getLogger(__name__)

class Node:
    """
    A Node represents a chess state for the monte-carlo tree search data structure.
    """

    def __init__(self, m, p, b): # move is from parent to node
    """ Initialises a node for the monte-carlo tree search tree.

    Attributes:
        self (Node): The current node
        m (chess.move): Represents the move to get to this node from the parent node
        p (Node): The parent node
        b (chess.board): The game state of the board

    Return:

    """
        self.move, self.parent, self.children = m, p, []
        self.wins, self.visits  = 0, 0
        self.board = b

    def expand_node(self):
        """ Expands tree by a single child of the selected node not yet expanded

        Attributes:
            self (Node): The current node to expand

        Return:
            nc (Node): The new child node
        """

        moves_added = []
        for child in self.children:
            moves_added.append(child.move)

        if not self.board.is_game_over():
          for m in list(self.board.legal_moves):
            b = copy.deepcopy(self.board)
            b.push(m)
            nc = Node(m, self, b)
            if m not in moves_added:
                self.children.append(nc)
                return nc

    def update(self, result, engine):
        """ Performs back propogation through the monte-carlo tree search
            data structure to update win/loss ratios.

        Attributes:
            self (Node): The current node
            result (chess.board): The final board state
            engine (GoldEngine): The engine to evaluate the final board

        Return:

        """

        self.visits += 1
        outcome = result.outcome()
        if outcome == None:
            self.wins += .5 + engine.eval(result)
        elif outcome.winner == True:
            self.wins += 1
        elif outcome.winner == False:
            x = 1
        else:
            self.wins += .5

    def is_leaf(self):
        """ Checks whether the current node is a leaf

        Attributes:
            self (Node): The current node

        Return:
            (Boolean): If the node is a leaf
        """

        return len(self.children) < len(list(self.board.legal_moves))

    def has_parent(self):
        """ Checks whether the current node has a parent

        Attributes:
            self (Node): The current node

        Return:
            (Boolean): If the node has a parent
        """
        return self.parent is not None


class GoldEngine(MinimalEngine):
    """
    Our chess engine that runs using monte-carlo tree search
    """

    def mcts(self, board, start_time, time_limit):
        """ The monte-carlo tree search method.
        With the four phases: selection, expansion, simulation and backpropagation

        Attributes:
            self (GoldEngine): An instance of a GoldEngine
            board (chess.board): The game state of a board
            start_time (float): The start time of the game
            time_limit (Limit/int): The time_limit to make the next move

        Return:
            (chess.move): Gets the best move possible according to our
                            monte-carlo tree search method
        """

        root_node = Node(None, None, copy.deepcopy(board))
        leaf_nodes = [root_node]
        while self.time_remaining(start_time, time_limit):

            n, leaf_nodes = self.tree_policy_child(leaf_nodes)  # selection
            n = n.expand_node()                                 # expansion
            b = copy.deepcopy(n.board)
            leaf_nodes.append(n)
            move_count = 0

            while not b.is_game_over() and move_count < 10:     # simulation
                b = self.simulation_policy_child(b)
                move_count += 1
            result = b

            while n.has_parent():                               # backpropagation
                n.update(result, self)
                n = n.parent

        return self.best_move(root_node)

    def tree_policy_child(self, leaf_nodes):
        """ determines which node to visit with explore factor

        Attributes:
            self (GoldEngine): An instance of a GoldEngine
            leaf_nodes (list): A list of all possible nodes that can be explored next.

        Return:
            best_to_visit_node (Node): The node that we want to perform expansion on.
            leaf_nodes (list): Updated list of all possible nodes that can be explored next.
        """

        best_explore_bonus = 0
        best_to_visit_node = Node(None, None, None)

        for child in leaf_nodes:
            explore_bonus = child.wins / child.visits + (math.sqrt(2) * math.sqrt(math.log(child.parent.visits) / child.visits)) if (child.visits > 0 and child.parent.visits > 0) else 100

            if (explore_bonus > best_explore_bonus and child.is_leaf()):
                best_explore_bonus = explore_bonus
                best_to_visit_node = child

        return best_to_visit_node, leaf_nodes


    def time_remaining(self, start_time, time_limit):
        """ Determines if there is more time available for the bot to calculate next best move

        Attributes:
            self (GoldEngine): An instance of the GoldEngine
            start_time (float): when turn started
            time_limit (Limit/int): The time_limit to make the next move

        Return:
            (boolean): is there still time to run best move calculation
        """

        if (isinstance(time_limit, int)):
            return time.time() - start_time < (time_limit / 10000)
        return time.time() - start_time < 10

    def eval(self, b):
        """ The evaluation function that uses the Carrera's standard values

        Attributes:
            self (GoldEngine): An instance of the GoldEngine
            b (chess.board): The game state of the current board

        Return:
            (float): Represents how well our side is playing
        """

        str_board = str(b)
        white_count = 0
        black_count = 0

        for c in str_board:
            if c == 'P':
                white_count += 1
            elif c == 'p':
                black_count += 1
            elif c == 'N':
                white_count += 3
            elif c == 'n':
                black_count += 3
            elif c == 'B':
                white_count += 3
            elif c == 'b':
                black_count += 3
            elif c == 'R':
                white_count += 5
            elif c == 'r':
                black_count += 5
            elif c == 'Q':
                white_count += 9
            elif c == 'q':
                black_count += 9

        return (white_count - black_count) / (white_count + black_count)  if b.turn == chess.WHITE else (black_count - white_count) / (white_count + black_count)

    def simulation_policy_child(self, b):
        """ A evaluation heuristic driven simulation of monte-carlo tree search

        Attributes:
            self (GoldEngine): An instance of the GoldEngine
            b (chess.board): The game state of the current board

        Return:
            b (chess.board): The board after playing out the simulation
        """

        best_move = None
        best_move_score = -100

        for move in list(b.legal_moves):
            temp_b = copy.deepcopy(b)
            temp_b.push(move)

            if (self.eval(temp_b) > best_move_score):
                best_move = move
                best_move_score = self.eval(temp_b)

        b.push(best_move)
        return b

    def best_move(self, root_node):
        """ Determines which node was visited most during the monte-carlo tree search

        Attributes:
            self (GoldEngine): An instance of the GoldEngine
            root_node (Node): The starting state calculated from

        Return:
            best_move (chess.move): The move that should be played based on the visitation
        """

        most_visits = 0
        best_move = chess.Move.from_uci("g1f3")
        logging.error("---------\n")

        for node in root_node.children:
            logging.error("Move: {}, Visit Count: {}, Win Ratio: {}".format(node.move, node.visits, node.wins / node.visits))

            if node.visits > most_visits:
                most_visits = node.visits
                best_move = node.move
        return best_move

    def search(self, board, time_limit, ponder):
        """ Searches for the best move to play given the board and the time to calculate

        Attributes:
            self (GoldEngine): An instance of the GoldEngine
            board (chess.board): The game state
            time_limit (Limit/int): The time_limit to make the next move
            ponder (chess.move): the response that the engine expects after a move

        Return:
            (chess.move): A move after performing a monte-carlo tree search
        """

        start_time = time.time()
        return self.mcts(board, start_time, time_limit)
