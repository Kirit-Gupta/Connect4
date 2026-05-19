from copy import deepcopy
from .constants import RED, YELLOW

class MiniMax:
    def __init__(self, depth, col):
        self.depth = depth
        self.ai_color = col
        if self.ai_color == RED:
            self.human_col = YELLOW
        else:
            self.human_col = RED
    
    def get_best_move(self, board):
        _, best_col = self.minimax(board, self.depth, float('-inf'), float('inf'), True)
        return best_col
        
    def minimax(self, board, depth, alpha, beta, max_player):
        winner = board.check_win()
        if winner == self.ai_color:
            return 1000000 + depth, None
        elif winner == self.human_col:
            return -1000000 - depth, None
        elif winner == 'No' or depth == 0:
            return self.evaluate(board), None
        
        valid_cols = [c for c, ok in enumerate(board.get_valid_moves()) if ok]

        if not valid_cols:
            return self.evaluate(board), None

        if max_player:
            max_eval = float('-inf')
            best_col = valid_cols[0]
            for col in valid_cols:
                child = self.simulate(board, col, self.ai_color)
                score, _ = self.minimax(child, depth - 1, alpha, beta, False)
                if score > max_eval:
                    max_eval = score
                    best_col = col
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break
            return max_eval, best_col
        
        else:
            min_eval = float('inf')
            best_col = valid_cols[0]
            for col in valid_cols:
                child = self.simulate(board, col, self.human_col)
                score, _ = self.minimax(child, depth - 1, alpha, beta, True)
                if score < min_eval:
                    min_eval = score
                    best_col = col
                beta = min(beta, min_eval)
                if alpha >= beta:
                    break
            return min_eval, best_col
    
    def simulate(self, board, col, color):
        temp = deepcopy(board)
        temp.add_counter(color, col)
        return temp
    
    def evaluate(self, board):
        score = 0
        rows = board.get_rows()
        cols = board.get_col()
        
        centre = cols // 2
        for row in range(rows):
            cell = board.get(row, centre)
            color = cell.get_color()

            if color == self.ai_color:
                score +=4
            elif color == self.human_col:
                score-=4

        for window in self.get_all_windows(board):
            score += self.score_window(window)
        
        return score
    
    def score_window(self, window):
        ai_count = window.count(self.ai_color)
        opp_count = window.count(self.human_col)
        empty_count = window.count(None)
        score = 0

        if ai_count == 4:
            score += 100
        elif ai_count == 3 and empty_count == 1:
            score += 10
        elif ai_count == 2 and empty_count == 2:
            score += 3
        
        if opp_count == 3 and empty_count == 1:
            score -=8

        return score
    
    def get_all_windows(self, board):
        rows = board.get_rows()
        cols = board.get_col()
        windows = []

        def color(r, c):
            return board.get(r, c).get_color()
        
        for r in range(rows):
            for c in range(cols - 3):
                windows.append([color(r, c + i) for i in range(4)])

        for c in range(cols):
            for r in range(rows - 3):
                windows.append([color(r + i, c) for i in range(4)])

        for r in range(rows - 3):
            for c in range(cols - 3):
                windows.append([color(-(r + i) - 1, c + i) for i in range(4)])

        for r in range(rows - 3):
            for c in range(cols - 3):
                windows.append([color(r + i, c + i) for i in range(4)])

        return windows