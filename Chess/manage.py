from GameField import *
from Figure import *

def main():
    gamefield = GameField()
    print(gamefield)
    print()
    gamefield.select_unit('b', 0)
    print(gamefield)
    print()
    gamefield.selected.move_or_attack('a', 2)
    print(gamefield)
    print()
main()