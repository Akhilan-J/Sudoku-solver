import pygame
import sys
import time
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (230, 240, 255)
BLUE = (0, 123, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 540, 600
CELL_SIZE = 60
GRID_SIZE = 9
MARGIN = 20

FONT = pygame.font.SysFont('comicsans', 40)
SMALL_FONT = pygame.font.SysFont('comicsans', 20)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")

class SudokuGame:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        self.selected = None
        self.generate_board()
        self.game_over = False
        self.feedback_message = ""
        self.feedback_time = 0
        self.timer_start = time.time()
    
    def generate_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board(self.board)
        solved_board = [row[:] for row in self.board]
        self.remove_elements(self.board, 40)  
        self.original_board = [row[:] for row in self.board]
        self.solved_board = solved_board
    
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, board, num, pos):
        for j in range(9):
            if board[pos[0]][j] == num and pos[1] != j:
                return False
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        
        return True
    
    def fill_board(self, board):
        nums = list(range(1, 10))
        empty = self.find_empty(board)
        
        if not empty:
            return True
        
        row, col = empty
        random.shuffle(nums)
        
        for num in nums:
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                
                if self.fill_board(board):
                    return True
                
                board[row][col] = 0
        
        return False
    
    def remove_elements(self, board, count):
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, j in cells[:count]:
            backup = board[i][j]
            board[i][j] = 0
            board_copy = [row[:] for row in board]
            solutions = [0]
            self.count_solutions(board_copy, solutions)
            
            if solutions[0] != 1:
                board[i][j] = backup
    
    def count_solutions(self, board, solutions, limit=2):
        if solutions[0] >= limit:
            return
        
        empty = self.find_empty(board)
        if not empty:
            solutions[0] += 1
            return
        
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                self.count_solutions(board, solutions, limit)
                board[row][col] = 0
    
    def select(self, row, col):
        if self.original_board[row][col] == 0:
            self.selected = (row, col)
    
    def place_number(self, num):
        if self.selected and self.original_board[self.selected[0]][self.selected[1]] == 0:
            self.board[self.selected[0]][self.selected[1]] = num
            if not self.is_valid(self.board, num, self.selected):
                self.feedback_message = "Invalid move!"
                self.feedback_time = time.time()
            if self.is_board_complete():
                self.feedback_message = "Congratulations! You solved the puzzle!"
                self.feedback_time = time.time()
                self.game_over = True
    
    def clear_cell(self):
        if self.selected and self.original_board[self.selected[0]][self.selected[1]] == 0:
            self.board[self.selected[0]][self.selected[1]] = 0
    
    def is_board_complete(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                self.board[i][j] = 0
                if not self.is_valid(self.board, num, (i, j)):
                    self.board[i][j] = num
                    return False
                self.board[i][j] = num
        
        return True
    
    def get_hint(self):
        if self.selected:
            row, col = self.selected
            if self.board[row][col] == 0:
                self.board[row][col] = self.solved_board[row][col]
                self.feedback_message = "Hint provided!"
                self.feedback_time = time.time()
    
    def solve_board(self):
        self.board = [row[:] for row in self.solved_board]
        self.game_over = True
        self.feedback_message = "Puzzle solved!"
        self.feedback_time = time.time()
    
    def draw_board(self):
        WIN.fill(WHITE)
        top_margin = MARGIN
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(WIN, BLACK, 
                           (MARGIN, top_margin + i * CELL_SIZE), 
                           (MARGIN + 9 * CELL_SIZE, top_margin + i * CELL_SIZE), 
                           line_width)
            pygame.draw.line(WIN, BLACK, 
                           (MARGIN + i * CELL_SIZE, top_margin), 
                           (MARGIN + i * CELL_SIZE, top_margin + 9 * CELL_SIZE), 
                           line_width)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    if self.original_board[i][j] != 0:
                        color = BLACK
                    else:
                        num = self.board[i][j]
                        self.board[i][j] = 0
                        if self.is_valid(self.board, num, (i, j)):
                            color = BLUE
                        else:
                            color = RED
                        self.board[i][j] = num
                    
                    text = FONT.render(str(self.board[i][j]), True, color)
                    text_rect = text.get_rect(center=(MARGIN + j * CELL_SIZE + CELL_SIZE // 2, 
                                                    top_margin + i * CELL_SIZE + CELL_SIZE // 2))
                    WIN.blit(text, text_rect)
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(WIN, LIGHT_BLUE, 
                           (MARGIN + col * CELL_SIZE, top_margin + row * CELL_SIZE, 
                            CELL_SIZE, CELL_SIZE))
            if self.board[row][col] != 0:
                if self.original_board[row][col] != 0:
                    color = BLACK
                else:
                    num = self.board[row][col]
                    self.board[row][col] = 0
                    if self.is_valid(self.board, num, (row, col)):
                        color = BLUE
                    else:
                        color = RED
                    self.board[row][col] = num
                
                text = FONT.render(str(self.board[row][col]), True, color)
                text_rect = text.get_rect(center=(MARGIN + col * CELL_SIZE + CELL_SIZE // 2, 
                                                top_margin + row * CELL_SIZE + CELL_SIZE // 2))
                WIN.blit(text, text_rect)
        self.draw_buttons()
        if not self.game_over:
            elapsed_time = int(time.time() - self.timer_start)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            timer_text = SMALL_FONT.render(f"Time: {minutes:02d}:{seconds:02d}", True, BLACK)
            WIN.blit(timer_text, (WIDTH - 120, 10))
        if self.feedback_message and time.time() - self.feedback_time < 3:
            feedback_text = SMALL_FONT.render(self.feedback_message, True, GREEN)
            WIN.blit(feedback_text, (WIDTH // 2 - feedback_text.get_width() // 2, 10))
        if self.game_over and self.feedback_message == "Congratulations! You solved the puzzle!":
            if int(time.time() * 5) % 2 == 0: 
                for _ in range(20):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    size = random.randint(3, 8)
                    color = random.choice([YELLOW, GREEN, BLUE])
                    pygame.draw.circle(WIN, color, (x, y), size)
    
    def draw_buttons(self):
        pygame.draw.rect(WIN, BLUE, (MARGIN, HEIGHT - 60, 100, 40), border_radius=5)
        new_game_text = SMALL_FONT.render("New Game", True, WHITE)
        WIN.blit(new_game_text, (MARGIN + 50 - new_game_text.get_width() // 2, 
                                HEIGHT - 60 + 20 - new_game_text.get_height() // 2))
        pygame.draw.rect(WIN, GREEN, (MARGIN + 120, HEIGHT - 60, 100, 40), border_radius=5)
        hint_text = SMALL_FONT.render("Hint", True, WHITE)
        WIN.blit(hint_text, (MARGIN + 120 + 50 - hint_text.get_width() // 2, 
                            HEIGHT - 60 + 20 - hint_text.get_height() // 2))
        pygame.draw.rect(WIN, RED, (MARGIN + 240, HEIGHT - 60, 100, 40), border_radius=5)
        solve_text = SMALL_FONT.render("Solve", True, WHITE)
        WIN.blit(solve_text, (MARGIN + 240 + 50 - solve_text.get_width() // 2, 
                             HEIGHT - 60 + 20 - solve_text.get_height() // 2))
        pygame.draw.rect(WIN, GRAY, (MARGIN + 360, HEIGHT - 60, 100, 40), border_radius=5)
        clear_text = SMALL_FONT.render("Clear", True, BLACK)
        WIN.blit(clear_text, (MARGIN + 360 + 50 - clear_text.get_width() // 2, 
                             HEIGHT - 60 + 20 - clear_text.get_height() // 2))
    
    def handle_click(self, pos):
        x, y = pos
        if (MARGIN <= x <= MARGIN + 9 * CELL_SIZE and 
            MARGIN <= y <= MARGIN + 9 * CELL_SIZE):
            col = (x - MARGIN) // CELL_SIZE
            row = (y - MARGIN) // CELL_SIZE
            
            if 0 <= row < 9 and 0 <= col < 9:
                self.select(row, col)
        elif (MARGIN <= x <= MARGIN + 100 and 
              HEIGHT - 60 <= y <= HEIGHT - 20):
            self.generate_board()
            self.selected = None
            self.game_over = False
            self.feedback_message = "New game started!"
            self.feedback_time = time.time()
            self.timer_start = time.time()
        elif (MARGIN + 120 <= x <= MARGIN + 220 and 
              HEIGHT - 60 <= y <= HEIGHT - 20):
            self.get_hint()
        elif (MARGIN + 240 <= x <= MARGIN + 340 and 
              HEIGHT - 60 <= y <= HEIGHT - 20):
            self.solve_board()
        elif (MARGIN + 360 <= x <= MARGIN + 460 and 
              HEIGHT - 60 <= y <= HEIGHT - 20):
            self.clear_cell()

def main():
    game = SudokuGame()
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.handle_click(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    game.place_number(1)
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    game.place_number(2)
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    game.place_number(3)
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    game.place_number(4)
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    game.place_number(5)
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    game.place_number(6)
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    game.place_number(7)
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    game.place_number(8)
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    game.place_number(9)
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    game.clear_cell()
        
        game.draw_board()
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()