import pygame
from random import randint


class Board:
    def __init__(self, width, height, bomb_count):
        self.width = width
        self.height = height
        self.bomb_count = bomb_count
        self.board_hidden = [[0] * height for _ in range(width)]
        self.flag = True  # меняется на False, когда игра завершается
        self.coords_levels = []
        self.coords_retry = []
        self.won = False

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
        self.marked_cell = 0

    def render(self, screen):
        width = self.base_board.width
        height = self.base_board.height
        scale = self.scale
        for i in range(self.base_board.width):
            for j in range(self.base_board.height):
                pygame.draw.rect(screen, (100, 100, 100), (i * scale, j * scale, scale, scale), 1)
        font = pygame.font.Font(None, 50)
        text = font.render("Назад", True, (0, 0, 0))
        text_x = (width * scale) // 4 - text.get_width() // 2
        text_y = scale * (height + 1) + scale // 2
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 0, 0), (0, scale * (height + 1), scale * width // 2, scale * 1.5), 1)
        self.base_board.coords_levels = [0, scale * (height + 1), scale * width // 2,
                                         scale * (height + 2.5)]
        font = pygame.font.Font(None, 50)
        text = font.render("Заново", True, (0, 0, 0))
        text_x = (width * scale) // 4 * 3 - text.get_width() // 2
        text_y = scale * (height + 1) + scale // 2
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 0, 0), (scale * width // 2, scale * (height + 1),
                                             scale * width // 2, scale * 1.5), 1)
        self.base_board.coords_retry = [scale * width // 2, scale * (height + 1),
                                        scale * width, scale * (height + 2.5)]

    def draw(self, screen, number, x, y):
        open_cell = 0
        if self.base_board.flag and self.was_drawn[x][y] != 2:
            self.was_drawn[x][y] = 1
        for i, el1 in enumerate(self.was_drawn):  
            for j, el2 in enumerate(el1):
                if el2 == 1:
                    if self.base_board.board_hidden[i][j] == 'B':
                        self.draw_number(screen, self.base_board.board_hidden[i][j], i, j, color=(255, 0, 0))
                        if self.base_board.flag:
                            self.base_board.flag = False
                            self.base_board.won = False
                    else:
                        open_cell += 1
                        self.draw_number(screen, self.base_board.board_hidden[i][j], i, j)
                elif el2 == 2 and not self.base_board.flag and self.base_board.board_hidden[i][j] != 'B':
                    self.draw_number(screen, self.base_board.board_hidden[i][j], i, j, color=(0, 0, 200))
                elif el2 == 2 and self.base_board.flag:
                    self.draw_number(screen, 'B', i, j, color=(255, 0, 0))
                elif el2 == 2 and not self.base_board.flag:
                    self.draw_number(screen, 'B', i, j, color=(0, 150, 0))
                elif not self.base_board.flag:
                    self.draw_number(screen, self.base_board.board_hidden[i][j], i, j, color=(150, 150, 150))
        if open_cell == self.base_board.width * self.base_board.height - self.base_board.bomb_count and \
                self.base_board.flag:
            self.base_board.won = True
            self.marked_cell = self.base_board.bomb_count
            self.base_board.flag = False
        self.draw_number(screen, self.base_board.bomb_count - self.marked_cell, 0, self.base_board.height)
        if not self.base_board.flag:
            if self.base_board.won:
                font = pygame.font.Font(None, 50)
                text = font.render("Победа", True, (0, 0, 0))
                text_x = (self.base_board.width * self.scale) // 2 - text.get_width() // 2
                text_y = self.scale * self.base_board.height
                screen.blit(text, (text_x, text_y))
            else:
                font = pygame.font.Font(None, 50)
                text = font.render("Проигрыш", True, (0, 0, 0))
                text_x = (self.base_board.width * self.scale) // 2 - text.get_width() // 2
                text_y = self.scale * self.base_board.height
                screen.blit(text, (text_x, text_y))
        if self.base_board.board_hidden[x][y] == 0:
            a = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                 (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        else:
            a = []
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
                self.marked_cell += 1
            elif self.was_drawn[i][j] == 2:
                self.was_drawn[i][j] = 0
                self.marked_cell -= 1

    def draw_number(self, screen, text, i, j, color=(0, 0, 0)):
        if text == 0 and 0 <= j <= self.base_board.height - 1:
            scale = self.scale
            pygame.draw.rect(screen, (200, 200, 200), (i * scale, j * scale, scale, scale), 0)
            pygame.draw.rect(screen, (100, 100, 100), (i * scale, j * scale, scale, scale), 1)
        else:
            font = pygame.font.Font(None, 50)
            text = font.render(str(text), True, color)
            screen.blit(text, (i * self.scale, j * self.scale))


class First_Window_UI():
    def __init__(self):
        self.coord_rect1 = []
        self.coord_rect2 = []
        self.coord_rect3 = []

    def draw(self, screen, width, height):
        font = pygame.font.Font(None, 50)
        text = font.render("Добро пожаловать! Пожалуйста, выберите уровень", True, (0, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 5 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))

        text = font.render("Уровень 1", True, (0, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 5 * 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)
        self.coord_rect1 = [text_x - 10, text_y - 10, text_x + text_w + 10, text_y + text_h + 10]

        text = font.render("Уровень 2", True, (0, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 5 * 3 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)
        self.coord_rect2 = [text_x - 10, text_y - 10, text_x + text_w + 10, text_y + text_h + 10]

        text = font.render("Уровень 3", True, (0, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 5 * 4 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)
        self.coord_rect3 = [text_x - 10, text_y - 10, text_x + text_w + 10, text_y + text_h + 10]


def check_in_rect(x, y, coords):
    if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
        return True
    return False


def start_first_window():
    pygame.init()
    first_window = First_Window_UI()
    size_first_window = width_first_window, height_first_window = 900, 500
    screen_first_window = pygame.display.set_mode(size_first_window)
    running_first_window = True
    screen_first_window.fill((255, 255, 255))
    first_window.draw(screen_first_window, width_first_window, height_first_window)
    pygame.display.flip()
    while running_first_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_first_window = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    if check_in_rect(event.pos[0], event.pos[1], first_window.coord_rect1):
                        pygame.quit()
                        start_game(10, 10, 15)
                    elif check_in_rect(event.pos[0], event.pos[1], first_window.coord_rect2):
                        pygame.quit()
                        start_game(15, 10, 25)
                    elif check_in_rect(event.pos[0], event.pos[1], first_window.coord_rect3):
                        pygame.quit()
                        start_game(15, 15, 40)



def start_game(width, height, bomb_count):
    pygame.init()
    board_base = Board(width, height, bomb_count)
    board_UI = BoardUI(board_base)
    size = board_UI.base_board.width * board_UI.scale, \
        int((board_UI.base_board.height + 2.5) * board_UI.scale)
    screen_game = pygame.display.set_mode(size)
    running_game = True
    x = randint(0, board_base.width - 1)
    y = randint(0, board_base.height - 1)
    while board_base.board_hidden[x][y] != 0:
        x = randint(0, board_base.width - 1)
        y = randint(0, board_base.height - 1)
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == pygame.MOUSEBUTTONUP:
                i = event.pos[0] // board_UI.scale
                j = event.pos[1] // board_UI.scale
                if 0 <= i <= board_base.width - 1 and 0 <= j <= board_base.height - 1:
                    if event.button == 1:
                        board_UI.draw(screen_game, board_base.board_hidden[i][j], i, j)
                    if event.button == 3:
                        board_UI.draw_bomb(screen_game, i, j)
                elif event.button == 1 or event.button == 3:
                    if check_in_rect(event.pos[0], event.pos[1], board_base.coords_levels):
                        pygame.quit()
                        start_first_window()
                    elif check_in_rect(event.pos[0], event.pos[1], board_base.coords_retry):
                        pygame.quit()
                        start_game(width, height, bomb_count)
        screen_game.fill((255, 255, 255))
        board_UI.render(screen_game)
        board_UI.draw(screen_game, board_base.board_hidden[x][y], x, y)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    start_first_window()
