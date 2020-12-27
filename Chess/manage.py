from GameField import *
from Figure import *
from Utils import convert_column_to_digit

''' 
 | Выбор действия |
         |
         v
 |   Выполнение   |

'''
split = "+---------------+"


def main():
    gamefield = GameField()
    print(gamefield)
    print()

    gamefield.select_unit('a', 1)
    print(gamefield)
    print()

    gamefield.selected.move_or_attack('a', 2)
    gamefield.current_step += 1
    gamefield.save()


    print(gamefield)
    print()

    gamefield.select_unit('a', 2)
    print(gamefield)
    print()
    gamefield.selected.move_or_attack('a', 3)
    gamefield.current_step += 1
    gamefield.save()

    gamefield.select_unit('b', 1)
    gamefield.undo()
    print(gamefield)
    print()

    gamefield.undo()
    print(gamefield)
    print()

    gamefield.select_unit('b', 1)
    print(gamefield)
    print()
main()