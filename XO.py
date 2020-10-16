#!/usr/bin/env python3
#coding: utf-8


from os import system, name
from sys import exit


def checkStatus(matrix, ox):
    """
    Проверка ходоф, кто победитель
    """
    # Словари для подсчета ходов по диагонали
    diagonal_left = {'11':0, '22':0, '33':0}
    diagonal_right = {'13':0, '22':0, '31':0}
    # Проверка по горизонтали
    for y in matrix.items():
        count = 0
        for x in y[1].items():
            count += 1 if x[1] == ox else 0
            # Сбор данных о ходах по диагонали
            if x[0] in diagonal_left.keys() and x[1] != '-': diagonal_left[x[0]] = 1 
            if x[0] in diagonal_right.keys() and x[1] != '-': diagonal_right[x[0]] = 1
        if count == 3:
            return True
    # Проверка по вертикали
    column_count = {}
    for y in matrix.items():
        for j in y[1].items():
            column_count[j[0][1:]] = column_count.setdefault(j[0][1:], 0)
            column_count[j[0][1:]] += 1 if j[1] == ox else 0
        if max(column_count.values()) == 3:
            return True
    # Проверка по диагонали
    if sum(diagonal_left.values()) == 3 or sum(diagonal_left.values()) == 3:
        return True
    return False


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
    def drawField(cell = 0, ox = '-'):
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
        if checkStatus(fieldMatrix, ox):
            return 'Victory'
    return drawField


def XorO():
    """
    Выбор игрока, который будет ходить
    """
    ox = ['X', 'O']
    while True:
        value = ox.pop(0)
        ox.append(value)
        yield value


def clearScreen():
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
    battleField = field()
    
    # Ход игры
    for ox in XorO():
        err = ''
        while True:
            clearScreen()
            print(f'{err}\nХод игрока {ox}\n')
            battleField()
            move = input('Формат:СтрокаСтолбец\n-> ')
            """
            Введеное значение должно соответсвовать формату: [Строка][Столбец], 
            например, 12 - первая строка, второй столбец.
            Значение не должно привышать диапазон заданных границ игрового поля - 3x3.
            """
            if len(move) == 2 and 0 < (int(move[0]) and int(move[1])) < 4:
                # Результат хода.
                game_res = battleField(move, ox)
                if game_res is False:
                    err = 'Вы не можете сделать ход в это поле!'
                    continue
                elif game_res is 'Victory':
                    clearScreen()
                    print(f'Победил игрок {ox}!')
                    exit()
            else:
                err = 'Введите корректное значение!'
                continue
            break


if __name__ == "__main__":
    main()