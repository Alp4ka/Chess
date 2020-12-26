from Chess.GameField import *
from enum import Enum
from Chess.Utils import *

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
        self.fraction = fraction
        self.game_field = field
        self.moves = []
        self.is_alive = True

    def attack(self):
        pass

#дописать
    def step(self, x_pos, y_pos):
        x_pos = convert_column_to_digit(x_pos)
        if [y_pos - self.y, x_pos - self.x] in self.moves:
            if self.game_field.is_not_on_ally(x_pos, y_pos, self):
                if self.game_field.is_on_enemy(x_pos, y_pos, self):
                    self.attack()
                else:
                    self.game_field.field
        else:
            raise ValueError('Недоступный ход.')


class Fraction(Enum):
    WHITE = 'white'
    BLACK = 'black'


class Empty:
    def __init__(self):
        pass

    def __str__(self):
        return "."


class King(Unit):
    def __init__(self, field, x_pos, y_pos, fraction):
        super().__init__(field, x_pos, y_pos, fraction)
        #[y, x]
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

