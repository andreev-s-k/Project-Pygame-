import random

import pygame
# import random
import ctypes

user32 = ctypes.windll.user32

knight_lvl = 1

lvl_change = True

exp = 0

max_exp = 10 * knight_lvl

f = open("Card/score.txt", encoding="utf8")
for i in range(1):
    max_score = f.readline()
    print(max_score)
f.close()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Card game')
    size = width, height = user32.GetSystemMetrics(0) // 3, user32.GetSystemMetrics(1) - 140
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill((40, 40, 40))
    all_sprites = pygame.sprite.Group()
    player_move = False
    score = money = 0

    class Board:
        # создание поля
        def __init__(self, b_width, b_height):
            self.width = b_width
            self.height = b_height
            self.board = [['1'] * b_width for _ in range(b_height)]
            self.board[1][1] = '1'
            # значения по умолчанию
            self.left = 10
            self.top = 10
            self.cell_size_x = 30
            self.cell_size_y = 50

        # настройка внешнего вида
        def set_view(self, left, top, cell_size_x, cell_size_y):
            self.left = left
            self.top = top
            self.cell_size_x = cell_size_x
            self.cell_size_y = cell_size_y

        def render(self, sc):
            for i1 in range(len(self.board)):
                for j1 in range(len(self.board[i])):

                    if isinstance(self.board[i1][j1], Coin):
                        sc.fill(pygame.Color((90, 90, 90)), pygame.Rect(self.left + (self.board[i1][j1].cell[0]
                                                                                     * self.cell_size_x)
                                                                        + 4,
                                                                        self.top + (self.board[i1][j1].cell[1]
                                                                                    * self.cell_size_y)
                                                                        + self.board[i1][j1].y - 126,
                                                                        self.cell_size_x - 8, self.cell_size_y - 8))

                    if isinstance(self.board[i1][j1], Potion):
                        sc.fill(pygame.Color((90, 90, 90)), pygame.Rect(self.left + (j1 * self.cell_size_x) + 4,
                                                                        self.top + (i1 * self.cell_size_y) + 4,
                                                                        self.cell_size_x - 8, self.cell_size_y - 8))

                    if isinstance(self.board[i1][j1], Monster):
                        sc.fill(pygame.Color((90, 90, 90)), pygame.Rect(self.left + (j1 * self.cell_size_x) + 4,
                                                                        self.top + (i1 * self.cell_size_y) + 4,
                                                                        self.cell_size_x - 8, self.cell_size_y - 8))

                    if isinstance(self.board[i1][j1], Weapon):
                        sc.fill(pygame.Color((90, 90, 90)), pygame.Rect(self.left + (j1 * self.cell_size_x) + 4,
                                                                        self.top + (i1 * self.cell_size_y) + 4,
                                                                        self.cell_size_x - 8, self.cell_size_y - 8))

                    if self.board[i1][j1] == 'player':
                        sc.fill(pygame.Color((90, 90, 90)),
                                pygame.Rect(self.left + ((player.cell[0] - 1) * self.cell_size_x) + player.player_x,
                                            self.top + ((player.cell[1] - 1) * self.cell_size_y) + player.player_y,
                                            self.cell_size_x - 8, self.cell_size_y - 8))

        def get_click(self, mouse_pos):
            cell = self.get_cell(mouse_pos)
            print(self.get_cell(mouse_pos))
            self.on_click(cell)

        def get_cell(self, mouse_pos):

            if ((mouse_pos[0] - self.left) // self.cell_size_x >= self.width
                    or (mouse_pos[1] - self.top) // self.cell_size_y >= self.height) \
                    or (mouse_pos[0] - self.left) // self.cell_size_x < 0.0 \
                    or (mouse_pos[1] - self.top) // self.cell_size_y < 0.0:
                return ''
            else:
                return (int((mouse_pos[0] - self.left) // self.cell_size_x) + 1,
                        int((mouse_pos[1] - self.top) // self.cell_size_y) + 1)

        def on_click(self, cell):
            print(self.board)

            player.move(cell)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            global knight_lvl
            self.cell = (2, 2)
            self.health = (knight_lvl * 2) + 8
            self.weapon = 0
            self.max_health = self.health
            self.image = pygame.image.load('Card/Texture/Knight_idle_anim_f0.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (width // 4, height // 5.5))
            self.rect = self.image.get_rect()
            self.rect.center = (width // 2.15, height // 1.8)
            self.font = pygame.font.Font(None, 30)
            self.health_text = self.font.render(str(self.health) + '/' + str(self.max_health), True, [255, 000, 000])
            self.weapon_text = self.font.render(str(self.weapon), True, [255, 255, 255])
            self.player_x = 4
            self.player_y = 4
            self.heart = Heart()
            self.move_cell = self.cell
            self.health_text_pos = (((self.cell[0]) * board.cell_size_x) + self.player_x - 30,
                                    ((self.cell[1]) * board.cell_size_y) + self.player_y - 140)
            self.weapon_text_pos = (((self.cell[0]) * board.cell_size_x) + self.player_x + 10,
                                    ((self.cell[1]) * board.cell_size_y) + self.player_y + 40)

        def move(self, cell):
            global player_move
            print('self.cell, cell, self.move_cell', self.cell, cell, self.move_cell)
            if cell != '':

                if cell[0] == self.cell[0] and cell[1] == self.cell[1] + 1 and not player_move:
                    self.move_cell = cell
                    player_move = True
                if cell[0] == self.cell[0] and cell[1] == self.cell[1] - 1 and not player_move:
                    self.move_cell = cell
                    player_move = True
                if cell[0] == self.cell[0] - 1 and cell[1] == self.cell[1] and not player_move:
                    self.move_cell = cell
                    player_move = True
                if cell[0] == self.cell[0] + 1 and cell[1] == self.cell[1] and not player_move:
                    self.move_cell = cell
                    player_move = True

        def update(self):
            global exp, max_exp, knight_lvl
            if exp >= max_exp and not game_over:
                knight_lvl += 1
                exp -= max_exp
                max_exp = knight_lvl * 10
                self.max_health = (knight_lvl * 2) + 8
                self.health = self.max_health
                if lvl_change:
                    self.cell = (2, 2)
                    self.rect.center = (width // 2.15, height // 1.8)
                    self.health_text_pos = (((self.cell[0]) * board.cell_size_x) + self.player_x - 30,
                                            ((self.cell[1]) * board.cell_size_y) + self.player_y - 140)
                    self.weapon_text_pos = (((self.cell[0]) * board.cell_size_x) + self.player_x + 10,
                                            ((self.cell[1]) * board.cell_size_y) + self.player_y + 40)
                    self.heart.rect.center = ((width // 2) + 50, (height // 2.1) - 10)
                    board.board = [['1'] * board.width for _ in range(board.height)]
                    board.board[1][1] = 'player'
                    for i2 in all_sprites:
                        if not isinstance(i2, Player):
                            i2.rect.center = (-1000, -1000)
                    for i2 in range(len(board.board)):
                        for j2 in range(len(board.board[i])):
                            if board.board[i2][j2] != 'player' and board.board[i2][j2] != 'blank':
                                board.board[i2][j2] = random.choice(['coin', 'potion', 'monster', 'weapon'])
                            if board.board[i2][j2] == 'coin':
                                board.board[i2][j2] = Coin((j2, i2))
                                all_sprites.add(board.board[i2][j2])
                            if board.board[i2][j2] == 'potion':
                                board.board[i2][j2] = Potion((j2, i2))
                                all_sprites.add(board.board[i2][j2])
                            if board.board[i2][j2] == 'monster':
                                board.board[i2][j2] = Monster((j2, i2))
                                all_sprites.add(board.board[i2][j2])
                            if board.board[i2][j2] == 'weapon':
                                board.board[i2][j2] = Weapon((j2, i2))
                                all_sprites.add(board.board[i2][j2])

    class Heart(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('Card/Texture/heart.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (width // 20, height // 25))
            self.rect = self.image.get_rect()
            self.rect.center = ((width // 2) + 50, (height // 2.1) - 10)

        def update(self):
            pass

    class Coin(pygame.sprite.Sprite):
        def __init__(self, cell):
            pygame.sprite.Sprite.__init__(self)
            self.cell = cell
            self.image = pygame.image.load('Card/Texture/coin4.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (width // 6, height // 8))
            self.rect = self.image.get_rect()
            self.x = 90
            self.y = 130
            self.cost = random.randrange(1, 11)
            self.rect.center = (board.left + (self.cell[0] * board.cell_size_x) + self.x,
                                board.top + (self.cell[1] * board.cell_size_y) + self.y)
            self.font = pygame.font.Font(None, 30)
            self.cost_text = self.font.render(str(self.cost), True, [255, 200, 000])
            self.cost_text_pos = (width // 5, height // 2)
            self.move = False
            print(self.cell[1])

        def update(self):
            if 0 <= self.cell[1] < 2 and self.cell[0] >= 0:
                pass
            if 0 <= self.cell[1] < 2 and self.cell[0] >= 0 and board.board[self.cell[1] + 1][self.cell[0]] == 'blank':
                self.move = True

    class Potion(pygame.sprite.Sprite):
        def __init__(self, cell):
            pygame.sprite.Sprite.__init__(self)
            self.cell = cell
            self.image = pygame.image.load(random.choice(['Card/Texture/potion_01.png',
                                                          'Card/Texture/potion_02.png',
                                                          'Card/Texture/potion_03.png',
                                                          'Card/Texture/potion_04.png',
                                                          'Card/Texture/potion_05.png',
                                                          'Card/Texture/potion_06.png'])).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width // 6, height // 8))
            self.rect = self.image.get_rect()
            self.x = 90
            self.y = 130
            self.cost = random.randrange(1, player.max_health // 2)
            self.rect.center = (board.left + (self.cell[0] * board.cell_size_x) + self.x,
                                board.top + (self.cell[1] * board.cell_size_y) + self.y)
            self.font = pygame.font.Font(None, 30)
            self.cost_text = self.font.render(str(self.cost), True, [000, 200, 255])
            self.cost_text_pos = (width // 5, height // 2)
            self.move = False
            print(self.cell[1])

        def update(self):
            if 0 <= self.cell[1] < 2 and self.cell[0] >= 0:
                pass
            if 0 <= self.cell[1] < 2 and self.cell[0] >= 0 and board.board[self.cell[1] + 1][self.cell[0]] == 'blank':
                self.move = True

    class Monster(pygame.sprite.Sprite):
        def __init__(self, cell):
            pygame.sprite.Sprite.__init__(self)
            self.cell = cell
            self.image = pygame.image.load(random.choice(['Card/Texture/goblin.png',
                                                          'Card/Texture/slime.png'])).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width // 6, height // 8))
            self.rect = self.image.get_rect()
            self.x = 90
            self.y = 130
            self.cost = random.randrange(1, 10)
            self.start_cost = self.cost
            self.rect.center = (board.left + (self.cell[0] * board.cell_size_x) + self.x,
                                board.top + (self.cell[1] * board.cell_size_y) + self.y)
            self.font = pygame.font.Font(None, 30)
            self.cost_text = self.font.render(str(self.cost), True, [255, 200, 000])
            self.cost_text_pos = (width // 5, height // 2)
            self.move = False
            print(self.cell[1])

        def update(self):
            if 0 <= self.cell[1] < 2 and self.cell[0] >= 0:
                pass
            if 0 <= self.cell[1] < 2 and self.cell[0] >= 0 and board.board[self.cell[1] + 1][self.cell[0]] == 'blank':
                self.move = True

    class Weapon(pygame.sprite.Sprite):
        def __init__(self, cell):
            pygame.sprite.Sprite.__init__(self)
            self.cell = cell
            self.image = pygame.image.load(random.choice(['Card/Texture/sword1.png',
                                                          'Card/Texture/sword2.png',
                                                          'Card/Texture/sword3.png',
                                                          'Card/Texture/sword4.png'])).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width // 6, height // 8))
            self.rect = self.image.get_rect()
            self.x = 90
            self.y = 130
            self.cost = random.randrange(1, 11)
            self.rect.center = (board.left + (self.cell[0] * board.cell_size_x) + self.x,
                                board.top + (self.cell[1] * board.cell_size_y) + self.y)
            self.font = pygame.font.Font(None, 30)
            self.cost_text = self.font.render(str(self.cost), True, [255, 200, 000])
            self.cost_text_pos = (width // 5, height // 2)
            self.move = False
            print(self.cell[1])

        def update(self):
            if 0 <= self.cell[1] < 2 and self.cell[0] >= 0:
                pass
            if 0 <= self.cell[1] < 2 and self.cell[0] >= 0 and board.board[self.cell[1] + 1][self.cell[0]] == 'blank':
                self.move = True
            # if self.cell[0] < 2 and board.board[self.cell[1]][self.cell[0] + 1] == 'blank':
                # self.move = True


    board = Board(3, 3)
    board.set_view(width // 14, height // 9, width // 3.5, height // 3.5)
    player = Player()
    all_sprites.add(player)
    all_sprites.add(player.heart)
    board.board[1][1] = 'player'
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if board.board[i][j] != 'player' and board.board[i][j] != 'blank':
                board.board[i][j] = random.choice(['coin', 'potion', 'monster', 'weapon'])
            if board.board[i][j] == 'coin':
                board.board[i][j] = Coin((j, i))
                all_sprites.add(board.board[i][j])
            if board.board[i][j] == 'potion':
                board.board[i][j] = Potion((j, i))
                all_sprites.add(board.board[i][j])
            if board.board[i][j] == 'monster':
                board.board[i][j] = Monster((j, i))
                all_sprites.add(board.board[i][j])
            if board.board[i][j] == 'weapon':
                board.board[i][j] = Weapon((j, i))
                all_sprites.add(board.board[i][j])
    game_over = False
    menu_open = False
    font_1 = pygame.font.Font(None, 80)
    font_2 = pygame.font.Font(None, 20)
    game_over_text = font_1.render('GAME OVER', True, [255, 000, 000])
    game_over_text_pos = (width // 5, height // 2)
    score_text = font_1.render(str(money), True, [255, 20, 000])
    score_text_pos = (width - 150, 30)
    max_score_text = font_1.render('Лучший счет: ' + str(max_score), True, [230, 20, 50])
    max_score_text_pos = (width // 5 - 30, height // 2 + 120)
    exp_text = font_1.render(str(exp) + '/' + (str(max_exp)), True, [5, 0, 255])
    exp_text_pos = (80, 30)

    running = True
    while running:
        player.health_text = player.font.render(str(player.health) + '/' + str(player.max_health),
                                                True, [255, 100, 100])
        player.weapon_text = player.font.render(str(player.weapon), True, [255, 255, 255])
        score_text = font_1.render(str(score), True, [255, 200, 000])
        exp_text = font_1.render(str(exp) + '/' + (str(max_exp)), True, [90, 90, 255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and not menu_open:
                    board.get_click(event.pos)
                if game_over:
                    print('gg')
                    player.cell = (2, 2)
                    player.rect.center = (width // 2.15, height // 1.8)
                    player.health_text_pos = (((player.cell[0]) * board.cell_size_x) + player.player_x - 30,
                                              ((player.cell[1]) * board.cell_size_y) + player.player_y - 140)
                    player.weapon_text_pos = (((player.cell[0]) * board.cell_size_x) + player.player_x + 10,
                                              ((player.cell[1]) * board.cell_size_y) + player.player_y + 40)
                    player.heart.rect.center = ((width // 2) + 50, (height // 2.1) - 10)
                    board.board = [['1'] * board.width for _ in range(board.height)]
                    board.board[1][1] = 'player'
                    for i in all_sprites:
                        if not isinstance(i, Player):
                            i.rect.center = (-1000, -1000)
                    for i in range(len(board.board)):
                        for j in range(len(board.board[i])):
                            if board.board[i][j] != 'player' and board.board[i][j] != 'blank':
                                board.board[i][j] = random.choice(['coin', 'potion', 'monster', 'weapon'])
                            if board.board[i][j] == 'coin':
                                board.board[i][j] = Coin((j, i))
                                all_sprites.add(board.board[i][j])
                            if board.board[i][j] == 'potion':
                                board.board[i][j] = Potion((j, i))
                                all_sprites.add(board.board[i][j])
                            if board.board[i][j] == 'monster':
                                board.board[i][j] = Monster((j, i))
                                all_sprites.add(board.board[i][j])
                            if board.board[i][j] == 'weapon':
                                board.board[i][j] = Weapon((j, i))
                                all_sprites.add(board.board[i][j])
                    knight_lvl = 1
                    exp = 0
                    max_exp = knight_lvl * 10
                    player.max_health = (knight_lvl * 2) + 8
                    player.health = player.max_health
                    player.health = player.max_health
                    score = 0
                    game_over = False
                # mouse_pos = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    pass
        if player_move:
            if isinstance(board.board[player.move_cell[1] - 1][player.move_cell[0] - 1], Coin):
                score += board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell = (-10, -10)
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].rect.center = \
                    (board.left + (board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell[0]
                                   * board.cell_size_x) + 90,
                        board.top + (board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell[1]
                                     * board.cell_size_y) + 130)
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1] = 0

            if isinstance(board.board[player.move_cell[1] - 1][player.move_cell[0] - 1], Monster):
                if player.weapon > 0:
                    weapon = player.weapon
                    if board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost > 0:
                        player.weapon -= board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost
                    board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost -= weapon
                    player_move = False
                else:
                    player.health -= board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost
                    board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost = 0
                if board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost <= 0:
                    exp += board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].start_cost
                    board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell = (-10, -10)
                    board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].rect.center = \
                        (board.left + (board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell[0]
                                       * board.cell_size_x) + 90,
                         board.top + (board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell[1]
                                      * board.cell_size_y) + 130)
                    board.board[player.move_cell[1] - 1][player.move_cell[0] - 1] = 'coin'

            if isinstance(board.board[player.move_cell[1] - 1][player.move_cell[0] - 1], Potion):
                if player.health < player.max_health:
                    player.health += board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost
                    if player.health > player.max_health:
                        player.health = player.max_health
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell = (-10, -10)
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].rect.center = \
                    (board.left + (board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell[0]
                                   * board.cell_size_x) + 90,
                     board.top + (board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell[1]
                                  * board.cell_size_y) + 130)
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1] = 0

            if isinstance(board.board[player.move_cell[1] - 1][player.move_cell[0] - 1], Weapon):
                player.weapon = board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cost
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell = (-10, -10)
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].rect.center = \
                    (board.left + (board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell[0]
                                   * board.cell_size_x) + 90,
                     board.top + (board.board[player.move_cell[1] - 1][player.move_cell[0] - 1].cell[1]
                                  * board.cell_size_y) + 130)
                board.board[player.move_cell[1] - 1][player.move_cell[0] - 1] = 0

            if player.move_cell[0] == player.cell[0] and player.move_cell[1] == player.cell[1] + 1:
                if board.top + (player.move_cell[1] * board.cell_size_y) + 4 > board.top \
                        + ((player.cell[1]) * board.cell_size_y) + player.player_y:
                    player.player_y += 1
                    player.rect.center = (player.rect.center[0], player.rect.center[1] + 1)
                    player.health_text_pos = (player.health_text_pos[0], player.health_text_pos[1] + 1)
                    player.weapon_text_pos = (player.weapon_text_pos[0], player.weapon_text_pos[1] + 1)
                    player.heart.rect.center = (player.heart.rect.center[0], player.heart.rect.center[1] + 1)
                else:
                    player_move = False
                    if board.board[player.cell[1] - 1][player.cell[0] - 1] == 'player':
                        board.board[player.cell[1] - 1][player.cell[0] - 1] = 'blank'
                    player.cell = player.move_cell
                    player.player_y = 4
                    if board.board[player.cell[1] - 1][player.cell[0] - 1] != 'player':
                        board.board[player.cell[1] - 1][player.cell[0] - 1] = 'player'

            if player.move_cell[0] == player.cell[0] and player.move_cell[1] == player.cell[1] - 1:
                if board.top + (player.move_cell[1] * board.cell_size_y) + 4 < board.top \
                        + ((player.cell[1]) * board.cell_size_y) + player.player_y:
                    player.player_y -= 1
                    player.rect.center = (player.rect.center[0], player.rect.center[1] - 1)
                    player.health_text_pos = (player.health_text_pos[0], player.health_text_pos[1] - 1)
                    player.weapon_text_pos = (player.weapon_text_pos[0], player.weapon_text_pos[1] - 1)
                    player.heart.rect.center = (player.heart.rect.center[0], player.heart.rect.center[1] - 1)
                else:
                    if board.board[player.cell[1] - 1][player.cell[0] - 1] == 'player':
                        board.board[player.cell[1] - 1][player.cell[0] - 1] = 'blank'
                    player.cell = player.move_cell
                    player_move = False
                    player.player_y = 4
                    if board.board[player.cell[1] - 1][player.cell[0] - 1] != 'player':
                        board.board[player.cell[1] - 1][player.cell[0] - 1] = 'player'

            if player.move_cell[0] == player.cell[0] - 1 and player.move_cell[1] == player.cell[1]:
                if board.left + (player.move_cell[0] * board.cell_size_x) + 4 < board.left \
                        + ((player.cell[0]) * board.cell_size_x) + player.player_x:
                    player.player_x -= 1
                    player.rect.center = (player.rect.center[0] - 1, player.rect.center[1])
                    player.health_text_pos = (player.health_text_pos[0] - 1, player.health_text_pos[1])
                    player.weapon_text_pos = (player.weapon_text_pos[0] - 1, player.weapon_text_pos[1])
                    player.heart.rect.center = (player.heart.rect.center[0] - 1, player.heart.rect.center[1])
                else:
                    if board.board[player.cell[1] - 1][player.cell[0] - 1] == 'player':
                        board.board[player.cell[1] - 1][player.cell[0] - 1] = 'blank'
                    player.cell = player.move_cell
                    player_move = False
                    player.player_x = 4
                    if board.board[player.cell[1] - 1][player.cell[0] - 1] != 'player':
                        board.board[player.cell[1] - 1][player.cell[0] - 1] = 'player'

            if player.move_cell[0] == player.cell[0] + 1 and player.move_cell[1] == player.cell[1]:
                if board.left + (player.move_cell[0] * board.cell_size_x) + 4 > board.left \
                        + ((player.cell[0]) * board.cell_size_x) + player.player_x:
                    player.player_x += 1
                    player.rect.center = (player.rect.center[0] + 1, player.rect.center[1])
                    player.health_text_pos = (player.health_text_pos[0] + 1, player.health_text_pos[1])
                    player.weapon_text_pos = (player.weapon_text_pos[0] + 1, player.weapon_text_pos[1])
                    player.heart.rect.center = (player.heart.rect.center[0] + 1, player.heart.rect.center[1])
                else:
                    if board.board[player.cell[1] - 1][player.cell[0] - 1] == 'player':
                        board.board[player.cell[1] - 1][player.cell[0] - 1] = 'blank'
                    player.cell = player.move_cell
                    player_move = False
                    player.player_x = 4
                    if board.board[player.cell[1] - 1][player.cell[0] - 1] != 'player':
                        board.board[player.cell[1] - 1][player.cell[0] - 1] = 'player'
        else:
            all_sprites.update()
        for i in range(len(board.board)):
            for j in range(len(board.board[i])):
                if isinstance(board.board[i][j], Coin) or isinstance(board.board[i][j], Potion) \
                        or isinstance(board.board[i][j], Monster) or isinstance(board.board[i][j], Weapon):
                    if board.board[i][j].move:
                        if i < 2 and board.board[i + 1][j] == 'blank':
                            if (board.top + (board.board[i][j].cell[1] * board.cell_size_y) + board.board[i][j].y) \
                                < (board.top + ((board.board[i][j].cell[1] + 1) * board.cell_size_y)
                                   + 4):
                                board.board[i][j].y += 1
                                board.board[i][j].rect.center = (board.board[i][j].rect.center[0],
                                                                 board.board[i][j].rect.center[1] + 2)
                            else:
                                obj = board.board[i][j]
                                print('obj', obj)
                                board.board[i][j].move = False
                                board.board[i][j].y = 130
                                print(board.board[i][j].y)
                                board.board[i + 1][j] = board.board[i][j]
                                board.board[i][j] = 'blank'
                                board.board[i + 1][j].cell = (board.board[i + 1][j].cell[0],
                                                              board.board[i + 1][j].cell[1] + 1)
        for i in range(len(board.board)):
            for j in range(len(board.board[i])):
                if board.board[0][j] == 'blank':
                    board.board[i][j] = random.choice(['coin', 'coin', 'potion', 'monster', 'monster', 'weapon',
                                                       'monster'])
                if i > 0 and board.board[i][j] == 'blank' and board.board[i - 1][j] == 'player':
                    board.board[i][j] = random.choice(['coin', 'coin', 'potion', 'monster', 'monster', 'weapon',
                                                       'monster'])
                if board.board[i][j] == 'coin':
                    board.board[i][j] = Coin((j, i))
                    all_sprites.add(board.board[i][j])
                if board.board[i][j] == 'potion':
                    board.board[i][j] = Potion((j, i))
                    all_sprites.add(board.board[i][j])
                if board.board[i][j] == 'monster':
                    board.board[i][j] = Monster((j, i))
                    all_sprites.add(board.board[i][j])
                if board.board[i][j] == 'weapon':
                    board.board[i][j] = Weapon((j, i))
                    all_sprites.add(board.board[i][j])
        screen.fill((60, 60, 60))
        board.render(screen)
        all_sprites.draw(screen)
        screen.blit(player.health_text, player.health_text_pos)
        if player.weapon > 0:
            screen.blit(player.weapon_text, player.weapon_text_pos)
        screen.blit(score_text, score_text_pos)
        screen.blit(exp_text, exp_text_pos)
        for i in range(len(board.board)):
            for j in range(len(board.board[i])):
                if isinstance(board.board[i][j], Coin) or isinstance(board.board[i][j], Potion):
                    board.board[i][j].cost_text = board.board[i][j].font.render(str(board.board[i][j].cost),
                                                                                True, [255, 200, 000])
                    board.board[i][j].cost_text_pos = \
                        (board.left + (board.board[i][j].cell[0] * board.cell_size_x) + 4 + board.board[i][j].x + 50,
                         (board.top + ((board.board[i][j].cell[1] + 1) * board.cell_size_y
                                       + board.board[i][j].y - 360)))
                    screen.blit(board.board[i][j].cost_text, board.board[i][j].cost_text_pos)
                if isinstance(board.board[i][j], Potion):
                    board.board[i][j].cost_text = board.board[i][j].font.render(str(board.board[i][j].cost),
                                                                                True, [000, 200, 255])
                    board.board[i][j].cost_text_pos = \
                        (board.left + (board.board[i][j].cell[0] * board.cell_size_x) + 4 + board.board[i][j].x + 50,
                         (board.top + ((board.board[i][j].cell[1] + 1) * board.cell_size_y
                                       + board.board[i][j].y - 360)))
                    screen.blit(board.board[i][j].cost_text, board.board[i][j].cost_text_pos)
                if isinstance(board.board[i][j], Monster):
                    board.board[i][j].cost_text = board.board[i][j].font.render(str(board.board[i][j].cost),
                                                                                True, [255, 000, 000])
                    board.board[i][j].cost_text_pos = \
                        (board.left + (board.board[i][j].cell[0] * board.cell_size_x) + 4 + board.board[i][j].x + 50,
                         (board.top + ((board.board[i][j].cell[1] + 1) * board.cell_size_y
                                       + board.board[i][j].y - 360)))
                    screen.blit(board.board[i][j].cost_text, board.board[i][j].cost_text_pos)
                if isinstance(board.board[i][j], Weapon):
                    board.board[i][j].cost_text = board.board[i][j].font.render(str(board.board[i][j].cost),
                                                                                True, [255, 255, 255])
                    board.board[i][j].cost_text_pos = \
                        (board.left + (board.board[i][j].cell[0] * board.cell_size_x) + 4 + board.board[i][j].x + 50,
                         (board.top + ((board.board[i][j].cell[1] + 1) * board.cell_size_y
                                       + board.board[i][j].y - 360)))
                    screen.blit(board.board[i][j].cost_text, board.board[i][j].cost_text_pos)
        if player.health <= 0:
            game_over = True
            screen.blit(game_over_text, game_over_text_pos)
            screen.blit(score_text, score_text_pos)
            screen.blit(max_score_text, max_score_text_pos)
            if score >= int(max_score):
                max_score = score
                max_score_text = font_1.render('Лучший счет: ' + str(max_score), True, [230, 20, 50])
                f = open("Card/score.txt", 'w')
                f.write(str(score))
                f.close()
        pygame.display.flip()
    pygame.quit()
