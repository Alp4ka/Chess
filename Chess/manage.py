from GameField import *

def main():
    gamefield = GameField()
    print(gamefield)
    print()
    gamefield.select_unit('b', 0)
    gamefield.selected.move_or_attack('a', 2)
    print(gamefield)

main()