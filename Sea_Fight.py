import math

import pygame as pg
from random import choice

pg.init()


class Game:
    # Инициализация игры, по умолчанию размер игрового поля - 10 на 10
    def __init__(self, is_debugging, screen_size=(500, 700)):
        self.color = (120, 228, 211)
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.screen = pg.display.set_mode(screen_size)
        self.screen.fill(self.color)
        pg.display.set_caption('Морской бой v1.01')
        # В этом списке будут храниться экземпляры кораблей
        self.ships = []
        # Этот список будет представлять игровое поле
        self.field = [['-' for col in range(10)] for row in range(10)]
        self.cell_map = [[FieldCell(self, row, col) for col in range(10)] for row in range(10)]
        # Эта переменная отвечает за главный цикл игры
        self.running = True
        # Это список хранит данные, введеные пользователем -> | строка | столбец | есть попадание | корабль уничтожен |
        self.aim = [0, 0, False, False]
        # free_zone - список того же размера, что и игровое поле, заполненный единицами
        # Он используется алгоритмом случайной расстановки кораблей
        # 1 - в списке означает, что ячейка свободна для помещения в нее корабельной ячейки
        self.free_zone = [['1' for col in range(10)] for row in range(10)]
        # Настройка игрового текста
        self.title_font = pg.font.Font('FreePixel.ttf', 30)
        self.input_font = pg.font.Font('FreePixel.ttf', 25)
        self.font_color = (48, 68, 63)
        self.font_back_color = (170, 255, 253)
        self.title = self.title_font.render('Морской Бой v1.01', False, self.font_color, self.font_back_color)
        self.label_one = self.input_font.render('Выбирай клетки, чтобы делать ходы', False,
                                                self.font_color, self.font_back_color)
        self.label_two = self.input_font.render('', False, self.font_color, self.font_back_color)
        self.label_three = self.input_font.render('', False, self.font_color, self.font_back_color)
        # Расстановка 10 кораблей
        for i_size in [4, 3, 2, 1]:
            for i_num in range(5-i_size):
                t_ship = Ship(self, i_size)
                self.ships.append(t_ship)
                self.place_ship(t_ship)
        # Показывает положение кораблей если игра запущена в режиме отладки
        if is_debugging:
            for ship in self.ships:
                for cell in ship.cells:
                    self.cell_map[cell.r][cell.c].state = 'mark'

    # Эта функция выводит игровое поле на экран
    def show_map(self):
        self.screen.fill(self.color)
        for row in self.cell_map:
            for col in row:
                col.draw()
        self.screen.blit(self.title, (self.width/2-125, 15))
        self.screen.blit(self.label_one, (25, 55))
        self.screen.blit(self.label_two, (25, 95))
        self.screen.blit(self.label_three, (25, 135))
        pg.display.flip()

    # Эта функция проверяет, может ли игрок сделать выстрел в точку с заданными координатами
    # Возвращает True если может и False если не может
    def can_hit(self):
        for ship in self.ships:
            for cell in ship.cells:
                # Для каждой клетки каждого корабля функция проверяет
                # Совпадают ли введеные координаты с координатами клетки
                if [self.aim[0], self.aim[1]] == [cell.r, cell.c]:
                    # Затем в случае если клетка еще не тронута (т.е. в целом состоянии)
                    if cell.state:
                        # Ставит значение "есть попадание" на True
                        self.aim[2] = True
                        # А значение состояния самой клетки ставит на False
                        cell.state = False
                        # Затем также проверяет если эта клетка была последней для корабля
                        if ship.is_drown():
                            self.aim[3] = True
                        return True
        # Если же никакой корабль не задет, значения "есть попадание" и "корабль уничтожен" становятся равны False
        self.aim[2], self.aim[3] = False, False
        # И если клетка игрового поля еще не была затронута возвращает True иначе False
        if self.cell_map[self.aim[0]][self.aim[1]].state == 'default':
            return True
        else:
            return False

    # Функция выводит результат хода, и вводит изменения на карту
    def make_move(self):
        if self.aim[2]:
            self.label_two = self.input_font.render('Есть попадание!', False, self.font_color, self.font_back_color)
            self.label_three = self.input_font.render('', False, self.font_color, self.font_back_color)
            self.cell_map[self.aim[0]][self.aim[1]].state = 'hit'
            if self.aim[3]:
                self.label_three = self.input_font.render('Корабль уничтожен!', False,
                                                          self.font_color, self.font_back_color)
                self.cell_map[self.aim[0]][self.aim[1]].state = 'destroyed'
        else:
            self.label_two = self.input_font.render('Промах!', False, self.font_color, self.font_back_color)
            self.label_three = self.input_font.render('', False, self.font_color, self.font_back_color)
            self.cell_map[self.aim[0]][self.aim[1]].state = 'missed'

    # Функция проверки условия окончания игры
    def check_win(self):
        # В этот список будут собираться значения состояний ВСЕХ корабельных ячеек
        have_ship_list = []
        for ship in self.ships:
            for cell in ship.cells:
                have_ship_list.append(cell.state)
        # Затем если в списке нет значений True
        # Главный игровой цикл прекращается
        if True not in have_ship_list:
            self.label_one = self.input_font.render('Флот противника уничтожен! Победа!', False,
                                                    self.font_color, self.font_back_color)
            self.label_two = self.input_font.render('', False, self.font_color, self.font_back_color)
            self.label_three = self.input_font.render('', False, self.font_color, self.font_back_color)

    # Это функция ставит в случайном месте 1 корабль с заданным
    def place_ship(self, ship):
        # Сначала она собирает список координат точек списка free_zone со значением 1 т.е. свободных
        free_zone_cells = []
        for row in range(len(self.field)):
            for col in range(len(self.field)):
                if self.free_zone[row][col]:
                    free_zone_cells.append([row, col])
        # Затем выбирает пару координат случайным образом из списка
        pair = choice(free_zone_cells)
        # Затем, отталкиваясь от расположения ячейки, отсеивает возможные варианты расположения
        variants = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        if pair[0] < ship.size - 1:
            variants.remove([-1, 0])
        if pair[1] < ship.size - 1:
            variants.remove([0, -1])
        if 9 - pair[0] < ship.size - 1:
            variants.remove([1, 0])
        if 9 - pair[1] < ship.size - 1:
            variants.remove([0, 1])
        # Если вариантов расположения и вовсе не осталось, он снова выбирает новую ячейку
        if len(variants) == 0:
            self.place_ship(ship)
        # Если же вариант расположения есть, то он выбирает случайный из них и использует
        else:
            xy_step = choice(variants)
            step = 0
            # Если конечная ячейка свободна на карте free_zone прокладывает остальные до нее
            if self.free_zone[pair[0] + xy_step[0]*(len(ship.cells)-1)][pair[1] + xy_step[1]*(len(ship.cells)-1)]:
                for cell in ship.cells:
                    cell.r = pair[0] + xy_step[0]*step
                    cell.c = pair[1] + xy_step[1]*step
                    cell.place()
                    step += 1
            # Если же корабль не помещается в свободное место, функция запускается заново
            else:
                self.place_ship(ship)

    def event_handling(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                m_place = pg.mouse.get_pos()
                if self.width*0.05 < m_place[0] < self.width*0.95 and \
                        self.height-self.width < m_place[1] < self.width*0.9 + self.height-self.width:
                    m_c = math.ceil((m_place[0]-self.width*0.05) // (self.width*0.9/10))
                    m_r = math.ceil((m_place[1]-(self.height-self.width)) // (self.width*0.9/10))
                    self.aim[0], self.aim[1] = m_r, m_c
                    self.aim[2], self.aim[3] = False, False
                    if self.can_hit():
                        self.make_move()
                    else:
                        self.label_two = self.input_font.render('Вы уже выбирали эту клетку!', False,
                                                                self.font_color, self.font_back_color)
                        self.label_three = self.input_font.render('', False, self.font_color, self.font_back_color)


# Это класс корабельной ячейки
class Cell:
    def __init__(self, game, r=0, c=0, state=True):
        # Номер строки r - row
        self.r = r
        # Номер строки c - column
        self.c = c
        # Состояние ячейки: True - цела, False - разрушена
        self.state = state
        self.game = game

    # функция размещения ячейки
    def place(self):
        try:
            # Меняет значение ячейки и близлежащих ячеек в списке free_zone на 0 (т.е. занятые)
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if 0 <= self.r+i <= 9 and 0 <= self.c+j <= 9:
                        self.game.free_zone[self.r+i][self.c+j] = 0
        # Игнорировать случаи когда ячейка погранична
        except IndexError:
            None


# Это класс визуальной ячейки
class FieldCell(pg.sprite.Sprite):
    def __init__(self, game, r, c, state='default', bd=5):
        super().__init__()
        self.state = state
        self.game = game
        self.colors = {'default': ((103, 159, 151), (75, 109, 104)),
                       'hit': ((250, 231, 127), (159, 146, 73)),
                       'destroyed': ((255, 139, 139), (164, 89, 89)),
                       'missed': ((158, 173, 169), (116, 128, 125)),
                       'mark': ((18, 77, 62), (10, 46, 36))}
        self.size = [game.width*0.9/10, game.width*0.9/10]
        self.bd_size = bd
        self.bound = pg.Surface((self.size[0], self.size[1]))
        self.image = pg.Surface((self.game.width/10-self.bd_size*2, self.game.width/10-self.bd_size*2))
        self.rect = self.bound.get_rect(topleft=(self.game.width*0.05 + c*self.size[0],
                                                 self.game.height-self.game.width + r*self.size[1]))
        self.img_rect = self.image.get_rect(center=self.rect.center)

    def draw(self):
        # Заполняет внешний и внутренний квадраты нужными цветами
        self.bound.fill(self.colors[self.state][1])
        self.image.fill(self.colors[self.state][0])
        # Затем отрисовывает оба квадрата
        self.game.screen.blit(self.bound, self.rect)
        self.game.screen.blit(self.image, self.img_rect)


# Класс корабля
class Ship:
    def __init__(self, game, size):
        self.game = game
        # Размер корабля определяет количество корабельных ячеек
        self.size = size
        # В списке cells содержатся экземпляры корабельных ячеек
        self.cells = list(Cell(self.game) for i in range(self.size))

    # Возвращает True если у корабля не осталось целых ячеек
    def is_drown(self):
        if True not in list(cell.state for cell in self.cells):
            # Если корабль потонул, меняет цвет всех его ячеек на красный
            for cell in self.cells:
                self.game.cell_map[cell.r][cell.c].state = 'destroyed'
            return True
        else:
            return False

    def __str__(self):
        return f'{[(cell.r, cell.c, cell.state) for cell in self.cells]}'


# Создание экземпляра игры
root = Game(False)

# Запуск основного цикла игры
while root.running:
    # Принимает ввод пользователя
    root.event_handling()
    # Показывает карту
    root.show_map()
    # Проверяет условие окончания игры
    root.check_win()

pg.quit()
