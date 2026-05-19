import pygame
from .constants import *
from .Replay import Replay
from .Bird import Birds
import math

class Draw:
    def __init__(self, game_over):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Connect Four')
        self.screen.fill(WHITE)
        pygame.display.flip()

        self.board_ui = pygame.image.load('Assets\Board.png')
        self.yellow_token = pygame.image.load('Assets/yellow_token.png').convert_alpha()
        self.red_token = pygame.image.load('Assets/red_token.png').convert_alpha()
        self.bg = pygame.image.load('Assets/playground.png').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        self.flash_visible = False
        self.last_flash = 0
        self.old_loc = None
        self.is_game_over = game_over

        self.text_font = pygame.font.Font('Assets/BagelFatOne-Regular.ttf', 20)
        self.counter_font = pygame.font.Font('Assets/BubbleBobble-rg3rx.ttf', 30)

        self.clock = pygame.time.Clock()
        self.replay = Replay()
        self.birds = Birds()

    def blit_components_1(self, board, gameover, counter):
        self.screen.fill(WHITE)
        self.screen.blit(self.bg, (0, 0))
        self.blit_tokens(board)
        self.blit_counts(counter)
        self.blit_birds()
        self.blit_replay_button(gameover)

    def blit_components_2(self, board, turn, is_human_turn):
        if is_human_turn:
            self.blit_mouse_token(board, turn)
        self.blit_board()
    
    def blit_replay_button(self, game_over):
        if game_over:
            self.replay.pulsate(self.screen)

    def blit_birds(self):
        b1, b2, pos = self.birds.next()
        self.screen.blit(b1, ((pos % (WIDTH + 240))-50, (50 + (math.sin(pos)))))
        self.screen.blit(b2, (1100, 250))

    def blit_counts(self, win_count):
        red_count = self.counter_font.render(str(win_count.return_red_count()), True, (255, 255, 255))
        yellow_count = self.counter_font.render(str(win_count.return_yellow_count()), True, (255, 255, 255))
        red_countRect = red_count.get_rect()
        yellow_countRect = yellow_count.get_rect()
        red_countRect.center = (153, 675)
        yellow_countRect.center = (1185, 675)
        self.screen.blit(red_count, red_countRect)
        self.screen.blit(yellow_count, yellow_countRect)

    def blit_board(self):
        self.screen.blit(self.board_ui, (357, 148))
    
    def blit_mouse_token(self, board, turn):
        h_col = self.get_mouse_column(board)
        if h_col != None and not self.is_game_over:
            row, col, _ = board.add_counter(None, h_col, False)
            if row == None and col == None:
                return
            x, y = self.get_counter_coords(board, row, col)
            loc = (x, y)

            counter = self.counter_for_turn(turn)
            self.flash_token(counter, loc)

    def flash_token(self, token, loc):
        current_time = pygame.time.get_ticks()
        if self.old_loc != loc:
            self.last_flash = current_time

        if current_time - self.last_flash > 375:
            self.flash_visible = not self.flash_visible
            self.last_flash = current_time
        
        
        if self.flash_visible:
            self.screen.blit(token, loc)
        
        self.old_loc = loc

    def grey_overlay_token(self, token_img):
        grey_overlay = pygame.Surface(token_img.get_size(), pygame.SRCALPHA)
        grey_overlay.fill((120, 120, 120, 100))
        greyed_token = token_img.copy()
        greyed_token.blit(grey_overlay, (0, 0))
        return greyed_token
    
    def blit_tokens(self, board):
        for row in range(board.get_rows()):
            for col in range(board.get_col()):
                x,y = self.get_counter_coords(board, row, col)
                cell = board.get(row, col)
                if not cell.is_empty():
                    counter = self.counter_for_turn(cell.get_color())
                    self.screen.blit(counter, (x, y))
    
    def get_counter_coords(self, board, row, col):
        x = 400 + (col * (890 - 400) / (board.get_col() - 1))
        y = 180 + (board.get_rows() - 1 - row) * (570 - 180) / (board.get_rows() - 1)
        return x, y

    def counter_for_turn(self, color):
        if color == YELLOW:
            counter = self.yellow_token
        elif color == RED: 
            counter = self.red_token
        return counter

    def get_mouse_column(self, board):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        start_x = 400
        end_x = 960

        col_width = (end_x - start_x) / board.get_col()

        if (mouse_x >= start_x) and (mouse_x <= end_x) and (mouse_y <= 670):
            for i in range(board.get_col()):
                if ((col_width * (i+1)) + start_x) >= mouse_x:
                    return i
        else:
            return None

    def tick(self, num):
        self.clock.tick(num)
    
    def interrupt_check(self, board, gameover, is_human_turn=True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0, None, None
            elif event.type == pygame.MOUSEBUTTONUP:
                if gameover:
                    if self.replay.clicked():
                        return None, None, True
                elif is_human_turn:
                    return 1, self.get_mouse_column(board), None
        return None, None, None
    
    def next_turn(self):
        current_time = pygame.time.get_ticks()
        self.last_flash = current_time

    def update_display(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()

    def game_over(self, over):
        self.is_game_over = over
    
    def draw_statements(self, statement):
        text = self.text_font.render(statement, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1160, 413)
        self.screen.blit(text, textRect)
    
    def animate_draw_token(self, color, column, board, win_count, gameover=False):
        counter = self.counter_for_turn(color)
        if column != None and not self.is_game_over:
            row_num, col_num, _ = board.add_counter(None, column, False)
            
            if row_num == None:
                return
            
            final_x, final_y = self.get_counter_coords(board, row_num, col_num)
            current_y = 120

            while current_y < final_y:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return False
            
                self.blit_components_1(board, gameover, win_count)
                self.screen.blit(counter, (final_x, current_y))
                self.blit_board()

                pygame.display.flip()

                current_y += 10
                self.clock.tick(150)
        
            self.blit_components_1(board, gameover, win_count)
            self.screen.blit(counter, (final_x, final_y))
            self.blit_board()

            pygame.display.flip()