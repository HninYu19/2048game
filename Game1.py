import pygame
import os

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

WIDTH, HEIGHT = 400, 500
FPS = 30



class Game1:
    def __init__(self, window, level=1):
        self.window = window
        self.level = level
        self.matrix = [[0] * 4 for _ in range(4)]
        self.cells = []
        self.score = [0, 0]
        self.steps=[0,0]
        self.fontEngine = pygame.font.SysFont(SCORE_LABEL_FONT, 45)
        self.over = [False, False]
        self.startGame()

    def startGame(self):
        with open("static/level/level%d.txt" % self.level) as fin:
            l = [list(map(int, line.split())) for line in fin]

        for i in range(4):
            for j in range(4):
                self.matrix[i][j] = l[i][j]

        for i in range(1, 5):
            row = []
            for j in range(4):
                rect = pygame.Rect(10 + j * 100, 10 + i * 100, 80, 80)
                textRect, textSurface = None, None
                if (x := self.matrix[i - 1][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = rect.center
                row.append({
                    "rect": rect,
                    "textRect": textRect,
                    "textSurface": textSurface
                })
            self.cells.append(row)
        stepsSurface=pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('Steps : ', True, (0, 0, 0))
        stepsRect = stepsSurface.get_rect()
        scoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('Score : ', True, (0, 0, 0))
        scoreRect = scoreSurface.get_rect()
        stepsRect.top=10
        scoreRect.top = 40
        self.steps[1] = [stepsSurface, stepsRect]
        self.score[1] = [scoreSurface, scoreRect]

    def next_level(self):
        self.level += 1
        if not os.path.isfile("static/level/level%d.txt" % self.level):
            return False  # 表示没有下一关
        self.startGame()  # 传入新的关卡文件路径
        return True  # 表示已经加载了下一关

    def horMoveExists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j + 1] == self.matrix[i][j]:
                    return True
        return False

    def verMoveExists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i + 1][j] == self.matrix[i][j]:
                    return True
        return False

    def gameOver(self):
        if any(2048 in row for row in self.matrix):
            self.over = [True, True]
        if not any(0 in row for row in self.matrix) and not self.horMoveExists() and not self.verMoveExists():
            self.over = [True, False]

    def updateTiles(self):
        for i in range(4):
            for j in range(4):

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
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][position] = self.matrix[i][j]
                    position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                x = self.matrix[i][j]
                if x != 0 and x == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score[0] += self.matrix[i][j]

    def reverse(self):
        new_matrix = []
        for row in self.matrix:
            new_matrix.append(row[::-1])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[j][i] = self.matrix[i][j]
        self.matrix = new_matrix

    def scs(self):
        oldmatrix = self.matrix
        self.stack()
        self.combine()
        self.stack()
        return oldmatrix

    def aug(self):
        self.updateTiles()
        self.gameOver()

    def left(self):
        self.steps[0]+=1
        oldmatrix = self.scs()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def right(self):
        self.steps[0]+=1
        oldmatrix = self.matrix
        self.reverse()
        self.scs()
        self.reverse()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def up(self):
        self.steps[0]+=1
        oldmatrix = self.matrix
        self.transpose()
        self.scs()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def down(self):
        self.steps[0]+=1
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
        self.__init__(self.window, level=self.level)
