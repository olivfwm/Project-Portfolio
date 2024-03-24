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
            for y in range(state.h):
                if(state.board[x][y] == EMPTY_PIECE):
                    count +=1
        start_time = time.time()
        if(time_limit != None): 
            move, e = self.minimax(state, count, start_time+time_limit)
        else: move, e = self.minimax(state, count, start_time+5.0)
        #board = [['O', 'X', 'X'],[' ', 'O', 'X'],[' ', 'O', 'O']]
        #e = self.static_eval(state, board)
        return move

    def minimax(self, state: game.GameState, depth_remaining: int, time_limit: float = None,
                alpha: float = None, beta: float = None, z_hashing=None) -> ((int, int), float):
        start_time = time.time()
        if(time_limit != None):
            move, e = self.minimax2(state, (0,0), depth_remaining, time_limit)
        else: move, e = self.minimax2(state, (0,0), depth_remaining, start_time+5.0)
        return move, e

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

        moves = []
        for x in range(state.w):
            for y in range(state.h):
                move = (x,y)
                if state.is_valid_move(move):
                    moves.append(move)
                    
        if state.next_player == X_PIECE:
            best_eval = float('-inf')
            # Maximize
            for move in moves:
                nstate = state.make_move(move)
                if(nstate.winner() == 'draw'):
                    e = self.static_eval(nstate)
                else:
                    #e = self.static_eval(nstate)
                    d = depth_remaining
                    if d >= 1:
                        d = 0
                    m, e = self.minimax2(nstate, best_move, d, time_limit, alpha, beta, z_hashing)
                #print(move, e)
                if e > best_eval:
                    best_eval = e
                    best_move = move
            return best_move, best_eval
        else:
            # Minimize
            best_eval = float('inf')
            for move in moves:
                nstate = state.make_move(move)
                if(nstate.winner() == 'draw'):
                    e = self.static_eval(nstate)
                else:
                    #e = self.static_eval(nstate)
                    d = depth_remaining
                    if d >= 1:
                        d = 0
                    m, e = self.minimax2(nstate, best_move, d, time_limit, alpha, beta, z_hashing)
                #print(move, e)
                if e < best_eval:
                    best_eval = e
                    best_move = move
            return best_move, best_eval

    def static_eval(self, state: game.GameState) -> float:
        """
        Evaluates the given state. States good for X should be larger that states good for O.
        :param state: state to evaluate
        :return: evaluation of the state
        """

        eval_x = self.count_sequences(state, X_PIECE)
        eval_o = (-2)*self.count_sequences(state, O_PIECE)
            
        # Return the total evaluation
        return eval_x + eval_o

    def count_sequences(self, state: game.GameState, piece):
        board = state.board
        e = 0

        #count rows
        for i in range(state.w):
            if piece not in board[i]:
                continue
            
            count = 0
            p_count = 0
            nconn = False
            for j in range(state.h):
                space = board[i][j]
                #print('current', space)
                if(space == piece or space == EMPTY_PIECE):
                    if(space == piece):
                        p_count+=1
                    else:
                        if p_count > 0:
                            nconn = True
                    count+=1
                else: 
                    if count >= state.k and p_count > 0:
                        e += 10**(p_count-1)
                        if nconn:
                            e -= 1
                    #print("Here", e)
                    count = 0
                    p_count = 0
                    nconn = False
                    continue
                if count >= state.k and p_count > 0:
                        e += 10**(p_count-1)
                        if nconn:
                            e -= 1
                #print("RowHere", e)
                #print('count', count)
                #print('pcount', p_count) 
                    

        #count columns
        for j in range(state.h):
            
            count = 0
            p_count = 0
            nconn = False
            for i in range(state.w):
                space = board[i][j]
                if(space == piece or space == EMPTY_PIECE):
                    if(space == piece):
                        p_count+=1
                    else:
                        if p_count > 0:
                            nconn = True
                    count +=1
                else: 
                    if count >= state.k and p_count > 0:
                        e += 10**(p_count-1)
                        if nconn:
                            e -= 1

                    count = 0
                    p_count = 0
                    nconn = False
                    continue
                
                if count >= state.k and p_count > 0:
                        e += 10**(p_count-1)
                        if nconn:
                            e -= 1
                #print("CHere", e)
                #print('count', count)
                #print('pcount', p_count)

        for i in range(state.w):
            count = 0
            p_count = 0
            nconn = False
            if state.w - i < state.k:
                break
            for j in range(min(state.w - i, state.h)):
                #print(i+j, j, "Dhere", e)
                space = board[i + j][j]
                if space == piece or space == EMPTY_PIECE:
                    if space == piece:
                        p_count += 1
                    else:
                        if p_count > 0:
                            nconn = True
                    count += 1
                else:
                    if count >= state.k and p_count > 0:
                        e += 10 ** (p_count - 1)
                        if nconn:
                            e -= 1
                    count = 0
                    p_count = 0
                    nconn = False
                    continue
                
                if count >= state.k and p_count > 0:
                        e += 10**(p_count-1)
                        if nconn:
                            e -= 1

    
        for j in range(1, state.h):
            count = 0
            p_count = 0
            nconn = False
            if state.h - j < state.k:
                break
            for i in range(min(state.w, state.h-j)):
                #print(i, j+i, "Dhere", e)
                space = board[i][j + i]
                if space == piece or space == EMPTY_PIECE:
                    if space == piece:
                        p_count += 1
                    else:
                        if p_count > 0:
                            nconn = True
                    count += 1
                else:
                    if count >= state.k and p_count > 0:
                        e += 10 ** (p_count - 1)
                        if nconn:
                            e -= 1
                    count = 0
                    p_count = 0
                    nconn = False
                    continue
                
                if count >= state.k and p_count > 0:
                        e += 10**(p_count-1)
                        if nconn:
                            e -= 1

        for j in range(state.h-1, -1, -1):
            count = 0
            p_count = 0
            nconn = False
            if j+1 < state.k:
                break
            for i in range(min(state.w, j+1)):
                #print(i+j, state.w - 1 - j, "Dhere", e)
                space = board[i][j-i]
                if space == piece or space == EMPTY_PIECE:
                    if space == piece:
                        p_count += 1
                    else:
                        if p_count > 0:
                            nconn = True
                    count += 1
                else:
                    if count >= state.k and p_count > 0:
                        e += 10 ** (p_count - 1)
                        if nconn:
                            e -= 1
                    count = 0
                    p_count = 0
                    nconn = False
                    continue
                
                if count >= state.k and p_count > 0:
                        e += 10**(p_count-1)
                        if nconn:
                            e -= 1

    # Count diagonals starting from top-right corner going left
        for i in range(1, state.w):
            count = 0
            p_count = 0
            nconn = False
            if state.w - i < state.k:
                break
            for j in range(min(state.h, state.w - i)):
                space = board[i+j][state.h- j - i]
                if space == piece or space == EMPTY_PIECE:
                    if space == piece:
                        p_count += 1
                    else:
                        if p_count > 0:
                            nconn = True
                    count += 1
                else:
                    if count >= state.k and p_count > 0:
                        e += 10 ** (p_count - 1)
                        if nconn:
                            e -= 1
                    count = 0
                    p_count = 0
                    nconn = False
                    continue
                
                if count >= state.k and p_count > 0:
                        e += 10**(p_count-1)
                        if nconn:
                            e -= 1
                            
        return e

