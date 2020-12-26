from Chess.Figure import *

def main():
    gamefield = GameField()
    print(gamefield)
    print()
    gamefield.select_unit('e', 0)
    gamefield.selected.move_or_attack('e', 2)
    print(gamefield)
main()