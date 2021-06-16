import chess
import random
import time
import copy
from strategies import MinimalEngine
from engine_wrapper import EngineWrapper
import logging
import math

logger = logging.getLogger(__name__)
logging.error("here1")
print("printing here")
class Node:
    def __init__(self, m, p): # move is from parent to node
        self.move, self.parent, self.children = m, p, []
        self.wins, self.visits  = 0, 0

    def expand_node(self, board):
        logging.error("in expand_node")
        if not board.is_game_over():
          for m in list(board.legal_moves):
            nc = Node(m, self) # new child node
            self.children.append(nc)

    def update(self, result):
        logging.error("in update")
        self.visits += 1
        if result.is_variant_loss():
            self.wins += 0
        if result.is_variant_win():
            self.wins += 1
        if result.is_variant_draw():
            self.wins += .5

    def is_leaf(self):
        logging.error("in is_leaf")
        return len(self.children)==0

    def has_parent(self):
        logging.error("in has_parent")
        return self.parent is not None


class GoldEngine(MinimalEngine):
    """

    """
    def mcts(self, board, start_time):
        logging.error("in mcts")
        root_node = Node(None, None)
        while self.time_remaining(start_time):
            logging.error("time to calc")
            n, b = root_node, copy.deepcopy(board)
            while not n.is_leaf():    # select leaf
                n = self.tree_policy_child(n)
                b.push(n.move)
            n.expand_node(b)          # expand
            n = self.tree_policy_child(n)
            while not b.is_game_over():    # simulate
                b = self.simulation_policy_child(b)
            result = b
            while n.has_parent():     # propagate
                n.update(result)
                n = n.parent

        logging.error("+++ Process Free. Children: {}.".format(root_node.children))
        return self.best_move(root_node)

    # determines which node to visit with explore factor
    def tree_policy_child(self, n):
        logging.error("in tree_policy_child")
        best_explore_bonus = 0
        best_to_visit_node = Node(None, None)
        for child in n.children:
            logging.error("in tree_policy_child looking through children")
            explore_bonus = child.wins / child.visits + (math.sqrt(2) * math.sqrt(math.log(child.parent.visits) / child.visits)) if (child.visits > 0 and child.parent.visits > 0) else 100
            logging.error("explore_bonus: {}".format(explore_bonus))
            if (explore_bonus > best_explore_bonus):
                best_explore_bonus = explore_bonus
                best_to_visit_node = child

        logging.error("best_to_visit_node: {}".format(best_to_visit_node))
        return best_to_visit_node

    """
    Determines if there is more time available for the bot to calculate next best move

    Attributes:
        start time (float): when turn started

    Return:
        hasTime (boolean): is there still time to run best move calculation
    """
    def time_remaining(self, start_time):
        logging.error("in time_remaining")
        #challenge = config["challenge"]
        # board.time controls
        return time.time() - start_time < 5

    def simulation_policy_child(self, b):
        logging.error("in simulation_policy_child")
        b.push(random.choice(list(b.legal_moves)))
        return b

    def best_move(self, root_node):
        logging.error("in best_move")
        most_visits = 0
        best_move = chess.Move.from_uci("g1f3")
        for node in root_node.children:
            logging.error("in best_move looking through children")
            if node.visits > most_visits:
                most_visits = node.visits
                best_move = node.move
        return best_move

    def search(self, board, *args):
        logging.error("in search")
        start_time = time.time()
        return self.mcts(board, start_time)
