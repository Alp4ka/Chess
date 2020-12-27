from GameField import *
from Figure import *
from Utils import convert_column_to_digit

split = "+---------------+"
def main():
    gamefield = GameField()
    print(gamefield)
    '''gamefield.set_item(row=6, column='d', value=Queen(field=gamefield,
                                                               x_pos=3,
                                                               y_pos=6,
                                                              fraction = Fraction.WHITE,
                                                             is_alive = True))'''
    #gamefield.select_unit('h', 0)
    #gamefield.selected.move_or_attack('d', 7)
    #gamefield.selected.castle()
    #amefield.clean_empty()
    print(gamefield)



main()