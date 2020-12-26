from GameField import *

def main():
    gamefield = GameField()
    print(gamefield)
    print()
    gamefield.select_unit('a', 0)
    gamefield.selected.move_or_attack('a', 1)
    print(gamefield)
main()