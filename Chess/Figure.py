from GameField import *
from enum import Enum
from Utils import *
import copy


class Fraction(Enum):
    WHITE = 'white'
    BLACK = 'black'


class Unit:
    '''def __init__(self):
        self.x = None
        self.y = None
        self.fraction = None
        self.game_field: GameField = None
        self.moves = []
        self.is_alive = True'''

    def __init__(self, field, x, y, fraction, is_alive=True):
        self.x = convert_column_to_digit(x)
        self.y = y
        self.fraction: Fraction = fraction
        self.game_field = field
        self.moves = []
        self.is_alive = is_alive

    def is_blocked(self, x_pos, y_pos):
        dir = Point(signum(x_pos - self.x), signum(y_pos - self.y))
        current = Point(self.x + dir.x, self.y + dir.y)
        dest = Point(x_pos, y_pos)

        while not current.Equals(dest):
            if self.game_field.is_in_bounds(current.x, current.y):
                if isinstance(self.game_field.field[current.y][current.x], Unit) and \
                        not isinstance(self.game_field.field[current.y][current.x], Empty):
                    return True
                current.y += dir.y
                current.x += dir.x
            else:
                break
        return False

    def attack(self, x_pos, y_pos):
        if not self.is_blocked(x_pos, y_pos):
            self.game_field.field[y_pos][x_pos].is_alive = False
            self.x = x_pos
            self.y = y_pos
            self.game_field.field[self.y][self.x] = Empty()
            self.game_field.field[y_pos][x_pos] = self
            print("Attacked and killed motherfucker")
        else:
            raise ValueError("Нельзя проходить через другие фигуры")

    def move(self, x_pos, y_pos):
        if not self.is_blocked(x_pos, y_pos):
            self.game_field.field[self.y][self.x] = Empty()
            self.x = x_pos
            self.y = y_pos
            self.game_field.field[y_pos][x_pos] = self
        else:
            raise ValueError("Нельзя проходить через другие фигуры")

    def move_or_attack(self, x_pos, y_pos):
        x_pos = convert_column_to_digit(x_pos)
        if [y_pos - self.y, x_pos - self.x] in self.moves:
            if self.game_field.is_on_empty(x_pos, y_pos):
                self.move(x_pos, y_pos)
            elif self.game_field.is_on_enemy(x_pos, y_pos, self):
                self.attack(x_pos, y_pos)
            else:
                raise ValueError("Недоступный ход.")
        else:
            raise ValueError("Недоступный ход.")

    def show_paths(self):
        pos = Point(self.x, self.y)
        for move in self.moves:
            pos_x = pos.x + move[1]
            pos_y = pos.y + move[0]
            if self.game_field.is_in_bounds(pos_x, pos_y):
                if not self.is_blocked(pos_x, pos_y):
                    if isinstance(self.game_field.field[pos_y][pos_x], Empty):
                        self.game_field.field[pos_y][pos_x] = Path()

class Empty:
    def copy(self):
        return Empty()

    def __str__(self):
        return "."

class Path(Empty):
    def __str__(self):
        return "*"

class King(Unit):
    def __init__(self, field, x_pos, y_pos, fraction, is_alive=True):
        super().__init__(field, x_pos, y_pos, fraction, is_alive)
        self.moves = [[-1, -1],
                      [-1, 0],
                      [-1, 1],
                      [0, -1],
                      [0, 1],
                      [1, -1],
                      [1, 0],
                      [1, 1]]

    def copy(self):
        return King(self.game_field, self.x, self.y, self.fraction, self.is_alive)

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'K'
        else:
            return 'k'


class Queen(Unit):
    def __init__(self, field, x_pos, y_pos, fraction, is_alive=True):
        super().__init__(field, x_pos, y_pos, fraction, is_alive)
        self.moves = []
        for i in range(1, field.WIDTH, 1):
            if i != 0:
                self.moves.append([i, i])
                self.moves.append([-i, i])
                self.moves.append([i, -i])
                self.moves.append([-i, -i])
        for i in range(-field.WIDTH + 1, field.WIDTH, 1):
            if i != 0:
                self.moves.append([i, 0])
                self.moves.append([0, i])

    def copy(self):
        return Queen(self.game_field, self.x, self.y, self.fraction, self.is_alive)

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'Q'
        else:
            return 'q'

#TODO: override show_paths
class Pawn(Unit):
    def __init__(self, field, x_pos, y_pos, fraction, is_alive):
        super().__init__(field, x_pos, y_pos, fraction, is_alive)
        self.first_step = True
        
#доделать
    def move(self, x_pos, y_pos):
        if not self.is_blocked(x_pos, y_pos):
            self.game_field.field[self.y][self.x] = Empty()
            self.game_field.field[y_pos][x_pos] = self
        else:
            raise ValueError("Нельзя проходить через другие фигуры")




class PawnBlack(Pawn):
    def __init__(self, field, x_pos, y_pos, fraction = Fraction.BLACK, is_alive=True):
        super().__init__(field, x_pos, y_pos, fraction, is_alive)
        self.moves = [[-1, 0], [-2, 0]]
        self.attack_moves = [[-1, 1], [-1, -1]]

    def copy(self):
        temp_pawn = PawnBlack(self.game_field, self.x, self.y, self.fraction, self.is_alive)
        temp_pawn.first_step = self.first_step
        return temp_pawn

    def __str__(self):
        return 'p'


class PawnWhite(Pawn):
    def __init__(self, field, x_pos, y_pos, fraction = Fraction.WHITE, is_alive=True):
        super().__init__(field, x_pos, y_pos, fraction, is_alive)
        self.moves = [[1, 0], [2, 0]]
        self.attack_moves = [[1, 1], [1, -1]]

    def copy(self):
        temp_pawn = PawnWhite(self.game_field, self.x, self.y, self.fraction, self.is_alive)
        temp_pawn.first_step = self.first_step
        return temp_pawn

    def __str__(self):
        return 'P'

class Rook(Unit):
    def __init__(self, field, x_pos, y_pos, fraction, is_alive=True):
        super().__init__(field, x_pos, y_pos, fraction, is_alive)
        self.moves = []
        for i in range(-field.WIDTH + 1, field.WIDTH, 1):
            if i != 0:
                self.moves.append([i, 0])
                self.moves.append([0, i])

    def copy(self):
        return Rook(self.game_field, self.x, self.y, self.fraction, self.is_alive)

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'R'
        else:
            return 'r'


class Bishop(Unit):
    def __init__(self, field, x_pos, y_pos, fraction, is_alive=True):
        super().__init__(field, x_pos, y_pos, fraction, is_alive)
        self.moves = []
        for i in range(1, field.WIDTH, 1):
            if i != 0:
                self.moves.append([i, i])
                self.moves.append([-i, i])
                self.moves.append([i, -i])
                self.moves.append([-i, -i])

    def copy(self):
        return Bishop(self.game_field, self.x, self.y, self.fraction, self.is_alive)

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'B'
        else:
            return 'b'


class Knight(Unit):
    def __init__(self, field, x_pos, y_pos, fraction, is_alive=True):
        super().__init__(field, x_pos, y_pos, fraction, is_alive)
        self.moves = [[-2, 1],
                      [-2, -1],
                      [-1, -2],
                      [1, -2],
                      [2, -1],
                      [2, 1],
                      [-1, 2],
                      [1, 2]]

    def copy(self):
        return Knight(self.game_field, self.x, self.y, self.fraction, self.is_alive)

    def is_blocked(self, x_pos, _pos):
        return False

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'N'
        else:
            return 'n'
