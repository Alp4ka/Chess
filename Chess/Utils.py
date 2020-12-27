WIDTH = 8
DEBUG = True


def convert_column_to_digit(column):
    alphabet = "abcdefgh"
    if type(column) == str:
        if alphabet.find(column) != -1:
            return alphabet.find(column)
        else:
            raise ValueError('Неверное значение для столбца ' + column)
    elif type(column) == int:
        column = int(column)
        if column >= WIDTH or column < 0:
            raise ValueError('Неверное значение для столбца' + column)
        return column
    else:
        raise ValueError('Неверное значение для столбца ' + column)


def signum(x: int):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Equals(self, point):
        return self.x == point.x and self.y == point.y