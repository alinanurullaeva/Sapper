import pygame
from random import randint


class Board:
    def __init__(self, width, height, number):
        self.width = width
        self.height = height
        self.number = number
        self.board = [[0] * width for _ in range(height)]
        self.a = 50
        self.arr = []
        self.b = []
        self.c = []
        while len(self.b) != self.number:
            n = randint(0, self.width * self.height - 1)
            if n not in self.b:
                self.b.append(n)
        for i in self.b:
            self.c.append((i % self.width, i // self.height))
        for i in range(self.width):
            self.d = []
            for j in range(self.height):
                if (i, j) not in self.c:
                    self.d.append(0)
                else:
                    self.d.append('B')
            self.arr.append(self.d)
        for i in range(self.width):
            for j in range(self.height):
                self.arr[i][j] = self.check(i, j)
        print(self.arr)
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        a = self.a
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (100, 100, 100), (i * a, j * a, (i + 1) * a, (j + 1) * a), 1)

    def draw(self, screen, number, x, y):
        font = pygame.font.Font(None, 50)
        text = font.render(str(number), True, (0, 0, 0))
        screen.blit(text, (x * self.a, y * self.a))

    def check(self, x, y):
        arr = self.arr
        self.k = 0
        if arr[x][y] != 'B':
            try:
                if arr[x - 1][y - 1] == 'B':
                    self.k += 1
            except:
                pass
            try:
                if arr[x - 1][y] == 'B':
                    self.k += 1
            except:
                pass
            try:
                if arr[x - 1][y + 1] == 'B':
                    self.k += 1
            except:
                pass
            try:
                if arr[x][y - 1] == 'B':
                    self.k += 1
            except:
                pass
            try:
                if arr[x][y + 1] == 'B':
                    self.k += 1
            except:
                pass
            try:
                if arr[x + 1][y - 1] == 'B':
                    self.k += 1
            except:
                pass
            try:
                if arr[x + 1][y] == 'B':
                    self.k += 1
            except:
                pass
            try:
                if arr[x + 1][y + 1] == 'B':
                    self.k += 1
            except:
                pass
            return self.k
        return 'B'

pygame.init()
board = Board(5, 7, 3)
size = width, height = board.width * board.a, board.height * board.a
screen = pygame.display.set_mode(size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    board.render(screen)
    for i, el in enumerate(board.arr):
        for j, el2 in enumerate(el):
            board.draw(screen, str(el2), i, j)
    pygame.display.flip()
pygame.quit()