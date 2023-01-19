# Реализовать программу, с которой можно играть в игру «Морской бой».
# Программа автоматически случайно расставляет на поле размером 10 на 10 клеток:
# 4 1-палубных корабля, 3 2-палубных корабля, 2 3-палубных корабля и 1 4-х палубный.
# Между любыми двумя кораблями по горизонтали и вертикали должна быть как минимум 1 незанятая клетка.
# Программа позволяет игроку ходить, производя выстрелы. Сама программа НЕ ходит т.е. не пытается топить
# корабли расставленные игроком.
#
# Взаимодействие с программой производится через консоль.
# Игровое поле изображается в виде 10 текстовых строк и перерисовывается при каждом изменении состояния поля.
# При запросе данных от пользователя программа сообщает, что ожидает от пользователя
# (в частности, координаты очередного «выстрела») и проверяет корректность ввода.
# Программа должна уметь автоматически определять потопление корабля и окончание партии и сообщать об этих событиях.

import random

SHIPS_IDS = {}
SHIPS_STATUS = {}
OCCUPIED_CELLS = []

alpha_dict = {'a': 0,
              'b': 1,
              'c': 2,
              'd': 3,
              'e': 4,
              'f': 5,
              'g': 6,
              'h': 7,
              'i': 8,
              'j': 9}

clear_cell = '\u2b1c'  # квадрат
dead_cell = '\u274c'  # крестик
dot_cell = '\u25aa'  # точка


def neighbours(ship):
    # Функция принимает на вход список координат корабля в формате (x, y) и возвращает список
    # координат его клеток-соседей
    neighbours = []
    for i in range(len(ship)):
        x_axis = ship[i][0]
        y_axis = ship[i][1]
        for x in (max(x_axis - 1, 0), x_axis, min(9, x_axis + 1)):
            for y in (max(y_axis - 1, 0), y_axis, min(9, y_axis + 1)):
                if (x, y) not in ship+neighbours:
                    neighbours.append((x, y))
    return neighbours


def free_neighbours(cell):
    # Функция принимает на вход координаты клетки в формате (x, y) и возвращает список координат ее свободных
    # клеток-соседей, исключая соседей по диагонали
    free_neighbours_list = []
    for neighbour in neighbours([cell]):
        if neighbour not in OCCUPIED_CELLS and (neighbour[0] == cell[0] or neighbour[1] == cell[1]):
            free_neighbours_list.append(neighbour)
    return free_neighbours_list


def potential(cell):
    # Функция принимает на вход координаты клетки в формате (x, y) и возвращает индекс ее потенциала - максимальное
    # количество палуб корабля, который можно построить из этой клетки.
    if len(free_neighbours(cell)) == 0:
        return 1
    if len(free_neighbours(cell)) == 1:
        first_neighbour = free_neighbours(cell)[0]
        if len(free_neighbours(first_neighbour)) == 1:
            return 2
        elif len(free_neighbours(first_neighbour)) == 2:
            second_neighbour = [l for l in free_neighbours(first_neighbour) if l != cell]
            if len(free_neighbours(second_neighbour[0])) == 1:
                return 3
    elif len(free_neighbours(cell)) == 2 and len(free_neighbours(free_neighbours(cell)[0])) + len(free_neighbours(free_neighbours(cell)[0])) == 2:
        return 3
    return 4


