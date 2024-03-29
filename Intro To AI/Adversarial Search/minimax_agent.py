"""
minimax_agent.py
author: Olivia Fang
"""
import agent
import game
import time

X_PIECE = 'X'
O_PIECE = 'O'
BLOCK_PIECE = '-'
EMPTY_PIECE = ' '

class MinimaxAgent(agent.Agent):
    def __init__(self, initial_state: game.GameState, piece: str):
        super().__init__(initial_state, piece)

    def introduce(self):
        """
        returns a multi-line introduction string
        :return: intro string
        """
        return "This is my agent Bob playing the game. \n My net id is olivfwm"

    def nickname(self):
        """
        returns a short nickname for the agent
        :return: nickname
        """
        return "Bob"

    def choose_move(self, state: game.GameState, time_limit: float) -> (int, int):
        """
        Selects a move to make on the given game board. Returns a move
        :param state: current game state
        :param time_limit: time (in seconds) before you'll be cutoff and forfeit the game
        :return: move (x,y)
        """
        count = 0
        for x in range(state.w):
        # hidden to protect information

    def minimax(self, state: game.GameState, depth_remaining: int, time_limit: float = None,
                alpha: float = None, beta: float = None, z_hashing=None) -> ((int, int), float):
        start_time = time.time()
        # hidden to protect information

    def minimax2(self, state: game.GameState, best_move: (), depth_remaining: int, time_limit: float = None,
                alpha: float = None, beta: float = None, z_hashing=None) -> ((int, int), float):
        """
        Uses minimax to evaluate the given state and choose the best action from this state. Uses the next_player of the
        given state to decide between min and max. Recursively calls itself to reach depth_remaining layers. Optionally
        uses alpha, beta for pruning, and/or z_hashing for zobrist hashing.
        :param state: State to evaluate
        :param depth_remaining: number of layers left to evaluate
        :param time_limit: argument for your use to make sure you return before the time limit. None means no time limit
        :param alpha: alpha value for pruning
        :param beta: beta value for pruning
        :param z_hashing: zobrist hashing data
        :return: move (x,y) or None, state evaluation
        """
        #if(time_limit == None):  
        #    if depth_remaining <= 0:
        #        return best_move, self.static_eval(state)
        #else:
        if depth_remaining <= 0 or time_limit - time.time() <= 0.3:
            return best_move, self.static_eval(state)

        # hidden to protect information

    def static_eval(self, state: game.GameState) -> float:
        """
        Evaluates the given state. States good for X should be larger that states good for O.
        :param state: state to evaluate
        :return: evaluation of the state
        """

        eval_x = self.count_sequences(state, X_PIECE)
        eval_o = (-2)*self.count_sequences(state, O_PIECE)
            
        # Return the total evaluation

    def count_sequences(self, state: game.GameState, piece):
        board = state.board
        e = 0

        #count rows
        for i in range(state.w):
        # hidden to protect information

