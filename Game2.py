import pygame
from random import randint, choice

GRID_COLOR = "#FFC0CB"
EMPTY_CELL_COLOR = "#FFFFFF"
SCORE_LABEL_FONT = "Arial"

CELL_COLORS = {
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#f5b682",
    16: "#f29446",
    32: "#ff775c",
    64: "#e64c2e",
    128: "#ede291",
    256: "#fce130",
    512: "#ffdb4a",
    1024: "#f0b922",
    2048: "#fad74d"
}

CELL_NUMBER_COLORS = {
    2: "#695c57",
    4: "#695c57",
    8: "#ffffff",
    16: "#ffffff",
    32: "#ffffff",
    64: "#ffffff",
    128: "#ffffff",
    256: "#ffffff",
    512: "#ffffff",
    1024: "#ffffff",
    2048: "#ffffff"
}

BACK_BUTTON_X = 280
BACK_BUTTON_Y = 10
BACK_BUTTON_WIDTH = 100
BACK_BUTTON_HEIGHT = 50
BACK_BUTTON_COLOR = (255, 255, 255)

WIDTH, HEIGHT = 400, 500
FPS = 30
MARGIN = 20
CELL_SPACING = 10


def load_highest_score():
    try:
        with open("static/highest_score.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highest_score(score):
    with open("static/highest_score.txt", "w") as file:
        file.write(str(score))





class Game2:
    def __init__(self, window, high_score=0, grid_size=4):
        self.window = window
        self.grid_size = grid_size
        self.cell_size = (WIDTH - 2 * MARGIN - (grid_size - 1) * CELL_SPACING) // grid_size
        self.matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.cells = []
        self.score = [0, 0]
        self.high_score = high_score  # Initialize high score
        self.highest_score = load_highest_score()
        self.fontEngine = pygame.font.SysFont(SCORE_LABEL_FONT, 30)
        self.over = [False, False]
        self.startGame()

    def startGame(self):
        row, col = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
        self.matrix[row][col] = 2
        while self.matrix[row][col] != 0:
            row, col = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
        self.matrix[row][col] = 2

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                rect = pygame.Rect(
                    MARGIN + j * (self.cell_size + CELL_SPACING),
                    MARGIN + 50 + i * (self.cell_size + CELL_SPACING),
                    self.cell_size,
                    self.cell_size
                )
                textRect, textSurface = None, None
                if (x := self.matrix[i][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = rect.center
                row.append({
                    "rect": rect,
                    "textRect": textRect,
                    "textSurface": textSurface
                })
            self.cells.append(row)

        scoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 30).render('Score : ', True, (0, 0, 0))
        scoreRect = scoreSurface.get_rect()
        scoreRect.top = 10
        scoreRect.left = MARGIN
        self.score[1] = [scoreSurface, scoreRect]

    def addNewTile(self):
        row, col = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
        while self.matrix[row][col] != 0:
            row, col = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
        self.matrix[row][col] = choice([2, 2, 2, 2, 4])

    def horMoveExists(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.matrix[i][j + 1] == self.matrix[i][j]:
                    return True
        return False

    def verMoveExists(self):
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size):
                if self.matrix[i + 1][j] == self.matrix[i][j]:
                    return True
        return False

    def gameOver(self):
        if any(2048 in row for row in self.matrix):
            self.over = [True, True]
        if not any(0 in row for row in self.matrix) and not self.horMoveExists() and not self.verMoveExists():
            self.over = [True, False]

    def updateTiles(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (x := self.matrix[i][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = self.cells[i][j]['rect'].center
                    self.cells[i][j]['textRect'] = textRect
                    self.cells[i][j]['textSurface'] = textSurface
                elif x == 0:
                    self.cells[i][j]['textRect'] = None
                    self.cells[i][j]['textSurface'] = None

    def stack(self):
        new_matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            position = 0
            for j in range(self.grid_size):
                if self.matrix[i][j] != 0:
                    new_matrix[i][position] = self.matrix[i][j]
                    position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                x = self.matrix[i][j]
                if x != 0 and x == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score[0] += self.matrix[i][j]
                    if self.score[0] > self.highest_score:
                        self.highest_score = self.score[0]
                        save_highest_score(self.highest_score)

    def reverse(self):
        new_matrix = []
        for row in self.matrix:
            new_matrix.append(row[::-1])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                new_matrix[j][i] = self.matrix[i][j]
        self.matrix = new_matrix

    def scs(self):
        oldmatrix = self.matrix
        self.stack()
        self.combine()
        self.stack()
        return oldmatrix

    def aug(self):
        self.addNewTile()
        self.updateTiles()
        self.gameOver()

    def left(self):
        oldmatrix = self.scs()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def right(self):
        oldmatrix = self.matrix
        self.reverse()
        self.scs()
        self.reverse()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def up(self):
        oldmatrix = self.matrix
        self.transpose()
        self.scs()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def down(self):
        oldmatrix = self.matrix
        self.transpose()
        self.reverse()
        self.scs()
        self.reverse()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def reset(self):
        self.score[0] = 0  # Reset the current score
        self.matrix = [[0] * self.grid_size for _ in range(self.grid_size)]  # Clear the matrix
        self.cells = []
        self.over = [False, False]
        self.startGame()
class Game2:
    def __init__(self, window, high_score=0, grid_size=4):
        self.window = window
        self.grid_size = grid_size
        self.cell_size = (WIDTH - 2 * MARGIN - (grid_size - 1) * CELL_SPACING) // grid_size
        self.matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.cells = []
        self.score = [0, 0]
        self.high_score = high_score  # Initialize high score
        self.highest_score = load_highest_score()
        self.fontEngine = pygame.font.SysFont(SCORE_LABEL_FONT, 30)
        self.over = [False, False]
        self.startGame()

    def startGame(self):
        row, col = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
        self.matrix[row][col] = 2
        while self.matrix[row][col] != 0:
            row, col = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
        self.matrix[row][col] = 2

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                rect = pygame.Rect(
                    MARGIN + j * (self.cell_size + CELL_SPACING),
                    MARGIN + 50 + i * (self.cell_size + CELL_SPACING),
                    self.cell_size,
                    self.cell_size
                )
                textRect, textSurface = None, None
                if (x := self.matrix[i][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = rect.center
                row.append({
                    "rect": rect,
                    "textRect": textRect,
                    "textSurface": textSurface
                })
            self.cells.append(row)

        scoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 20).render('Score : ', True, (0, 0, 0))
        scoreRect = scoreSurface.get_rect()
        scoreRect.top = 10
        scoreRect.left = MARGIN
        self.score[1] = [scoreSurface, scoreRect]

    def addNewTile(self):
        row, col = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
        while self.matrix[row][col] != 0:
            row, col = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
        self.matrix[row][col] = choice([2, 2, 2, 2, 4])

    def horMoveExists(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.matrix[i][j + 1] == self.matrix[i][j]:
                    return True
        return False

    def verMoveExists(self):
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size):
                if self.matrix[i + 1][j] == self.matrix[i][j]:
                    return True
        return False

    def gameOver(self):
        if any(2048 in row for row in self.matrix):
            self.over = [True, True]
        if not any(0 in row for row in self.matrix) and not self.horMoveExists() and not self.verMoveExists():
            self.over = [True, False]

    def updateTiles(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (x := self.matrix[i][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = self.cells[i][j]['rect'].center
                    self.cells[i][j]['textRect'] = textRect
                    self.cells[i][j]['textSurface'] = textSurface
                elif x == 0:
                    self.cells[i][j]['textRect'] = None
                    self.cells[i][j]['textSurface'] = None

    def stack(self):
        new_matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            position = 0
            for j in range(self.grid_size):
                if self.matrix[i][j] != 0:
                    new_matrix[i][position] = self.matrix[i][j]
                    position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                x = self.matrix[i][j]
                if x != 0 and x == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score[0] += self.matrix[i][j]
                    if self.score[0] > self.highest_score:
                        self.highest_score = self.score[0]
                        save_highest_score(self.highest_score)

    def reverse(self):
        new_matrix = []
        for row in self.matrix:
            new_matrix.append(row[::-1])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                new_matrix[j][i] = self.matrix[i][j]
        self.matrix = new_matrix

    def scs(self):
        oldmatrix = self.matrix
        self.stack()
        self.combine()
        self.stack()
        return oldmatrix

    def aug(self):
        self.addNewTile()
        self.updateTiles()
        self.gameOver()

    def left(self):
        oldmatrix = self.scs()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def right(self):
        oldmatrix = self.matrix
        self.reverse()
        self.scs()
        self.reverse()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def up(self):
        oldmatrix = self.matrix
        self.transpose()
        self.scs()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def down(self):
        oldmatrix = self.matrix
        self.transpose()
        self.reverse()
        self.scs()
        self.reverse()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def reset(self):
        self.score[0] = 0  # Reset the current score
        self.matrix = [[0] * self.grid_size for _ in range(self.grid_size)]  # Clear the matrix
        self.cells = []
        self.over = [False, False]
        self.startGame()