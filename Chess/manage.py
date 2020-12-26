from GameField import *
from Figure import *

def main():
    gamefield = GameField()
    print(gamefield)
    print()
    #gamefield.select_unit('b', 1)
    gamefield.set_item(row=5, column='e', value=Figure.Queen(field=gamefield,
                                                       x_pos=convert_column_to_digit('e'),
                                                       y_pos=5,
                                                       fraction=Figure.Fraction.WHITE))
    gamefield.select_unit('e', 5)
    print(gamefield)
    print()
    gamefield.selected.move_or_attack('a', 2)
    print(gamefield)
    print()
main()