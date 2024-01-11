import pygame
from random import randint
    
class Board:
    def __init__(self, width, height, number):
        self.width = width
        self.height = height
        self.number = number
        self.board = [[0] * height for _ in range(width)]
        self.scale = 50 
        
        non_repeatible_coords = []
        while len(non_repeatible_coords) != self.number:
            coord = (randint(0, self.width - 1), randint(0, self.height - 1))
            if coord not in non_repeatible_coords:
                non_repeatible_coords.append(coord)
            
        for bomb in non_repeatible_coords:
            x, y = bomb
            self.board[x][y] = 'B'
                
        for i in range(self.width):
            for j in range(self.height):
                self.board[i][j] = self.check(i, j)
                
        print(self.board)
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        scale = self.scale
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (100, 100, 100), (i * scale, j * scale, (i + 1) * scale, (j + 1) * scale), 1)

    def draw(self, screen, number, x, y):
        font = pygame.font.Font(None, 50)
        text = font.render(str(number), True, (0, 0, 0))
        screen.blit(text, (x * self.scale, y * self.scale))

    def check(self, x, y):
        arr = self.board
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

pygame.init()
board = Board(5, 7, 3)
size = width, height = board.width * board.scale, board.height * board.scale
screen = pygame.display.set_mode(size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    board.render(screen)
    for i, el in enumerate(board.board):
        for j, el2 in enumerate(el):
            board.draw(screen, str(el2), i, j)
    pygame.display.flip()
pygame.quit()