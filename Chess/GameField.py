import Figure as Figure
from Utils import *

class GameField:
    WIDTH = 8
    alphabet = "abcdefgh"

    def __init__(self):
        self.field = [[Figure.Empty()] * self.WIDTH for x in range(self.WIDTH)]
        self.init_units()
        self.selected = None
        self.turn = Figure.Fraction.WHITE
        #self.game_field[0][0] =

    def init_units(self):
        self.set_item(row=0, column='e', value=Figure.King(field=self,
                                                           x_pos=5,
                                                           y_pos=0,
                                                           fraction=Figure.Fraction.WHITE))
        self.set_item(row=0, column='d', value=Figure.Queen(field=self,
                                                            x_pos=4,
                                                            y_pos=0,
                                                            fraction=Figure.Fraction.WHITE))
        self.set_item(row=7, column='d', value=Figure.King(field=self,
                                                           x_pos=4,
                                                           y_pos=7,
                                                           fraction=Figure.Fraction.BLACK))
        self.set_item(row=7, column='e', value=Figure.Queen(field=self,
                                                            x_pos=5,
                                                            y_pos=7,
                                                            fraction=Figure.Fraction.BLACK))
        for column in range(self.WIDTH):
            self.set_item(row=6, column=column, value=Figure.PawnBlack(field=self,
                                                                       x_pos=column,
                                                                       y_pos=6))
        for column in range(self.WIDTH):
            self.set_item(row=1, column=column, value=Figure.PawnWhite(field=self,
                                                                       x_pos=column,
                                                                       y_pos=1))
        self.set_item(row=7, column='a', value=Figure.Rook(field=self,
                                                           x_pos=0,
                                                           y_pos=7,
                                                           fraction=Figure.Fraction.BLACK))
        self.set_item(row=7, column='h', value=Figure.Rook(field=self,
                                                           x_pos=7,
                                                           y_pos=7,
                                                           fraction=Figure.Fraction.BLACK))
        self.set_item(row=0, column='a', value=Figure.Rook(field=self,
                                                           x_pos=0,
                                                           y_pos=0,
                                                           fraction=Figure.Fraction.WHITE))
        self.set_item(row=0, column='h', value=Figure.Rook(field=self,
                                                           x_pos=7,
                                                           y_pos=0,
                                                           fraction=Figure.Fraction.WHITE))
        self.set_item(row=7, column='c', value=Figure.Bishop(field=self,
                                                             x_pos=2,
                                                             y_pos=7,
                                                             fraction=Figure.Fraction.BLACK))
        self.set_item(row=7, column='f', value=Figure.Bishop(field=self,
                                                             x_pos=5,
                                                             y_pos=7,
                                                             fraction=Figure.Fraction.BLACK))
        self.set_item(row=0, column='c', value=Figure.Bishop(field=self,
                                                             x_pos=2,
                                                             y_pos=0,
                                                             fraction=Figure.Fraction.WHITE))
        self.set_item(row=0, column='f', value=Figure.Bishop(field=self,
                                                             x_pos=5,
                                                             y_pos=0,
                                                             fraction=Figure.Fraction.WHITE))
        self.set_item(row=7, column='b', value=Figure.Knight(field=self,
                                                             x_pos=1,
                                                             y_pos=7,
                                                             fraction=Figure.Fraction.BLACK))
        self.set_item(row=7, column='g', value=Figure.Knight(field=self,
                                                             x_pos=6,
                                                             y_pos=7,
                                                             fraction=Figure.Fraction.BLACK))
        self.set_item(row=0, column='b', value=Figure.Knight(field=self,
                                                             x_pos=1,
                                                             y_pos=0,
                                                             fraction=Figure.Fraction.WHITE))
        self.set_item(row=0, column='g', value=Figure.Knight(field=self,
                                                             x_pos=6,
                                                             y_pos=0,
                                                             fraction=Figure.Fraction.WHITE))

    def is_in_bounds(self, x, y):
        if 0 <= x < self.WIDTH and 0 <= y < self.WIDTH:
            return True
        return False

    def is_on_empty(self, x, y):

        return isinstance(self.field[y][x], Figure.Empty)

    def is_on_enemy(self, x, y, unit):
        if isinstance(self.field[y][x], Figure.Unit) and not isinstance(self.field[y][x], Figure.Empty) and \
                self.field[y][x].fraction != unit.fraction:
            return True
        return False

    def __str__(self):
        letters = "A B C D E F G H"
        row_cnt = 1
        result = ""
        result += "   " + letters + "\n\n"
        for row in self.field:
            result += str(row_cnt) + "  "
            for elem in row:
                result += elem.__str__() + " "
            result += " " + str(row_cnt) + "\n"
            row_cnt += 1
        result += "\n   " + letters
        return result

    def get_item(self, column, row):
        column = convert_column_to_digit(column)
        return self.field[row][column]

    def set_item(self, column, row, value):
        column = convert_column_to_digit(column)

        if type(row) != int or row >= self.WIDTH or row < 0:
            raise ValueError('Неверное значение для строки ' + row)

        self.field[row][column] = value

    def clean_empty(self):
        for row in self.field:
            for el in row:
                if isinstance(el, Figure.Path):
                    el = Figure.Empty

    def select_unit(self, column, row):
        choice = self.get_item(column, row)
        if isinstance(choice, Figure.Unit):
            if choice.fraction != self.turn:
                raise ValueError('На {} {} нет доступной фигуры'.format(column, row))
            self.selected = choice
        else:
            raise ValueError('На {} {} нет доступной фигуры'.format(column, row))

        self.clean_empty()

        choice.show_paths()

    def switch_turn(self):
        if self.turn == Figure.Fraction.WHITE:
            self.turn = Figure.Fraction.BLACK
        else:
            self.turn = Figure.Fraction.WHITE


class MemorizedField:
    def __init__(self, field, turn):
        self.field = [row[:] for row in field]
        self.turn = turn
