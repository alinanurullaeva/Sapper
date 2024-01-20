import pygame
from random import randint


class Board:
    def __init__(self, width, height, bomb_count):
        self.width = width
        self.height = height
        self.bomb_count = bomb_count
        self.board_hidden = [[0] * height for _ in range(width)]
        self.flag = True # меняется на False, когда игра завершается

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
        self.scale = 40
        self.was_drawn = [[0] * self.base_board.height for _ in range(self.base_board.width)]

    def render(self, screen):
        scale = self.scale
        for i in range(self.base_board.width):
            for j in range(self.base_board.height):
                pygame.draw.rect(screen, (100, 100, 100), (i * scale, j * scale, (i + 1) * scale, (j + 1) * scale), 1)

    def draw(self, screen, number, x, y):
        open_cell = 0
        if self.base_board.flag and self.was_drawn[x][y] != 2:
            self.was_drawn[x][y] = 1
        for i, el1 in enumerate(self.was_drawn): # def draw_number(self, text, i, j, color=(0, 0, 0)):
            for j, el2 in enumerate(el1):
                if el2 == 1:
                    if self.base_board.board_hidden[i][j] == 'B':
                        self.draw_number(self.base_board.board_hidden[i][j], i, j, color=(255, 0, 0))
                        if self.base_board.flag:
                            self.base_board.flag = False
                            print('Увы. Вы проиграли. Игра завершена')
                    else:
                        open_cell += 1
                        self.draw_number(self.base_board.board_hidden[i][j], i, j)
                elif el2 == 2 and not self.base_board.flag and self.base_board.board_hidden[i][j] != 'B':
                    self.draw_number(self.base_board.board_hidden[i][j], i, j, color=(0, 0, 200))
                elif el2 == 2 and self.base_board.flag:
                    self.draw_number('B', i, j, color=(255, 0, 0))
                elif el2 == 2 and not self.base_board.flag:
                    self.draw_number('B', i, j, color=(0, 150, 0))
                elif not self.base_board.flag:
                    self.draw_number(self.base_board.board_hidden[i][j], i, j, color=(150, 150, 150))
        if open_cell == self.base_board.width * self.base_board.height - self.base_board.bomb_count and \
                self.base_board.flag:
            print('Поздравляю! Вы победили! Игра завершена')
            self.base_board.flag = False
        a = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
             (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        if self.base_board.board_hidden[x][y] == 0:
            for i, j in a:
                if 0 <= i <= self.base_board.width - 1 and 0 <= j <= self.base_board.height - 1:
                    if self.was_drawn[i][j] == 0:
                        self.draw(screen, self.base_board.board_hidden[i][j], i, j)
        for i, j in a:
            if 0 <= i <= self.base_board.width - 1 and 0 <= j <= self.base_board.height - 1:
                if self.was_drawn[i][j] == 0:
                    if self.base_board.board_hidden[i][j] == 0:
                        self.draw(screen, 0, i, j)

    def draw_bomb(self, screen, i, j):
        if self.base_board.flag:
            if self.was_drawn[i][j] == 0:
                self.was_drawn[i][j] = 2
            elif self.was_drawn[i][j] == 2:
                self.was_drawn[i][j] = 0

    def draw_number(self, text, i, j, color=(0, 0, 0)):
        font = pygame.font.Font(None, 50)
        text = font.render(str(text), True, color)
        screen.blit(text, (i * self.scale, j * self.scale))


pygame.init()
board_base = Board(10, 10, 15)
board_UI = BoardUI(board_base)
size = width, height = board_UI.base_board.width * board_UI.scale, board_UI.base_board.height * board_UI.scale
screen = pygame.display.set_mode(size)
running = True
x = randint(0, board_base.width - 1)
y = randint(0, board_base.height - 1)
while board_base.board_hidden[x][y] != 0:
    x = randint(0, board_base.width - 1)
    y = randint(0, board_base.height - 1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            i = event.pos[0] // board_UI.scale
            j = event.pos[1] // board_UI.scale
            if event.button == 1:
                board_UI.draw(screen, board_base.board_hidden[i][j], i, j)
            if event.button == 3:
                board_UI.draw_bomb(screen, i, j)
    screen.fill((255, 255, 255))
    board_UI.render(screen)
    board_UI.draw(screen, board_base.board_hidden[x][y], x, y)
    '''for i, el in enumerate(board_UI.base_board.board_hidden):
        for j, el2 in enumerate(el):
            board_UI.draw(screen, str(el2), i, j)'''
    pygame.display.flip()
pygame.quit()