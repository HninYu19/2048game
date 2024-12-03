import pygame
import pygame_gui
from number_two import Target1
from number_zero import Target2
from number_four import Target3
from number_eight import Target4
from random import randint, choice
from Game1 import Game1
from Game2 import Game2

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

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
FONT1 = pygame.font.SysFont("simhei", 36)
FONT2 = pygame.font.SysFont("华文新魏", 24)
FONT3 = pygame.font.SysFont("华文新魏", 12)

pygame.display.set_caption('2048 Game')
background_image = pygame.image.load("static/images/back.png")
ico = pygame.image.load("static/images/2048.ico").convert()
pygame.display.set_icon(ico)

pygame.mixer.music.load("static/sounds/bgm.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.Channel(7)
pygame.mixer.music.play(-1)  # 参数-1表示循环播放

background_image = pygame.transform.scale(background_image, (400, 500))

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# 创建文本输入框
input_rect = pygame.Rect((50, 50), (300, 50))
input_box = pygame_gui.elements.UITextEntryLine(
    relative_rect=input_rect,
    manager=manager,
    initial_text=''
)

label_rect = pygame.Rect((50, 110), (300, 20))  # 假设你希望它位于输入框下方60个像素的位置
label = pygame_gui.elements.UILabel(
    relative_rect=label_rect,
    manager=manager,
    text="Please sign up your username"
)

label_rect = pygame.Rect((50, 170), (300, 20))  # 假设你希望它位于输入框下方60个像素的位置
label = pygame_gui.elements.UILabel(
    relative_rect=label_rect,
    manager=manager,
    text="Then press the ENTER "
)

# 存储文件路径
save_file_path = "static/file.txt"

# 文本变化的标志
text_changed = False

clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                # 当按下回车键时，保存文本并退出
                if input_box.get_text():
                    with open(save_file_path, 'a') as f:
                        f.write(f'{input_box.get_text()}\n')
                    input_box.set_text('')  # 清空输入框
                running = False

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(window)
    pygame.display.flip()


def load_highest_score():
    try:
        with open("static/highest_score.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highest_score(score):
    with open("static/highest_score.txt", "w") as file:
        file.write(str(score))


class Button:
    def __init__(self, text, pos, size, color, hover_color, font, action=None):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.action = action
        self.rect = pygame.Rect(pos, size)
        self.surface = self.font.render(self.text, True, (0, 0, 0))

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, self.hover_color, self.rect)
        else:
            pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.surface, (self.rect.x + (self.rect.width - self.surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - self.surface.get_height()) // 2))
        draw_back_button(window, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, BACK_BUTTON_COLOR)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


class Game:
    def __init__(self, window):
        self.window = window
        self.matrix = [[0] * 4 for _ in range(4)]
        self.cells = []
        self.score = [0, 0]
        self.highest_score = load_highest_score()
        self.fontEngine = pygame.font.SysFont(SCORE_LABEL_FONT, 45)
        self.over = [False, False]
        self.startGame()

    def startGame(self):
        row, col = randint(0, 3), randint(0, 3)
        self.matrix[row][col] = 2
        while self.matrix[row][col] != 0:
            row, col = randint(0, 3), randint(0, 3)
        self.matrix[row][col] = 2

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

        scoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('SCORE:', True, (0, 0, 0))
        scoreRect = scoreSurface.get_rect()
        scoreRect.top = 25
        self.score[1] = [scoreSurface, scoreRect]

    def addNewTile(self):
        row, col = randint(0, 3), randint(0, 3)
        while self.matrix[row][col] != 0:
            row, col = randint(0, 3), randint(0, 3)
        self.matrix[row][col] = choice([2, 2, 2, 2, 4])

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
                    if self.score[0] > self.highest_score:
                        self.highest_score = self.score[0]
                        save_highest_score(self.highest_score)

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
        self.__init__(self.window)


def draw(window, matrix, cells, score, over):
    window.fill(GRID_COLOR)
    window.blit(score[1][0], score[1][1])
    scoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render(str(score[0]), True, (0, 0, 0))
    scoreRect = scoreSurface.get_rect()
    scoreRect.top = 25
    scoreRect.left = score[1][1].right + 10
    window.blit(scoreSurface, scoreRect)

    highest_score_surface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render(f"High Score: {load_highest_score()}", True,
                                                                             (0, 0, 0))
    highest_score_rect = highest_score_surface.get_rect()
    highest_score_rect.top = scoreRect.top + 30
    highest_score_rect.left = scoreRect.right - 180
    window.blit(highest_score_surface, highest_score_rect)

    for i in range(4):
        for j in range(4):
            cell = cells[i][j]

            if (x := matrix[i][j]) != 0:
                pygame.draw.rect(window, CELL_COLORS[x], cell['rect'])
                window.blit(cell['textSurface'], cell['textRect'])
            elif x == 0:
                pygame.draw.rect(window, EMPTY_CELL_COLOR, cell['rect'])
    draw_back_button(window, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, BACK_BUTTON_COLOR)

    # Game Over
    if over[0] and over[1]:
        gameOverSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('2048 Completed. Ctrl + q to reset', True,
                                                                           (0, 0, 0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH // 2, HEIGHT // 2)
        window.blit(gameOverSurface, gameOverRect)
    if over[0] and not over[1]:
        gameOverSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render(
            'No moves left Ctrl + q to reset, Esc to quit', True, (0, 0, 0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH // 2, HEIGHT // 2)
        window.blit(gameOverSurface, gameOverRect)

    pygame.display.update()

def draw(window, matrix, cells, score, over, high_score):
    window.fill("pink")
    window.blit(score[1][0], score[1][1])

    scoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 20).render(str(score[0]), True, (0, 0, 0))
    scoreRect = scoreSurface.get_rect()
    scoreRect.top = 10
    scoreRect.left = score[1][1].right + 10
    window.blit(scoreSurface, scoreRect)

    highScoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 20).render(f'High Score: {high_score}', True, (0, 0, 0))
    highScoreRect = highScoreSurface.get_rect()
    highScoreRect.top = 45
    highScoreRect.left = 20
    window.blit(highScoreSurface, highScoreRect)

    text_surface = create_button2('落子无悔', 150, 450)
    window.blit(text_surface[2], text_surface[1])

    draw_back_button(window, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, BACK_BUTTON_COLOR)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            cell = cells[i][j]

            if (x := matrix[i][j]) != 0:
                pygame.draw.rect(window, CELL_COLORS[x], cell['rect'])
                window.blit(cell['textSurface'], cell['textRect'])
            elif x == 0:
                pygame.draw.rect(window, EMPTY_CELL_COLOR, cell['rect'])

    # Game Over
    if over[0] and over[1]:
        gameOverSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('2048 Completed. Ctrl + q to reset', True, (0, 0, 0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH // 2, HEIGHT // 2)
        window.blit(gameOverSurface, gameOverRect)
    if over[0] and not over[1]:
        gameOverSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('No moves left Ctrl + q to reset, Esc to quit', True, (0, 0, 0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH // 2, HEIGHT // 2)
        window.blit(gameOverSurface, gameOverRect)

    pygame.display.update()
def draw1(window, matrix, cells, score, steps, over):
    window.fill(GRID_COLOR)
    window.blit(score[1][0], score[1][1])
    window.blit(steps[1][0], steps[1][1])
    stepsSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render(str(steps[0]), True, (0, 0, 0))
    stepsRect = stepsSurface.get_rect()
    stepsRect.top = 10
    scoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render(str(score[0]), True, (0, 0, 0))
    scoreRect = scoreSurface.get_rect()
    scoreRect.top = 40
    stepsRect.left = steps[1][1].right + 10
    scoreRect.left = score[1][1].right + 10
    window.blit(scoreSurface, scoreRect)
    window.blit(stepsSurface, stepsRect)

    for i in range(4):
        for j in range(4):
            cell = cells[i][j]

            if (x := matrix[i][j]) != 0:
                pygame.draw.rect(window, CELL_COLORS[x], cell['rect'])
                if cell['textSurface'] is not None:  # 添加此条件检查
                    window.blit(cell['textSurface'], cell['textRect'])
            elif x == 0:
                pygame.draw.rect(window, EMPTY_CELL_COLOR, cell['rect'])
    draw_back_button(window, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, BACK_BUTTON_COLOR)

    # Game Over
    if over[0] and over[1]:
        gameOverSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('2048 Completed. Ctrl + q to next level', True,
                                                                           (0, 0, 0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH // 2, HEIGHT // 2)

        window.blit(gameOverSurface, gameOverRect)

    if over[0] and not over[1]:
        gameOverSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render(
            'No moves left Ctrl + q to reset, Esc to quit', True, (0, 0, 0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH // 2, HEIGHT // 2)
        window.blit(gameOverSurface, gameOverRect)

    pygame.display.update()

def request(username,best_score):
    import requests
    import json

    # 游戏数据
    game_data = {
        'username': username,
        'score': best_score
    }
    # 服务器URL'/submit_score'
    url = 'http://172.24.148.217:8080/submit_score'

    # 将游戏数据序列化为JSON格式
    game_data_json = json.dumps(game_data)
    # 发送POST请求
    response = json.loads(requests.post(url, json=game_data_json, headers={'Content-Type': 'application/json'}).text)
    return response
def tiqu():
    with open("static/username.txt", "r") as file:
            username1=file.read()
    with open("static/highest_score.txt", "r") as file:
            score1=file.read()
    return username1,score1

def draw_ranking(window,data):
    window.fill("pink")
    draw_back_button(window, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, BACK_BUTTON_COLOR)
    # 创建排行榜数据
    rankings = data
    print(rankings)
    # 创建游戏窗口
    pygame.display.set_caption("游戏排行榜")
    # 渲染排行榜
    ranking_text = ""
      # 绘制排行榜
    for index, player in enumerate(rankings):
        rankings=FONT3.render(f'第{index+1}名 : ', True, (0,0,0))
        name = FONT3.render(player["name"], True, (0,0,0))
        score = FONT3.render(str(player["score"]), True, (0,0,0))
        # 确定位置
        rankings_rect = rankings.get_rect(center=(WIDTH//2-150, 20+ index*25))
        name_rect = name.get_rect(center=(WIDTH//2-100, 20+ index*25))
        score_rect = score.get_rect(center=(WIDTH//2 -50, 20 + index*25))
        # 绘制名字和分数
        window.blit(rankings,rankings_rect)
        window.blit(name, name_rect)
        window.blit(score, score_rect)
    pygame.display.update()



def draw_text(screen, text, size, x, y):
    font = pygame.font.SysFont(pygame.font.get_default_font(), size)
    image = font.render(text, True, "yellow")
    rect = image.get_rect()
    rect.center = (x, y)
    screen.blit(image, rect)


def draw_back_button(surface, x, y, width, height, color):
    pygame.draw.rect(surface, color, (x, y, width, height), 2)
    text_surface = pygame.font.SysFont('simhei', 20).render('返回', True, "black")
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    surface.blit(text_surface, text_rect)


def draw_back_button2(surface, x, y, width, height, color):
    pygame.draw.rect(surface, color, (x, y, width, height), 2)
    text_surface = pygame.font.SysFont('simhei', 20).render('返回', True, "white")
    text_rect = text_surface.get_rect(center=( x + width / 2, y +  height / 2))
    surface.blit(text_surface, text_rect)


def create_button1(text, x, y):
    button_rect = pygame.Rect(x, y, 140, 33)
    return button_rect, button_rect, FONT1.render(text, True, 'white')


def create_button2(text, x, y):
    button_rect = pygame.Rect(x, y, 150, 50)
    return button_rect, button_rect, FONT2.render(text, True, 'black')


def create_button3(text, x, y):
    button_rect = pygame.Rect(x, y, 150, 50)
    return button_rect, button_rect, FONT3.render(text, True, 'black')


def start_game(grid_size, high_score):
    running = True
    clock = pygame.time.Clock()
    game = Game2(window, high_score, grid_size)

    while running:
        clock.tick(FPS)

        draw(window, game.matrix, game.cells, game.score, game.over, game.highest_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if BACK_BUTTON_X < mouse_pos[0] < BACK_BUTTON_X + BACK_BUTTON_WIDTH and \
                        BACK_BUTTON_Y < mouse_pos[1] < BACK_BUTTON_Y + BACK_BUTTON_HEIGHT:
                    main()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.left()
                if event.key == pygame.K_RIGHT:
                    game.right()
                if event.key == pygame.K_UP:
                    game.up()
                if event.key == pygame.K_DOWN:
                    game.down()
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL and game.over:
                    game.reset()
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    running = False

def main2():
    running = True

    clock = pygame.time.Clock()
    high_score = 0

    font = pygame.font.SysFont(SCORE_LABEL_FONT, 30)
    buttons = [
        Button("3x3", (50, HEIGHT // 2 - 60), (100, 50), (200, 200, 200), (170, 170, 170), font, lambda: start_game(3, high_score)),
        Button("4x4", (150, HEIGHT // 2 - 60), (100, 50), (200, 200, 200), (170, 170, 170), font, lambda: start_game(4, high_score)),
        Button("5x5", (250, HEIGHT // 2 - 60), (100, 50), (200, 200, 200), (170, 170, 170), font, lambda: start_game(5, high_score)),
    ]

    while running:
        window.fill(GRID_COLOR)
        selectSurface = font.render('Select difficulty:', True, (0, 0, 0))
        draw_back_button(window, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, BACK_BUTTON_COLOR)

        selectRect = selectSurface.get_rect()
        selectRect.center = (WIDTH // 2, HEIGHT // 2 - 100)
        window.blit(selectSurface, selectRect)

        for button in buttons:
            button.draw(window)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if BACK_BUTTON_X < mouse_pos[0] < BACK_BUTTON_X + BACK_BUTTON_WIDTH and \
                        BACK_BUTTON_Y < mouse_pos[1] < BACK_BUTTON_Y + BACK_BUTTON_HEIGHT:
                    main()
            for button in buttons:
                if button.is_clicked(event):
                    return
    pygame.quit()
    quit()


def main():
    running = True
    yy = True
    clock = pygame.time.Clock()
    game = Game(window)
    game1 = Game1(window)
    target_start = True
    game_started = False
    game_started1 = False
    all_sprites = pygame.sprite.Group()
    start_button1 = create_button1("闯关模式", (WIDTH // 2 - 80), (HEIGHT // 2) + 10)
    start_button2 = create_button1("无尽模式", (WIDTH // 2 - 80), (HEIGHT // 2) + 50)
    game_over_button = create_button1("结束游戏", (WIDTH // 2 - 80), (HEIGHT // 2 + 90))
    ranking_button = create_button1("排行榜", (WIDTH // 2 - 80), (HEIGHT // 2 + 130))

#2048动画效果
    if not game_started:
        target1 = Target1(80, 60)
        all_sprites.add(target1)
        target2 = Target2(180, 60)
        all_sprites.add(target2)
        target3 = Target3(80, 150)
        all_sprites.add(target3)
        target4 = Target4(180, 150)
        all_sprites.add(target4)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if BACK_BUTTON_X < mouse_pos[0] < BACK_BUTTON_X + BACK_BUTTON_WIDTH and \
                        BACK_BUTTON_Y < mouse_pos[1] < BACK_BUTTON_Y + BACK_BUTTON_HEIGHT:
                    # 点击了返回按钮，这里你可以根据你的逻辑处理返回
                    pygame.mixer.music.load("static/sounds/bgm.wav")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.Channel(7)
                    pygame.mixer.music.play(-1)  # 参数-1表示循环播放
                    main()
                if start_button2[0].collidepoint(mouse_pos):
                    target_start = False
                    game_started = True
                    main2()

                if start_button1[0].collidepoint(mouse_pos):
                    target_start = False
                    game_started1 = True
                    draw1(window, game1.matrix, game1.cells, game1.score, game1.steps ,game1.over)
                if game_over_button[0].collidepoint(mouse_pos):
                    running = False
                if ranking_button[0].collidepoint(mouse_pos):
                    username=tiqu()[0]
                    score=tiqu()[1]
                    response=request(username,score)
                    draw_ranking(window,response)
                    target_start = False

            if event.type == pygame.KEYUP:
                if game_started:
                    if event.key == pygame.K_LEFT:
                        game.left()
                    if event.key == pygame.K_RIGHT:
                        game.right()
                    if event.key == pygame.K_UP:
                        game.up()
                    if event.key == pygame.K_DOWN:
                        game.down()
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL and game.over:
                        game.reset()
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_w and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        running = False
                if game_started1:
                    if event.key == pygame.K_LEFT:
                        game1.left()
                    if event.key == pygame.K_RIGHT:
                        game1.right()
                    if event.key == pygame.K_UP:
                        game1.up()
                    if event.key == pygame.K_DOWN:
                        game1.down()
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL and game.over:
                        has_next = game1.next_level()
                        if not has_next:
                            yy = False
                        if has_next:
                            game1.reset()
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_w and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        running = False
                    if not yy:
                        game_started1 = False
                        pygame.mixer.music.load("static/sounds/success.wav")
                        pygame.mixer.music.set_volume(0.1)
                        pygame.mixer.music.play()  # 参数-1表示循环播放
                        window.fill("black")
                        draw_text(window, "Win!", 200, WIDTH / 2, HEIGHT / 2)
                        draw_back_button2(window, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT,
                                         BACK_BUTTON_COLOR)
                pygame.display.flip()

        # 根据 target_start 的状态决定绘制哪个按钮
        if target_start:
            window.blit(background_image, (0, 0))
            all_sprites.update()
            all_sprites.draw(window)
            text_surface1 = create_button2('制作人员：', 250, 30)  # 渲染中文文本
            text_surface2 = create_button3('计算2301 陈柏廷', 250, 60)  # 渲染中文文本
            text_surface3 = create_button3('计算2301(国际) 大鹏', 250, 80)  # 渲染中文文本
            text_surface4 = create_button3('计算2301(国际) HNIN YU', 250, 100)
            text_surface5 = create_button3('计算2302 马江龙', 250, 120)
            text_surface6 = create_button3('计算2302 成宝骏', 250, 140)  # 渲染中文文本

            window.blit(text_surface1[2],text_surface1[1])
            window.blit(text_surface2[2], text_surface2[1])
            window.blit(text_surface3[2], text_surface3[1])
            window.blit(text_surface4[2], text_surface4[1])
            window.blit(text_surface5[2], text_surface5[1])
            window.blit(text_surface6[2], text_surface6[1])
            window.blit(ranking_button[2], ranking_button[1])

            window.blit(start_button1[2], start_button1[1])
            window.blit(start_button2[2], start_button2[1])

            window.blit(game_over_button[2], game_over_button[1])
            pygame.display.flip()

        # ...绘制其他游戏元素...

        if game_started1:
            draw1(window, game1.matrix, game1.cells, game1.score,game1.steps, game1.over)

    pygame.quit()
if __name__ == "__main__":
    main()
