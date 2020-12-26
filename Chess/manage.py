from GameField import *

def main():
    gamefield = GameField()
    print(gamefield)
    print()
    gamefield.select_unit('a', 0)
    gamefield.selected.move_or_attack('b', 0)
    print(gamefield)

main()