def create_decker(decks):
    # Функция принимает на вход количество палуб корабля и возвращает список координат корабля в формате (x, y) с
    # указанным количеством палуб
    global SHIPS_IDS
    global SHIPS_STATUS
    global OCCUPIED_CELLS
    print("Строю " + str(decks) + "-палубник")
    tries = []
    tries_counts = []
    ship = []
    while len(ship) < decks:
        l = len(ship)
        tries_counts.append(l)
        if l == 0:
            print("Это первая клетка корабля. И " + str(tries_counts.count(l)) + "-я" + " попытка ее подобрать")
            x_axis = random.randint(0, 9)
            y_axis = random.randint(0, 9)
            print("Выбрал", x_axis, y_axis)
        else:
            print("Это " + str(l + 1) + "-я" + " клетка корабля. И " + str(
                tries_counts.count(l)) + "-я" + " попытка ее подобрать")
            innitial_cell = random.choice(ship)
            x = innitial_cell[0]
            y = innitial_cell[1]
            print("Отталкиваюсь от", x, y)
            if random.choice((0, 1)):
                print("Фиксирую y")
                y_axis = y
                if x == 9:
                    x_axis = 8
                elif x == 0:
                    x_axis = 1
                else:
                    x_axis = x + random.choice((-1, 1))
                print("Выбираю в качетсве x", x_axis)
            else:
                print("Фиксирую x")
                x_axis = x
                if y == 9:
                    y_axis = 8
                elif y == 0:
                    y_axis = 1
                else:
                    y_axis = y + random.choice((-1, 1))
                print("Выбираю в качетсве y", y_axis)
            tries.append((x_axis, y_axis))
        if (x_axis, y_axis) not in OCCUPIED_CELLS + ship and (potential((x_axis, y_axis)) >= decks or l > 0):
            print("Таких координат еще нет. Клетка готова")
            ship.append((x_axis, y_axis))
        else:
            print("Клетка занята или недостаточно потенциальна. Начинаю сначала")
    print("Корабль готов")
    ship_id = len(SHIPS_IDS)
    SHIPS_IDS.update({ship_id: ship})
    SHIPS_STATUS.update({ship_id: 0})
    OCCUPIED_CELLS += neighbours(ship)


def create_game_field():
    # Функция создает пустое игровое поле
    game_field = {}
    for i in range(100):
        game_field.update({i: clear_cell})
    return game_field


def print_field(game_field):
    # Функция выода на экран игрового поля
    print("{:^107}".format('a   b  c  d   e  f   g  h  i   j'))
    for i in range(10):
        row = [str(i+1)]
        for j in range(10):
            row.append(str(game_field[i + j*10]))
        print("{:^100}".format('  '.join(row)))


def ship_dead(game_field, ship):
    # Функция прнимает на вход словарь с игровым полем, координаты корабля и определяет, является ли корабль убитым
    # (все клетки в статусе dead)
    for cell in ship:
        if game_field[cell[0]*10 + cell[1]] != dead_cell:
            return False
    return True


def make_shot(game_field, shot):
    # Функция "делает выстрел" - прнимает на вход словарь с игровым полем, координаты выстрела и
    # вносит необходимые изменения во все словари
    x_axis = int(alpha_dict[shot[0]])
    y_axis = int(shot[1:])-1
    for ship_id in SHIPS_IDS:
        ship = SHIPS_IDS[ship_id]
        for cell in ship:
            if x_axis == cell[0] and y_axis == cell[1]:
                game_field.update({y_axis + x_axis * 10: dead_cell})
                if ship_dead(game_field, ship):
                    SHIPS_STATUS.update({ship_id: 1})
                    for neighbour_cell in neighbours(ship):
                        game_field.update({neighbour_cell[1] + neighbour_cell[0] * 10: dot_cell})
                    return "{:-^100}".format("Корабль убит!")
                else:
                    return "{:-^100}".format("Корабль ранен!")
    game_field.update({y_axis + x_axis * 10: dot_cell})
    return "{:-^100}".format("Мимо")


def sea_battle():
    # Функция запускает игру в Морской бой
    SHIPS_IDS.clear()
    SHIPS_STATUS.clear()
    OCCUPIED_CELLS.clear()
    turn = 0

    create_decker(1)
    create_decker(1)
    create_decker(1)
    create_decker(1)
    create_decker(2)
    create_decker(2)
    create_decker(2)
    create_decker(3)
    create_decker(3)
    create_decker(4)

    print(SHIPS_IDS)
    print(SHIPS_STATUS)
    print(OCCUPIED_CELLS)

    game_field = create_game_field()
    print_field(game_field)

    while 0 in list(SHIPS_STATUS.values()):
            shot = str(input("Введите координаты выстрела в формате 'буква+цифра' (например, b1):\n"))
            if shot[0] not in list(alpha_dict.keys()) or int(shot[1:])-1 not in range(10):
                print("Координаты выстрела введены неверно!")
            else:
                turn += 1
                print(make_shot(game_field, shot))
                print_field(game_field)

    print("Вы закончили игру в", turn, "ходов!")


game_on = 'y'
while game_on == 'y':
    print("{:-^100}".format("Добро пожаловать в игру Морской бой!"))
    sea_battle()
    game_on = input("Сыграем еще раз? Введите y для новой игры или n для выхода из игры:\n")





