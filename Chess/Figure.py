from GameField import *
from enum import Enum
from Utils import *


class Fraction(Enum):
    WHITE = 'white'
    BLACK = 'black'


class Unit:
    def __init__(self):
        self.x = None
        self.y = None
        self.fraction = None
        self.game_field: GameField = None
        self.moves = []
        self.is_alive = True

    def __init__(self, field, x, y, fraction):
        self.x = convert_column_to_digit(x)
        self.y = y
        self.fraction: Fraction = fraction
        self.game_field = field
        self.moves = []
        self.is_alive = True

    def attack(self, x_pos, y_pos):
        self.game_field.field[self.y][self.x] = Empty()
        self.game_field.field[y_pos][x_pos] = self
        print("Attacked and killed motherfucker")

    def move(self, x_pos, y_pos):
        self.game_field.field[self.y][self.x] = Empty()
        self.game_field.field[y_pos][x_pos] = self

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


class Empty:
    def __str__(self):
        return "."


class King(Unit):
    def __init__(self, field, x_pos, y_pos, fraction):
        super().__init__(field, x_pos, y_pos, fraction)
        self.moves = [[-1, -1],
                      [-1, 0],
                      [-1, 1],
                      [0, -1],
                      [0, 0],
                      [0, 1],
                      [1, -1],
                      [1, 0],
                      [1, 1],
                      ]

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'K'
        else:
            return 'k'


class Queen(Unit):
    def __init__(self, field, x_pos, y_pos, fraction):
        super().__init__(field, x_pos, y_pos, fraction)
        self.moves = []
        for i in range(-field.WIDTH+1, field.WIDTH, 1):
            for j in range(-field.WIDTH+1, field.WIDTH, 1):
                self.moves.append([i, j])

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'Q'
        else:
            return 'q'


class PawnBlack(Unit):
    def __init__(self, field, x_pos, y_pos):
        super().__init__(field, x_pos, y_pos, Fraction.BLACK)
        self.first_step = True
        self.moves = [[-1, 0], [-2, 0]]
        self.attack_moves = [[-1, 1], [-1, -1]]

    def __str__(self):
        return 'p'


class PawnWhite(Unit):
    def __init__(self, field, x_pos, y_pos):
        super().__init__(field, x_pos, y_pos, Fraction.WHITE)
        self.first_step = True
        self.moves = [[1, 0], [2, 0]]
        self.attack_moves = [[1, 1], [1, -1]]

    def __str__(self):
        return 'P'


class Rook(Unit):
    def __init__(self, field, x_pos, y_pos, fraction):
        super().__init__(field, x_pos, y_pos, fraction)
        self.moves = []
        for i in range(-field.WIDTH+1, field.WIDTH, 1):
            if i != 0:
                self.moves.append([i, 0])
                self.moves.append([0, i])

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'R'
        else:
            return 'r'


class Bishop(Unit):
    def __init__(self, field, x_pos, y_pos, fraction):
        super().__init__(field, x_pos, y_pos, fraction)
        self.moves = []
        for i in range(1, field.WIDTH, 1):
            if i != 0:
                self.moves.append([i, i])
                self.moves.append([-i, i])
                self.moves.append([i, -i])
                self.moves.append([-i, -i])

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'B'
        else:
            return 'b'


class Knight(Unit):
    def __init__(self, field, x_pos, y_pos, fraction):
        super().__init__(field, x_pos, y_pos, fraction)
        self.moves = [[-2, 1],
                      [-2, -1],
                      [-1, -2],
                      [1, -2],
                      [2, -1],
                      [2, 1],
                      [-1, 2],
                      [1, 2]]

    def __str__(self):
        if self.fraction == Fraction.WHITE:
            return 'N'
        else:
            return 'n'