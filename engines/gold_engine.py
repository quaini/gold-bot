import chess
import random
import time
import copy
from strategies import MinimalEngine
from engine_wrapper import EngineWrapper
import logging
import math

logger = logging.getLogger(__name__)
#logging.error("here1")
class Node:
    def __init__(self, m, p, b): # move is from parent to node
        self.move, self.parent, self.children = m, p, []
        self.wins, self.visits  = 0, 0
        self.board = b

    # expands tree by a single child of the selected node not yet expanded
    def expand_node(self):
        #logging.error("in expand_node")
        moves_added = []
        for child in self.children:
            moves_added.append(child.move)
        #logging.error("self.board: {}".format(self.board))
        if not self.board.is_game_over():
          for m in list(self.board.legal_moves):
            b = copy.deepcopy(self.board)
            b.push(m)
            #logging.error("b in expand_node: {}".format(b))
            nc = Node(m, self, b)
            if m not in moves_added:
                self.children.append(nc)
                #logging.error("found new child")
                return nc

    def update(self, result):
        #logging.error("in update")
        self.visits += 1
        outcome = result.outcome().winner
        if outcome == None:
            self.wins += .5
        elif outcome == True:
            self.wins += 1
        elif outcome == False:
            x = 1

        #else:
        # CALCULATE BOARD STATE

    def is_leaf(self):
        #logging.error("in is_leaf")
        return len(self.children) < len(list(self.board.legal_moves))

    def has_parent(self):
        #logging.error("in has_parent")
        return self.parent is not None


class GoldEngine(MinimalEngine):
    """

    """
    def mcts(self, board, start_time):
        logging.error("in mcts")
        root_node = Node(None, None, copy.deepcopy(board))
        leaf_nodes = [root_node]
        while self.time_remaining(start_time):
            #logging.error("time to calc")
            n, leaf_nodes = self.tree_policy_child(leaf_nodes)  # selection
            n = n.expand_node()                                 # expansion
            #logging.error("n.board: {}".format(n.board))
            b = copy.deepcopy(n.board)
            leaf_nodes.append(n)
            #logging.error("b: {}".format(b))
            while not b.is_game_over():                         # simulation
                b = self.simulation_policy_child(b)
            result = b
            while n.has_parent():                               # backpropagation
                n.update(result)
                n = n.parent

        #logging.error("+++ Process Free. Children: {}.".format(root_node.children))
        return self.best_move(root_node)

    # determines which node to visit with explore factor
    def tree_policy_child(self, leaf_nodes):
        #logging.error("in tree_policy_child")
        best_explore_bonus = 0
        best_to_visit_node = Node(None, None, None)

        for child in leaf_nodes:
            #logging.error("in tree_policy_child looking through children")
            explore_bonus = child.wins / child.visits + (math.sqrt(2) * math.sqrt(math.log(child.parent.visits) / child.visits)) if (child.visits > 0 and child.parent.visits > 0) else 100
            #logging.error("move: {}, explore_bonus: {}, board: {}".format(child.move, explore_bonus, child.board))
            if (explore_bonus > best_explore_bonus and child.is_leaf()):
                best_explore_bonus = explore_bonus
                best_to_visit_node = child

        #logging.error("best_to_visit_node: {}, leaf_nodes: {}".format(best_to_visit_node.move, leaf_nodes))
        return best_to_visit_node, leaf_nodes

    """
    Determines if there is more time available for the bot to calculate next best move

    Attributes:
        start time (float): when turn started

    Return:
        hasTime (boolean): is there still time to run best move calculation
    """
    def time_remaining(self, start_time):
        #logging.error("in time_remaining")
        #challenge = config["challenge"]
        # board.time controls
        return time.time() - start_time < 30

    def simulation_policy_child(self, b):
        #logging.error("in simulation_policy_child")
        b.push(random.choice(list(b.legal_moves)))
        return b

    def best_move(self, root_node):
        #logging.error("in best_move")
        most_visits = 0
        best_move = chess.Move.from_uci("g1f3")
        logging.error("---------\n")
        for node in root_node.children:
            logging.error("Move: {}, Visit Count: {}, Win Ratio: {}".format(node.move, node.visits, node.wins / node.visits))
            if node.visits > most_visits:
                most_visits = node.visits
                best_move = node.move
        return best_move

    def search(self, board, *args):
        #logging.error("in search")
        start_time = time.time()
        return self.mcts(board, start_time)
