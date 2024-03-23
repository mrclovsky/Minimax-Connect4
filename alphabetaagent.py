from connect4 import Connect4
from minmaxagent import MinMaxAgent
from exceptions import AgentException


class AlphaBetaAgent(MinMaxAgent):
    def __init__(self, my_token='o', depth=4):
        super().__init__(my_token=my_token, depth=depth)

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        return self.alphabeta_decision(connect4, self.depth)

    def alphabeta_decision(self, connect4, depth):
        scores = []
        alpha = float('-inf')
        beta = float('inf')
        for move in connect4.possible_drops():
            new_board = Connect4(width=connect4.width, height=connect4.height)
            new_board.board = [row.copy() for row in connect4.board]
            new_board.who_moves = connect4.who_moves
            new_board.drop_token(move)
            score = self.alphabeta(new_board, depth - 1, alpha, beta, False)
            alpha = max(alpha, score)
            scores.append((move, score))

        best_move = max(scores, key=lambda x: x[1])[0]
        return best_move

    def alphabeta(self, board, depth, alpha, beta, is_max):
        if depth == 0 or board.game_over:
            return self.evaluate(board)
        if is_max:
            best_value = float('-inf')
            for move in board.possible_drops():
                new_board = Connect4(width=board.width, height=board.height)
                new_board.board = [row.copy() for row in board.board]
                new_board.who_moves = board.who_moves
                new_board.drop_token(move)
                value = self.alphabeta(new_board, depth - 1, alpha, beta, False)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
            return best_value
        else:
            best_value = float('inf')
            for move in board.possible_drops():
                new_board = Connect4(width=board.width, height=board.height)
                new_board.board = [row.copy() for row in board.board]
                new_board.who_moves = board.who_moves
                new_board.drop_token(move)
                value = self.alphabeta(new_board, depth - 1, alpha, beta, True)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if alpha >= beta:
                    break
            return best_value
