from Figure import *
import Figure


class GameField:
    WIDTH = 8

    def __init__(self):
        self.field = [[Empty()] * self.WIDTH for x in range(self.WIDTH)]
        self.field[0][4] = King(field=self,
                                x_pos=4,
                                y_pos=0,
                                fraction=Fraction.WHITE)
        self.selected = None
        self.turn = Fraction.WHITE
        #self.field[0][0] =

    def is_in_bounds(self, x, y):
        if 0 <= x < self.WIDTH and 0 <= y < self.WIDTH:
            return True
        else:
            return False

    def is_not_on_ally(self, x, y, unit):
        if self.is_on_enemy(x, y, unit.fraction):
            return True
        elif self.field[y][x] is not Figure.Unit:
            return True
        else:
            return False

    def is_on_enemy(self, x, y, unit):
        if self.field[y][x] is Figure.Unit and self.field[y][x].fraction != unit.fraction:
            return True
        else:
            return False

    def __str__(self):
        letters = "A B C D E F G H"
        row_cnt = 1
        result = ""
        result += "  " + letters + "\n"
        for row in self.field:
            result += str(row_cnt) + " "
            for elem in row:
                result += elem.__str__() + " "
            result += str(row_cnt) + "\n"
            row_cnt += 1
        result += "  " + letters
        return result

    def get_item(self, column, row):
        if column.isalpha():
            alphabet = "abcdefgh"
            if alphabet.find(column) != -1:
                column = alphabet.find(column)
            else:
                raise ValueError('Неверное значение для столбца ' + column)
        elif column.isdigit():
            column = int(column)
            if column >= self.WIDTH or column < 0:
                raise ValueError('Неверное значение для столбца' + column)
        else:
            raise ValueError('Неверное значение для столбца ' + column)

        if row is not int or row >= self.WIDTH or row < 0:
            raise ValueError('Неверное значение для строки ' + row)

        return self.field[row][column]

    def set_item(self, column, row, value):
        if column.isalpha():
            alphabet = "abcdefgh"
            if alphabet.find(column.tolower()) != -1:
                column = alphabet.find(column.tolower())
            else:
                raise ValueError('Неверное значение для столбца ' + column)
        elif column.isdigit():
            column = int(column)
            if column >= self.WIDTH or column < 0:
                raise ValueError('Неверное значение для столбца' + column)
        else:
            raise ValueError('Неверное значение для столбца ' + column)

        if row is not int or row >= self.WIDTH or row < 0:
            raise ValueError('Неверное значение для строки ' + row)

        self.field[row][column] = value

    def select_unit(self, column, row):
        choice = self.get_item(column, row)
        if choice is Figure.Unit:
            self.selected = choice
        else:
            raise ValueError('На ')

class MemorizedField:
    def __init__(self, field, turn):
        self.field = [row[:] for row in field]
        self.turn = turn