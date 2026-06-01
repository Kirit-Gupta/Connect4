from .Draw import Draw
from .Board import Board
from .Counter import Counter
from .MiniMax import MiniMax
from .constants import RED, YELLOW

import random
import threading

class Game:
    def __init__(self):
        self.game_over = False
        self.depth = 4
        self.turn = random.choice([RED, YELLOW])
        self.run = True
        self.winner = None
        self.ai_color = random.choice([RED, YELLOW])
        self.minimax = MiniMax(self.depth, self.ai_color)

        self.ai_thinking = False
        self.ai_move = None


        self.win_count = Counter()
        self.board = Board()
        self.draw = Draw(self.game_over)

    def run_minimax(self, board):
        self.ai_move = self.minimax.get_best_move(board)
        self.ai_thinking = False
    
    def main(self):
        while self.run:
            is_human_turn = self.turn != self.ai_color
            interupt_type, col, restart = self.draw.interrupt_check(self.board, self.game_over, is_human_turn)
            if restart:
                self.restart()
            
            
            self.draw.game_over(self.game_over)
            self.draw.blit_components_1(self.board, self.game_over, self.win_count)

            if not self.game_over and self.turn == self.ai_color:
                if not self.ai_thinking and self.ai_move is None:
                    self.ai_thinking = True
                    thread = threading.Thread(target=self.run_minimax, args=(self.board,))
                    thread.daemon = True
                    thread.start()
                
                elif not self.ai_thinking and self.ai_move is not None:
                    col = self.ai_move
                    self.ai_move = None
                    tp = self.draw.animate_draw_token(self.turn, col, self.board, self.win_count)
                    self.run = not (tp == False)
                    _, __, added = self.board.add_counter(self.turn, col, gameover=self.game_over)
                    if added:
                        self.next_turn()
                        continue

            elif interupt_type == 0:
                self.run = False
            elif col != None:
                tp = self.draw.animate_draw_token(self.turn, col, self.board, self.win_count)
                self.run = not(tp == False)
    
                _, __, added = self.board.add_counter(self.turn, col, gameover=self.game_over)
                if added:
                    self.next_turn()
                    continue
            
            self.draw.blit_components_2(self.board, self.turn, self.turn != self.ai_color)
            self.draw.draw_statements(self.choose_statement())
            self.draw.tick(60)


            winner = self.board.check_win()
            if winner != self.winner:
                self.winner = winner
                self.win_count.increase(self.winner)
            if self.winner != None:
                self.game_over = True

            self.draw.update_display()
        
        self.draw.quit()

    def next_turn(self):
        if self.turn == YELLOW:
            self.turn = RED
        else:
            self.turn = YELLOW
        
        self.draw.next_turn()

    
    def choose_statement(self):
        if self.game_over:
            if self.winner == 'No':
                return 'It\'s a DRAW!'
            elif self.winner == RED:
                return 'Red is the winner'
            elif self.winner == YELLOW:
                return 'Yellow is the winner'
        else:
            if self.ai_thinking:
                return 'AI is thinking...'
            t = 'Yellow' if self.turn == YELLOW else 'Red'
            return f'{t}\'s turn'
    
    def restart(self):
        self.game_over = False
        self.turn = random.choice([RED, YELLOW])
        self.run = True
        self.winner = None
        self.ai_thinking = False
        self.minimax = MiniMax(self.depth, self.ai_color)
        
        self.board = Board()
        self.draw = Draw(self.game_over)