import chess
import random
import time
from strategies import MinimalEngine
from engine_wrapper import EngineWrapper

class Node:
    def __init__(self, m, p): # move is from parent to node
        self.move, self.parent, self.children = m, p, []
        self.wins, self.visits  = 0, 0

    def expand_node(self, board):
        if not board.is_game_over():
          for m in list(board.legal_moves):
            nc = Node(m, self) # new child node
            self.children.append(nc)

    def update(self, result):
        self.visits += 1
        if result.is_variant_loss():
            self.wins += 0
        if result.is_variant_win():
            self.wins += 1
        if result.is_variant_draw():
            self.wins += .5

      def is_leaf(self):
          return len(self.children)==0

      def has_parent(self):
        return self.parent is not None


class GoldEngine(MinimalEngine):
    """

    """
    def mcts(board, start_time):
        root_node = Node(None, None)
        while time_remaining(start_time):
            n, b = root_node, copy.deepcopy(board)
            while not n.is_leaf():    # select leaf
                n = tree_policy_child(n)
                b.push(n.move)
            n.expand_node(b)          # expand
            n = tree_policy_child(n)
            while not b.is_game_over():    # simulate
                b = simulation_policy_child(b)
            result = b
            while n.has_parent():     # propagate
                n.update(result)
                n = n.parent

        return best_move(root_node)

    # determines which node to visit with explore factor
    def tree_policy_child(n):
        best_explore_bonus = 0
        best_to_visit_node = Node(None, None)
        for child in node:
            explore_bonus = child.wins / child.visits + (sqrt(2) * sqrt(math.log(child.parent.visits) / child.visits))
            if (explore_bonus > best_explore_bonus):
                best_explore_bonus = explore_bonus
                best_to_visit_node = child

        return best_to_visit_node

    """
    Determines if there is more time available for the bot to calculate next best move

    Attributes:
        start time (float): when turn started

    Return:
        hasTime (boolean): is there still time to run best move calculation
    """
    def time_remaining(start_time):
        #challenge = config["challenge"]
        # board.time controls
        return time.time() - start_time > 5

    def simulation_policy_child(b):
        b.push(random.choice(list(board.legal_moves)))
        return b

    def best_move(root_node):
        most_visits = 0
        best_move = chess.Move.from_uci("g1f3")
        for node in root_node.children:
            if node.visits > most_visits:
                most_visits = node.visits
                best_move = node.move

    def search(self, board, *args):
        start_time = time.time()
        return mcts(board, start_time)
