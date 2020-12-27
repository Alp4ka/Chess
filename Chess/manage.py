from GameField import *
from Figure import *
from Utils import convert_column_to_digit

split = "+---------------+"
def main():
    gamefield = GameField()
    print(gamefield)
    print()

    gamefield.select_unit('a', 1)
    print(gamefield)
    print()

    gamefield.selected.move_or_attack('a', 2)
    gamefield.save()

    print(gamefield)
    print()

    gamefield.select_unit('a', 2)
    print(gamefield)
    print()
    gamefield.selected.move_or_attack('a', 3)
    gamefield.save()


main()