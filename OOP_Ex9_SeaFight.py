from random import choice


class Game:
    # Инициализация игры, по умолчанию размер игрового поля - 10 на 10
    def __init__(self, size=(10, 10)):
        # В этом списке будут храниться экземпляры кораблей
        self.ships = []
        # Этот список будет представлять игровое поле
        self.field = []
        # Эта переменная отвечает за главный цикл игры
        self.running = True
        # Это список хранит данные, введеные пользователем -> | строка | столбец | есть попадание | корабль уничтожен |
        self.aim = [0, 0, False, False]

        # Далее список игрового поля заполняется дефисами
        # Сначала в него добавляются 10 строк
        for row in range(size[0]):
            self.field.append([])
        # Затем в каждую строку добавляется 10 столбцов
        for row in self.field:
            for col in range(size[1]):
                # И вставляется символ дефис '-'
                row.append('-')
            # Здесь выводится номер строки под каждой строкой
            row.append(f'|{self.field.index(row)}')

        # free_zone - список того же размера, что и игровое поле, заполненный единицами
        # Он используется алгоритмом случайной расстановки кораблей
        # 1 - в списке означает, что ячейка свободна для помещения в нее корабельной ячейки
        self.free_zone = []
        for row in range(size[0]):
            self.free_zone.append([])
        for row in self.free_zone:
            for col in range(size[1]):
                row.append('1')

    # Эта функция выводит игровое поле на экран
    def show_map(self):
        print('\n\n\n')
        for row in self.field:
            print((' | '.join(str(col) for col in row)))
        print('_________________________________________')
        print(' | '.join(str(k) for k in range(len(self.field))))

    # Эта функция выводит free_zone на экран
    # Нужна была функция только для отладки
    def show_free_map(self):
        print('\n')
        for row in self.free_zone:
            print((' | '.join(str(col) for col in row)))

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
                        if ship.is_drawn():
                            self.aim[3] = True
                        return True
        # Если же никакой корабль не задет, значения "есть попадание" и "корабль уничтожен" становятся равны False
        self.aim[2], self.aim[3] = False, False
        # И если клетка игрового поля уже не была затронута возвращает True иначе False
        if self.field[self.aim[0]][self.aim[1]] not in ('M', 'X'):
            return True
        else:
            return False

    # Функция для ввода пользователем информации
    def get_player_input(self):
        # Ввод происходит до тех пор, пока не будут введены корректные данные
        while True:
            try:
                print('\nИгрок, вводите координаты точки')

                try:
                    self.aim[0], self.aim[1] = int(input('Строка: ')), int(input('Столбец: '))
                    self.aim[2], self.aim[3] = False, False

                    if self.can_hit():
                        break
                    else:
                        print('\nЯчейка уже была отмечена, попробуйте ввести другую!!!')

                except ValueError:
                    print('Вы ввели некорректный номер ячейки, допустимый интервал от 0 до 9 включительно!')
                    self.get_player_input()

            except IndexError:
                print('Вы ввели некорректный номер ячейки, допустимый интервал от 0 до 9 включительно!')
                self.get_player_input()

    # Функция выводит результат хода, и вводит изменения на карту
    def make_move(self):
        if self.aim[2]:
            input('Есть попадание! (enter) >')
            if self.aim[3]:
                input('Корабль уничтожен! (enter) >')
            self.field[self.aim[0]][self.aim[1]] = 'X'
        else:
            input('Промах! (enter) >')
            self.field[self.aim[0]][self.aim[1]] = 'M'

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
            self.show_map()
            self.running = False
            print('Флот противника уничтожен! Победа!')

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

        # Можно раскомментировать, чтобы видеть положение кораблей (для отладки)
        '''
        finally:
            self.game.field[self.r][self.c] = 'H'
        '''


# Класс корабля
class Ship:
    def __init__(self, game, size):
        self.game = game
        # Размер корабля определяет количество корабельных ячеек
        self.size = size
        # В списке cells содержатся экземпляры корабельных ячеек
        self.cells = list(Cell(self.game) for i in range(self.size))

    # Возвращает True если у корабля не осталось целых ячеек
    def is_drawn(self):
        return True not in list(cell.state for cell in self.cells)


# Создание экземпляра игры
root = Game()
# Расстановка 10 кораблей разного размера
number = 0
for i_size in [4, 3, 2, 1]:
    for i_num in range(5-i_size):
        t_ship = Ship(root, i_size)
        root.ships.append(t_ship)
        root.place_ship(t_ship)
        number += 1

# Запуск основного цикла игры
while root.running:
    # Показывает карту
    root.show_map()
    # Принимает ввод пользователя
    root.get_player_input()
    # Совершает ход
    root.make_move()
    # Проверяет условие окончания игры
    root.check_win()
