import numpy as np
import abc
from itertools import product
import util
from game import Agent, Action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)
        if action == Action.DOWN:
            return 0
        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score
        return consistent_board_rows_and_cols_num(current_game_state) + number_of_empty_tiles(current_game_state)


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        minimax_eval = lambda action: self.minimax_core(game_state.generate_successor(0, action), self.depth, 1)
        return max(game_state.get_legal_actions(0), key=minimax_eval)

    def minimax_core(self, state, depth, agent_index):
        actions = state.get_opponent_legal_actions() if agent_index else state.get_agent_legal_actions()
        if depth == 0 or not actions:
            return self.evaluation_function(state)
        f, new_depth = (min, depth - 1) if agent_index else (max, depth)
        return f(
            [self.minimax_core(state.generate_successor(agent_index, action), new_depth, 1 - agent_index) for action in
             actions])


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        alphabeta_eval = lambda action: self.alpha_beta_core(game_state.generate_successor(0, action), self.depth,
                                                             float('-inf'), float('inf'), 1)
        return max(game_state.get_legal_actions(0), key=alphabeta_eval)

    def alpha_beta_core(self, state, depth, a, b, agent_index):
        if depth == 0:
            return self.evaluation_function(state)
        actions = state.get_opponent_legal_actions() if agent_index else state.get_agent_legal_actions()
        if agent_index == 0:
            v = float('-inf')
            for action in actions:
                v = max(v, self.alpha_beta_core(state.generate_successor(agent_index, action), depth, a, b,
                                                1 - agent_index))
                if v >= b:
                    break
                a = max(a, v)
            return v
        else:
            v = float('inf')
            for action in actions:
                v = min(v, self.alpha_beta_core(state.generate_successor(agent_index, action), depth - 1, a, b,
                                                1 - agent_index))
                if v <= a:
                    break
                b = min(b, v)
            return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        util.raiseNotDefined()

    def expectimax_core(self, state, depth, agent_index):
        actions = state.get_opponent_legal_actions() if agent_index else state.get_agent_legal_actions()
        if depth == 0 or not actions:
            return self.evaluation_function(state)




def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    a = 1 / current_game_state.max_tile
    b = 2
    c = 1
    return -a * smoothness(current_game_state) + b * consistent_board_rows_and_cols_num(
        current_game_state) + c * number_of_empty_tiles(current_game_state)


def smoothness(current_game_state):
    state_score = 0
    for row, col in product(range(current_game_state.board.shape[0]), range(current_game_state.board.shape[1])):
        if current_game_state.board[row, col] == 0:
            continue

        if row + 1 < current_game_state.board.shape[0]:
            if current_game_state.board[row + 1, col] != 0:
                state_score += abs(current_game_state.board[row, col] - current_game_state.board[row + 1, col])

        if col + 1 < current_game_state.board.shape[1]:
            if current_game_state.board[row, col + 1] != 0:
                state_score += abs(current_game_state.board[row, col] - current_game_state.board[row, col + 1])

    return state_score


def consistent_board_rows_and_cols_num(current_game_state):
    board = current_game_state.board
    return number_of_monotonic_rows(board) + number_of_monotonic_rows(board.T)


def number_of_monotonic_rows(board):
    left_mon = np.count_nonzero(np.all(board[:, 1:] >= board[:, :-1], axis=1))  # [<,<,<,<]
    right_mon = np.count_nonzero(np.all(board[:, 1:] <= board[:, :-1], axis=1))  # [>,>,>,>]
    return max(left_mon, right_mon)


def number_of_empty_tiles(current_game_state):
    board = current_game_state.board
    return np.count_nonzero(board == 0)


# Abbreviation
better = better_evaluation_function
