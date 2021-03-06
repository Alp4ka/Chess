import Figure as Figure
import copy
from Utils import *


class GameField:
    WIDTH = 8
    alphabet = "abcdefgh"
    separator = "+----------------------------+"

    translate = { 'white': 'белые', 'black': 'чёрные'}
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
        """
        Инициализация фигурок.
        """
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
        """
        Проверка, находится ли x y в грацницах поля.
        """
        if 0 <= x < self.WIDTH and 0 <= y < self.WIDTH:
            return True
        return False

    def is_on_empty(self, x, y):
        """
        Првоерка, на пустом ли поле.
        """
        return isinstance(self.field[y][x], Figure.Empty)

    def is_on_enemy(self, x, y, unit):
        """
        Является ли поле x,y вргом.
        """
        if isinstance(self.field[y][x], Figure.Unit) and not isinstance(self.field[y][x], Figure.Empty) and \
                self.field[y][x].fraction != unit.fraction:
            return True
        return False

    def find_king(self, fraction):
        """
        Вернуть instance King с King.fraction = fraction.
        """
        for row in range(self.WIDTH):
            for elem in range(self.WIDTH):
                if isinstance(self.get_item(elem, row), Figure.King):
                    if self.get_item(elem, row).fraction == fraction:
                        return self.get_item(elem, row)

    def generate_separator(self, n):
        ret = "+"
        for i in range(n-1):
            ret += "-"
        return ret + "+\n"

    def step_info(self):
        data = "|  Ход #{}: {}    |\n".format(self.current_step + 1, self.translate[self.turn.value])
        sep = self.generate_separator(len(data)-2)
        ret = sep
        ret += data
        ret += sep
        return ret

    def eaten_info(self, fraction):
        data = "| Съеденные {}: {}   |".format(self.translate[fraction.value], ' '.join([x.__str__() for x in self.eaten[fraction.value]])) + "\n"
        sep = self.generate_separator(len(data)-2)
        ret = sep
        ret += data
        ret += sep
        return ret

    def __str__(self):
        letters = " A B C D E F G H"
        row_cnt = 1
        result = self.step_info()
        result += self.eaten_info(Figure.Fraction.WHITE)
        result += self.eaten_info(Figure.Fraction.BLACK)
        if self.check['white'] is True:
            result += "Белые под шахом \n"
        if self.check['black'] is True:
            result += "Чёрные под шахом \n"

        result += self.separator
        result += "\n|     " + letters + "       |\n|"
        result += "    +-----------------+     |\n"
        for row in self.field:
            result += "| " + str(row_cnt) + "  | "
            for elem in row:
                result += elem.__str__() + " "
            result += "|   " + str(row_cnt) + " |\n"
            row_cnt += 1
        result += "|    +-----------------+     |\n"
        result += "|     " + letters + "       |\n" + self.separator
        return result

    def team_list(self, fraction):
        """
        Вернуть весь спитсок фигур на поле с Unit.fraction = fraction.
        """
        t_list = list()
        for r in range(self.WIDTH):
            for c in range(self.WIDTH):
                if isinstance(self.field[r][c], Figure.Unit):
                    if self.field[r][c].fraction == fraction:
                        t_list.append(self.field[r][c])
        return t_list

    def get_item(self, column, row):
        """
        Получить Instance на column row
        """
        #column = convert_column_to_digit(column)
        return self.field[row][column]

    def set_item(self, column, row, value):
        """
        Задать значение value в ячейке на column row.
        """
        column = convert_column_to_digit(column)

        if type(row) != int or row >= self.WIDTH or row < 0:
            raise ValueError('Неверное значение для строки ' + row)

        self.field[row][column] = value

    def clean_empty(self):
        """
        Очистить пустые клетки.
        """
        for r in range(self.WIDTH):
            for c in range(self.WIDTH):
                if isinstance(self.field[r][c], Figure.Path):
                    self.field[r][c] = Figure.Empty()

    def check_all_in_danger(self, fraction=None):
        """
        Проверить все фигуры Unit.fraction = fraction на налчие опасности.
        """
        if fraction is None:
            for r in range(self.WIDTH):
                for c in range(self.WIDTH):
                    if isinstance(self.field[r][c], Figure.Unit):
                        self.get_attackers(c, r)
            return
        for i in self.team_list(fraction):
            self.get_attackers(i.x, i.y)

    def is_checked(self, fraction):
        """
        Под шахом ли fraction.
        """
        king = self.find_king(fraction)
        if king is not None:
            attackers = self.get_attackers(king.x, king.y)
            if attackers is None or len(attackers) == 0:
                return False
            else:
                return True
        else:
            return True

    '''def is_mate(self, fraction):
        king = self.find_king(fraction)
        start_x = int(king.x)
        start_y = int(king.y)
        status = True
        if self.is_checked(fraction):
            for move in king.moves:
                try:
                    king.move(move[1]+start_x, move[0]+start_y)
                    if self.is_checked(fraction):
                except:
                    continue
        else:
            return False'''

    def get_attackers(self, x_pos, y_pos):
        """
        Список угроз для x_pos y_pos.
        """
        danger_f = list()
        unit_on = self.field[y_pos][x_pos]
        if not isinstance(unit_on, Figure.Unit):
            return None
        if unit_on.fraction == Figure.Fraction.WHITE:
            enemy_team = self.team_list(Figure.Fraction.BLACK)
        elif unit_on.fraction == Figure.Fraction.BLACK:
            enemy_team = self.team_list(Figure.Fraction.WHITE)
        else:
            raise ValueError('wtf')
        for i in range(len(enemy_team)):
            if enemy_team[i].may_attack(x_pos, y_pos):
                danger_f.append(enemy_team[i])
        if len(danger_f) > 0:
            check = False
            for elem in self.eaten[Figure.Fraction.WHITE.value]:
                if isinstance(elem, Figure.King):
                    check = True
                    break
            if not check:
                for elem in self.eaten[Figure.Fraction.BLACK.value]:
                    if isinstance(elem, Figure.King):
                        check = True
                        break
            if not check:
                print('Под угрозой {} от: '.format(unit_on.__str__()) + ' '.join([x.__str__() for x in danger_f]))
        return danger_f

    def select_unit(self, column, row):
        """
        Выбрать юнита.
        """
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
        """
        Сменить действующую сторону.
        """
        if self.turn == Figure.Fraction.WHITE:
            self.turn = Figure.Fraction.BLACK
        else:
            self.turn = Figure.Fraction.WHITE

    def save(self):
        """
        Засейвить ход в стэк.
        """
        self.memory_stack.append(MemorizedField(self))

    def undo(self):
        """
        Вернуть предыдущий ход.
        """
        if DEBUG:
            print("UNDO")
        last_copy = None
        if len(self.memory_stack) > 1:
            self.memory_stack.pop()
            last_copy = self.memory_stack[len(self.memory_stack)-1]
        else:
            last_copy = self.memory_stack[len(self.memory_stack)-1]

        self.field = [[elem.copy() for elem in row] for row in last_copy.field]
        self.turn = copy.copy(last_copy.turn)
        self.current_step = copy.copy(last_copy.current_step)
        self.eaten['white'] = [x.copy() for x in last_copy.eaten['white']]
        self.eaten['black'] = [x.copy() for x in last_copy.eaten['black']]
        # if len(self.memory_stack) > 0:
        #     previous = self.memory_stack.pop()
        #     if previous.current_step == self.current_step:
        #         self.undo()
        #         return
        #     self.field = [[elem.copy() for elem in row] for row in previous.field]
        #     self.turn = copy.copy(previous.turn)
        #     self.current_step = copy.copy(previous.current_step)
        # else:
        #     raise IndexError("Невозможно вернуться назад, буфер пустой")


class MemorizedField:
    def __init__(self, gamefield):
        self.eaten = dict()
        self.field = [[elem.copy() for elem in row] for row in gamefield.field]
        self.turn = copy.copy(gamefield.turn)
        self.current_step = copy.copy(gamefield.current_step)
        self.eaten['white'] = [x.copy() for x in gamefield.eaten['white']]
        self.eaten['black'] = [x.copy() for x in gamefield.eaten['black']]

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

