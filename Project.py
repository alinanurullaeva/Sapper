import pygame
from random import randint

class Board:
    def __init__(self, width, height, bomb_count):
        self.width = width
        self.height = height
        self.bomb_count = bomb_count
        self.board_hidden = [[0] * height for _ in range(width)]
        
        non_repeatible_coords = []
        while len(non_repeatible_coords) != self.bomb_count:
            coord = (randint(0, self.width - 1), randint(0, self.height - 1))
            if coord not in non_repeatible_coords:
                non_repeatible_coords.append(coord)
            
        for bomb in non_repeatible_coords:
            x, y = bomb
            self.board_hidden[x][y] = 'B'
                
        for i in range(self.width):
            for j in range(self.height):
                self.board_hidden[i][j] = self.check_bomb_count(i, j)
                
        print(*self.board_hidden, sep='\n')
        
    def check_bomb_count(self, x, y):
        arr = self.board_hidden
        count = 0
        if arr[x][y] != 'B':
            for i in range(3):
                for j in range(3):
                    checkX = (x - 1) + i
                    checkY = (y - 1) + j
                    if (0 <= checkX < self.width) and (0 <= checkY < self.height):
                        if arr[checkX][checkY] == 'B':
                            count += 1
            return count
        return 'B'


class BoardUI:
    def __init__(self, board: Board):
        self.base_board = board
        self.scale = 50 
        
        self.left = 10       # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.top = 10        # Не очень понимаю, зачем это нужно
        self.cell_size = 30  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    
    def render(self, screen):
        scale = self.scale
        for i in range(self.base_board.width):
            for j in range(self.base_board.height):
                pygame.draw.rect(screen, (100, 100, 100), (i * scale, j * scale, (i + 1) * scale, (j + 1) * scale), 1)
    
    def draw(self, screen, number, x, y):
        font = pygame.font.Font(None, 50)
        text = font.render(str(number), True, (0, 0, 0))
        screen.blit(text, (x * self.scale, y * self.scale))

pygame.init()
board_base = Board(10, 10, 10)
board_UI = BoardUI(board_base)
size = width, height = board_UI.base_board.width * board_UI.scale, board_UI.base_board.height * board_UI.scale
screen = pygame.display.set_mode(size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    board_UI.render(screen)
    for i, el in enumerate(board_UI.base_board.board_hidden):
        for j, el2 in enumerate(el):
            board_UI.draw(screen, str(el2), i, j)
    pygame.display.flip()
pygame.quit()