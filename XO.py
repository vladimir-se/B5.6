#!/usr/bin/env python3
#coding: utf-8


from os import system, name
from sys import exit


def check_status(matrix, ox):
    """
    Проверка ходоф, кто победитель
    Возвращаемые значения:
    0 - следующий ход
    1 - победа
    2 - ничья
    """
    # Словари для подсчета ходов по диагонали
    diagonal_left = {'11':0, '22':0, '33':0}
    diagonal_right = {'13':0, '22':0, '31':0}
    nobody_won = 0
    # Проверка по горизонтали
    for y in matrix.items():
        count = 0
        for x in y[1].items():
            count += 1 if x[1] == ox else 0
            # Сбор данных о ходах по диагонали
            if x[0] in diagonal_left.keys() and x[1] == ox: diagonal_left[x[0]] = 1 
            if x[0] in diagonal_right.keys() and x[1] == ox: diagonal_right[x[0]] = 1
            # Подсчет доступных ходов чтобы определить ничью
            nobody_won += 1 if x[1] == '-' else 0
        if count == 3:
            return 1
    # Проверка по вертикали
    column_count = {}
    for y in matrix.items():
        for j in y[1].items():
            column_count[j[0][1:]] = column_count.setdefault(j[0][1:], 0)
            column_count[j[0][1:]] += 1 if j[1] == ox else 0
        if max(column_count.values()) == 3:
            return 1
    # Проверка по диагонали
    if sum(diagonal_left.values()) == 3 or sum(diagonal_right.values()) == 3:
        return 1
    # Проверка на ничью
    if nobody_won == 0:
        return 2
    return 0


def field():
    """
    Создание игрового поля
    """
    fieldMatrix = {
        0:{'00':'1', '01':'2', '02':'3'},
        1:{'11':'-', '12':'-', '13':'-'},
        2:{'21':'-', '22':'-', '23':'-'},
        3:{'31':'-', '32':'-', '33':'-'}
        }
    def draw_field(cell = 0, ox = '-'):
        """
        Отметка ходов на игровом поле
        """
        # Контроль ходов, нельзя делать ход в поле, в которое уже был сделан ход
        if cell != 0 and fieldMatrix[int(cell[:1])][cell] == '-':
            fieldMatrix[int(cell[:1])][cell] = ox
        elif cell != 0 and fieldMatrix[int(cell[:1])][cell] != '-':
            return False
        # Отметка ходов на игровом поле
        for y in fieldMatrix:
            print(' ' if y == 0 else y, end=f'{" "*5}')
            for x in fieldMatrix[y].values():
                print(x, end=f'{" "*5}')
            print('\n')
        # Контроль ходов, кто победил
        result = check_status(fieldMatrix, ox)
        return 'Victory' if result == 1 else ('Nobody_won' if result == 2 else None)

    return draw_field


def x_or_o():
    """
    Выбор игрока, который будет ходить
    """
    ox = ['X', 'O']
    while True:
        value = ox.pop(0)
        ox.append(value)
        yield value


def clear_screen():
    """
    Очистка экрана после каждого хода
    """
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def main():
    """
    Основноа
    """
    # Создание игрового поля
    battle_field = field()
    
    # Ход игры
    for ox in x_or_o():
        err = ''
        while True:
            clear_screen()
            print(f'{err}\nХод игрока {ox}\n')
            battle_field()
            move = input('Формат:СтрокаСтолбец\n-> ')
            """
            Введеное значение должно соответсвовать формату: [Строка][Столбец], 
            например, 12 - первая строка, второй столбец.
            Значение не должно привышать диапазон заданных границ игрового поля - 3x3.
            """
            if len(move) == 2 and 0 < (int(move[0]) and int(move[1])) < 4:
                # Результат хода.
                game_res = battle_field(move, ox)
                if game_res is False:
                    err = 'Вы не можете сделать ход в это поле!'
                    continue
                elif game_res == 'Victory':
                    clear_screen()
                    print(f'Победил игрок {ox}!')
                    exit()
                elif game_res == 'Nobody_won':
                    clear_screen()
                    print(f'Ничья')
                    exit()
            else:
                err = 'Введите корректное значение!'
                continue
            break


if __name__ == "__main__":
    main()