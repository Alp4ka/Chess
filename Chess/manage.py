from GameField import *
from Figure import *
from Utils import convert_column_to_digit


class Codes(Enum):
    BACK = -1
    EXIT = -2


class Manager:
    COMMANDS = ["exit", "move", "help", "undo", "unit", "back", "castle"]

    def __init__(self):
        self.game_field: GameField = GameField()
        self.game_over = False

    def print(self):
        print(self.game_field)
        print()

    def castle(self):
        if isinstance(self.game_field.selected, Figure.Rook):
            try:
                self.game_field.selected.castle()
            except ValueError:
                print("Ладья не может провести рокировку с королём")
        else:
            print("Чтобы провести рокировку нужно выбрать ладью")

    def get_position_with_context(self, context):
        print(context)
        data = input()

        if len(data) != 0:
            if data == "exit":
                return Codes.EXIT, Codes.EXIT
            if data == "back":
                return Codes.BACK, Codes.BACK

        while True:
            try:
                column, row = data[0], data[1]
                column = convert_column_to_digit(data[0])
                row = convert_column_to_digit(int(row)-1)
                return column, row
            except:
                print("Введена неправильная позиция, повторите ввод или введите <exit> для выхода")
                data = input()
                if len(data) != 0:
                    if data == "exit":
                        return Codes.EXIT, Codes.EXIT
                    if data == "back":
                        return Codes.BACK, Codes.BACK

    def turn(self):
        self.game_field.clean_empty()
        self.game_field.switch_turn()
        self.game_field.current_step += 1
        self.save_game_state()
        self.game_field.selected = None
        self.game_field.check['white'] = self.game_field.is_checked(Fraction.WHITE)
        self.game_field.check['black'] = self.game_field.is_checked(Fraction.BLACK)

    def choose_unit(self):
        self.game_field.clean_empty()
        column, row = self.get_position_with_context("Выберите фигуру")

        if column == Codes.EXIT:
            self.exit()
            return
        if column == Codes.BACK:
            return

        try:
            self.game_field.select_unit(column, row)
        except ValueError:
            print("На данной позиции нет фигуры")
        return

    def move(self):
        while True:
            column, row = self.get_position_with_context("Введите позицию, куда переместить фигуру")

            if column == Codes.EXIT:
                self.exit()
                return False
            if column == Codes.BACK:
                return
            try:
                self.game_field.selected.move_or_attack(column, row)
                self.turn()
                return True
            except ValueError:
                print("Данный ход недоступен, введите другую позицию или введите <exit> для выхода")
            except AttributeError:
                print("Для начала выберите фигуру")

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

    def undo(self):
        try:
            self.game_field.undo()
        # Теоритически, эта штука теперь никогда не случится, но на всякий случай пусть пока будет
        except IndexError:
            print("Невозможно вернуться назад, буфер пустой")

    def check_mate(self):
        for elem in self.game_field.eaten[Fraction.WHITE.value]:
            if isinstance(elem, King):
                print("!!! ПОБЕДА БЕЛЫХ !!!")
                self.game_over = True
        for elem in self.game_field.eaten[Fraction.BLACK.value]:
            if isinstance(elem, King):
                print("!!! ПОБЕДА ЧЕРНЫХ !!!")
                self.game_over = True

    def update(self):
        # Костыль на костыле
        while not self.game_over:
            if DEBUG:
                print("STEP IS: ", self.game_field.current_step)
            self.check_mate()
            if self.game_over:
                self.print()
                break
            self.print()
            command = self.get_command()

            if command == "help":
                self.help()
            elif command == "unit":
                self.choose_unit()
            elif command == "move":
                self.move()
            elif command == "castle":
                self.castle()
            elif command == "undo":
                self.undo()
            elif command == "exit":
                self.exit()
                break
            self.game_field.check_all_in_danger(self.game_field.turn)

    @staticmethod
    def help():
        to_print = "'Консольные шахматы'\n" \
                   "Давай познакомлю тебя с интерфейсом: \n" \
                   "1) Перед собой ты видишь игровое поле, где '.' обозначает свободную ячейку.\n" \
                   "2) Сверху, слева, снизу, справа отображаются буквы и цифры для облегчения процесса\n" \
                   "ориентации на поле.\n" \
                   "3) Буквы внутри квадрата поля обозначают фигуры. Большие буквы - фигуры белых, маленькие - черных.\n" \
                   "K - король, Q - королева, R - ладья, N - конь, B - слон, P - пешка\n" \
                   "\n" \
                   "Теперь подробнее про команды:\n" \
                   "1) unit - выбирает фигуру.\n" \
                   "2) move - двигает фигуру, которую выделили командой unit.\n" \
                   "3) undo - возвращает на ход назад.\n" \
                   "4) castle - Проводит рокировку короля с выбранной unit'ом ладьей.\т" \
                   "5) back - выйти из move.\n" \
                   "6) exit - закончить игру.\n" \
                   "\n" \
                   "Пример последовательности команд:\n" \
                   "unit\n" \
                   "a2\n" \
                   "move\n" \
                   "a4\n" \
                   "unit\n" \
                   "a8\n" \
                   "castle\n" \
                   "undo\n" \
                   "move\n" \
                   "back\n\n" \
                   "Удачи на поле битвы!\n"
        print(to_print)

    def exit(self):
        self.game_over = True
        print("Game over!")


def main():
    manager = Manager()
    manager.update()


main()