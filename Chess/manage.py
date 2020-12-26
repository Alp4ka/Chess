from GameField import *
from Figure import *
from Utils import convert_column_to_digit

split = "+---------------+"
def main():
    gamefield = GameField()
    print(gamefield)
    print()
    #gamefield.select_unit('b', 0)
    print(gamefield)
    print()
   # gamefield.selected.move_or_attack('a', 2)
    gamefield.set_item(row=6, column='e', value=Figure.PawnWhite(field=gamefield,
                                                        x_pos=4,
                                                        y_pos=6,
                                                        fraction=Figure.Fraction.WHITE))
    gamefield.select_unit('e', 6)
    #gamefield.selected.move_or_attack('d', 6)
    #gamefield.selected.move_or_attack('e', 7)
    #gamefield.selected.move_or_attack('d', 8)
    #gamefield.selected.move_or_attack('e', 7)
    #gamefield.selected.move_or_attack('e', 3)
    #gamefield.selected.move_or_attack('e', 4)
    print(gamefield)
    print()
    # while True:
    #     print("Вы играете за: {}".format(gamefield.turn))
    #     print(gamefield)
    #     print("Введите позицию в формате: <столбец> <строка> ")
    #     print("Пример: a 2")
    #     print(split)
    #     data = input()
    #     splitted = data.split()
    #     col, row = splitted[0], splitted[1]
    #     col = convert_column_to_digit(col)
    #     row = int(row)
    #     if (row < 0 or row > 7):
    #         raise ValueError("")
main()