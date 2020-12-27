from GameField import *
from Figure import *
from Utils import convert_column_to_digit

class Manager:

    COMMANDS = ["exit", "move", "help", "back", "unit"]
    def __init__(self):
        self.game_field:GameField = GameField()
        self.game_field.save()
        self.game_over = False
    def print(self):
        print(self.game_field)
        print()

    def get_position_with_context(self, context):
        print(context)

        data = input().split()

        if data[0] == "exit":
            return -1, -1

        column = row = 0
        while True:
            column, row = data[0], data[1]

            try:
                column = convert_column_to_digit(data[0])
                row = convert_column_to_digit(int(row))
                return column, row
            except ValueError:
                print("Введена неправильная позиция, повторите ввод или введите <exit> для выхода")
                data = input().split()
                if data[0] == "exit":
                    return -1, -1

    def turn(self):
        self.save_game_state()
        self.game_field.current_step += 1
        self.game_field.switch_turn()

    def choose_unit(self):
        column, row = self.get_position_with_context("Выберите фигуру")

        if column == -1:
            self.exit()
            return False

        try:
            self.game_field.select_unit(column, row)
        except ValueError:
            print("На данной позиции нет фигуры")
            return False
        return True

    def move(self):
        while True:
            column, row = self.get_position_with_context("Введите позицию, куда переметить фигуру")

            if column == -1:
                self.exit()
                return False

            try:
                self.game_field.selected.move_or_attack(column, row)
                self.turn()
                return True
            except ValueError:
                print("Данный ход недоступен, введите другую позицию или введите <exit> для выхода")

    def save_game_state(self):
        self.game_field.save()

    def get_command(self):
        while True:
            print("Введите команду (Для просмотра всех доступных команд введите <help>")
            data = input()
            if data not in self.COMMANDS:
                print("Такой команды не существует, вы можете посмотреть список всех доступных команд введя <help>")
            else:
                return data

    def update(self):
        # Костыль на костыле
        while not self.game_over:
            self.print()
            command = self.get_command()

            if command == "help":
                self.help()
            elif command == "unit":
                if not self.choose_unit():
                    continue
            elif command == "move":
                if not self.move():
                    continue
            elif command == "back":
                pass
            elif command == "exit":
                self.exit()
                break

    def help(self):
        raise NotImplementedError()

    def exit(self):
        self.game_over = True
        print("Game over bitch")

def main():

    manager = Manager()

    manager.update()
    #gamefield = GameField()
    # print(gamefield)
    # print()
    #
    # gamefield.select_unit('a', 1)
    # print(gamefield)
    # print()
    #
    # gamefield.selected.move_or_attack('a', 2)
    # gamefield.current_step += 1
    # gamefield.save()
    #
    #
    # print(gamefield)
    # print()
    #
    # gamefield.select_unit('a', 2)
    # print(gamefield)
    # print()
    # gamefield.selected.move_or_attack('a', 3)
    # gamefield.current_step += 1
    # gamefield.save()
    #
    # gamefield.select_unit('b', 1)
    # gamefield.undo()
    # print(gamefield)
    # print()
    #
    # gamefield.undo()
    # print(gamefield)
    # print()
    #
    # gamefield.select_unit('b', 1)
    # print(gamefield)
    # print()
main()