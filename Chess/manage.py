from Chess.GameField import *
from Chess.Figure import *

def main():
    gamefield = GameField()
    print(gamefield)
    print()
    gamefield.select_unit('d', 0)
    gamefield.selected.step('a', 1)
    print(gamefield)
main()