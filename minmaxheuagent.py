from connect4 import Connect4
from exceptions import AgentException


class MinMaxHeuAgent:
    def __init__(self, my_token='o', depth=4):
        self.my_token = my_token
        self.depth = depth
        self.enemy_token = 'x' if my_token == 'o' else 'o'

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        return self.minmax_decision(connect4, self.depth)

    def minmax_decision(self, connect4, depth):
        scores = []
        for move in connect4.possible_drops():
            new_board = Connect4(width=connect4.width, height=connect4.height)
            new_board.board = [row.copy() for row in connect4.board]
            new_board.who_moves = connect4.who_moves
            new_board.drop_token(move)
            score = self.minimax(new_board, depth - 1, False)
            scores.append((move, score))

        best_move = max(scores, key=lambda x: x[1])[0]
        return best_move

    def minimax(self, board, depth, is_max):
        if depth == 0 or board.game_over:
            return self.evaluate(board)

        if is_max:
            best_value = float('-inf')
            for move in board.possible_drops():
                new_board = Connect4(width=board.width, height=board.height)
                new_board.board = [row.copy() for row in board.board]
                new_board.who_moves = board.who_moves
                new_board.drop_token(move)
                value = self.minimax(new_board, depth - 1, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for move in board.possible_drops():
                new_board = Connect4(width=board.width, height=board.height)
                new_board.board = [row.copy() for row in board.board]
                new_board.who_moves = board.who_moves
                new_board.drop_token(move)
                value = self.minimax(new_board, depth - 1, True)
                best_value = min(best_value, value)
            return best_value

    def evaluate(self, board):
        if board.wins == self.my_token:
            return 1000
        if board.wins == self.enemy_token:
            return -1000
        score_heu = 0
        for i in range(0, board.height-1):
            if board.board[i][board.width//2] == self.my_token:
                score_heu += 50
            if board.board[i][board.width//2] == self.enemy_token:
                score_heu -= 5
        return score_heu