WIDTH = 8

def convert_column_to_digit(column: str):
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