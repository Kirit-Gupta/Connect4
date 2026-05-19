from .Cell import Cell

class Board:
    def __init__(self):
        self.rows = 6
        self.column = 7
        self.reset_board()
    
    def reset_board(self):
        self.board = []     #[row, col]
        for i in range(self.rows):
            a = []
            for j in range(self.column):
                cell = Cell()
                a.append(cell)
            self.board.append(a)
    
    def get_rows(self):
        return self.rows
    
    def get_col(self):
        return self.column

    def add_counter(self, color, column, type=1, gameover=0):
        found = False
        if not gameover:
            for row in range(self.rows):
                if not found:
                    cell = self.board[row][column]
                    if cell.is_empty():
                        found = True
                        if type:
                            cell.add_counter(color)
                        else:
                            return row, column, None
        return None, None, found
        
    
    def board_full(self):
        return not (any(self.get_valid_moves()))
    
    def get_valid_moves(self):
        valid_columns = []

        for col in range(self.column):
            found = False
            for row in range(self.rows):
                if self.board[row][col].is_empty():
                    found = True
            valid_columns.append(found)

        return valid_columns

    def check_four_horizontal(self):
        for row in range((self.rows)):
            for col in range(self.column - 3):
                ls = []
                for i in range(4):
                    cell = self.board[row][col + i]
                    ls.append(cell.get_color())

                if not(None in ls):
                    if len(set(ls)) == 1:
                        return ls[0]
    
    def check_four_vertical(self):
        for col in range(self.column):
            for row in range(self.rows - 3):
                ls = []
                for i in range(4):
                    cell = self.board[row + i][col]
                    ls.append(cell.get_color())
                
                if not(None in ls):
                    if len(set(ls)) == 1:
                        return ls[0]

    def check_positive_diagonal(self):
        for row in range(self.rows - 3):
            for col in range(self.column - 3):
                ls = []
                for i in range(4):
                    cell = self.board[-(row+i)-1][col+i]
                    ls.append(cell.get_color())
                
                if not(None in ls):
                    if len(set(ls)) == 1:
                        return ls[0]
    
    def check_negative_diagonal(self):
        for row in range(self.rows - 3):
            for col in range(self.column - 3):
                ls = []
                for i in range(4):
                    cell = self.board[row + i][col + i]
                    ls.append(cell.get_color())
                
                if not(None in ls):
                    if len(set(ls)) == 1:
                        return ls[0]
    
    def check_win(self):
        win = []
        win.append(self.check_positive_diagonal())
        win.append(self.check_negative_diagonal())
        win.append(self.check_four_horizontal())
        win.append(self.check_four_vertical())
        win = [x for x in win if x is not None]
        if len(set(win)) == 1:
            return win[0]
        elif self.board_full():
            return 'No'
    
    def get(self, row, col):
        return self.board[row][col]