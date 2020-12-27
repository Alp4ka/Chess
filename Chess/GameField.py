import Figure as Figure
import copy
from Utils import *


class GameField:
    WIDTH = 8
    alphabet = "abcdefgh"

    def __init__(self):
        self.field = [[Figure.Empty()] * self.WIDTH for x in range(self.WIDTH)]
        self.init_units()

        # check['white'] = true белым ставили шах
        # check['black'] = true черным ставили шах
        self.check = dict()
        self.check['white'] = False
        self.check['black'] = False

        # mate['white'] = false  белым ставили мат
        # mate['black'] = false черным ставили мат
        self.mate = dict()
        self.mate['white'] = False
        self.mate['black'] = False


        self.eaten = dict()
        self.eaten['white'] = list()
        self.eaten['black'] = list()


        self.selected = None
        self.turn = Figure.Fraction.WHITE
        self.memory_stack = list()
        self.current_step = 0

        self.save()

    def init_units(self):
        self.set_item(row=0, column='e', value=Figure.King(field=self,
                                                           x_pos=4,
                                                           y_pos=0,
                                                           fraction=Figure.Fraction.WHITE))
        self.set_item(row=0, column='d', value=Figure.Queen(field=self,
                                                            x_pos=3,
                                                            y_pos=0,
                                                            fraction=Figure.Fraction.WHITE))
        self.set_item(row=7, column='d', value=Figure.King(field=self,
                                                           x_pos=3,
                                                           y_pos=7,
                                                           fraction=Figure.Fraction.BLACK))
        self.set_item(row=7, column='e', value=Figure.Queen(field=self,
                                                            x_pos=4,
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

    def find_king(self, fraction):
        for row in range(self.WIDTH):
            for elem in range(self.WIDTH):
                if isinstance(self.get_item(elem, row), Figure.King):
                    if self.get_item(elem, row).fraction == fraction:
                        return self.get_item(elem, row)

    def __str__(self):
        letters = "A B C D E F G H"
        row_cnt = 1
        result = "Съеденные {}: {}".format(Figure.Fraction.WHITE.value, ' '.join([x.__str__() for x in self.eaten[Figure.Fraction.WHITE.value]])) + "\n"
        result += "Съеденные {}: {}".format(Figure.Fraction.BLACK.value, ' '.join([x.__str__() for x in self.eaten[Figure.Fraction.BLACK.value]])) + "\n"
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
        for r in range(self.WIDTH):
            for c in range(self.WIDTH):
                if isinstance(self.field[r][c], Figure.Path):
                    self.field[r][c] = Figure.Empty()

    def select_unit(self, column, row):
        choice = self.get_item(column, row)
        if isinstance(choice, Figure.Unit) and not isinstance(choice, Figure.Empty):
            if choice.fraction != self.turn:
                raise ValueError('На {} {} нет доступной фигуры'.format(column, row))
            self.selected = choice
        else:
            raise ValueError('На {} {} нет доступной фигуры'.format(column, row))

        #self.clean_empty()

        choice.show_paths()

    def switch_turn(self):
        if self.turn == Figure.Fraction.WHITE:
            self.turn = Figure.Fraction.BLACK
        else:
            self.turn = Figure.Fraction.WHITE

    def save(self):
        self.memory_stack.append(MemorizedField(self))

    def undo(self):
        print("UNDO")
        if len(self.memory_stack) > 0:
            previous = self.memory_stack.pop()
            self.field = [[elem.copy() for elem in row] for row in previous.field]
            self.turn = copy.copy(previous.turn)
            self.current_step = copy.copy(previous.current_step)
        else:
            raise IndexError("Невозможно вернуться назад, буфер пустой")

class MemorizedField:
    def __init__(self, gamefield):
        self.field = [[elem.copy() for elem in row] for row in gamefield.field]
        self.turn = copy.copy(gamefield.turn)
        self.current_step = copy.copy(gamefield.current_step)

    def __str__(self):
        letters = "A B C D E F G H"
        row_cnt = 1
        result = "{} STEP \n".format(self.current_step)
        result += "   " + letters + "\n\n"
        for row in self.field:
            result += str(row_cnt) + "  "
            for elem in row:
                result += elem.__str__() + " "
            result += " " + str(row_cnt) + "\n"
            row_cnt += 1
        result += "\n   " + letters + "\n_______________________________"
        return result

