import keyboard
import os
import random

COLS = 25
ROWS = 10
EMPTY = '☐'
PLAYER = 'P'
ANT = 'a'

class Cell:
    """
    Класс Cell представляет отдельную ячейку на игровом поле.

    Attributes:
        image (str): Символ, представляющий изображение ячейки.
        Y (int): Координата Y ячейки на поле.
        X (int): Координата X ячейки на поле.
        content (object): Содержимое ячейки, такое как игрок или муравей.
    """

    def __init__(self, Y=None, X=None):
        """
        Инициализация объекта Cell.

        Parameters:
            Y (int): Координата Y ячейки на поле.
            X (int): Координата X ячейки на поле.
        """
        self.image = EMPTY
        self.Y = Y
        self.X = X
        self.content = None

    def draw(self):
        """
        Отображение содержимого ячейки.
        Если ячейка пуста, отображается символ EMPTY, иначе отображается символ содержимого.
        """
        if self.content:
            print(self.content.image, end=' ')
        else:
            print(self.image, end=' ')


class Player:
    """
    Класс Player представляет игрока на поле.

    Attributes:
        image (str): Символ, представляющий изображение игрока.
        Y (int): Координата Y игрока на поле.
        X (int): Координата X игрока на поле.
    """

    def __init__(self, Y=None, X=None):
        """
        Инициализация объекта Player.

        Parameters:
            Y (int): Координата Y игрока на поле.
            X (int): Координата X игрока на поле.
        """
        self.image = PLAYER
        self.Y = Y
        self.X = X

    def move(self, direction, field):
        """
        Перемещение игрока на поле в указанном направлении.

        Parameters:
            direction (str): Направление движения ('up', 'down', 'left', 'right').
            field (Field): Объект поля, на котором находится игрок.
        """
        new_Y, new_X = self.Y, self.X

        if direction == 'up' and self.Y > 0:
            new_Y -= 1
        elif direction == 'down' and self.Y < field.rows - 1:
            new_Y += 1
        elif direction == 'left' and self.X > 0:
            new_X -= 1
        elif direction == 'right' and self.X < field.cols - 1:
            new_X += 1

        if field.cells[new_Y][new_X].content is None:
            field.cells[self.Y][self.X].content = None
            self.Y, self.X = new_Y, new_X
            field.cells[self.Y][self.X].content = self


class Ant:
    """
    Класс Ant представляет муравья на поле.

    Attributes:
        image (str): Символ, представляющий изображение муравья.
        Y (int): Координата Y муравья на поле.
        X (int): Координата X муравья на поле.
    """

    def __init__(self, Y=None, X=None):
        """
        Инициализация объекта Ant.

        Parameters:
            Y (int): Координата Y муравья на поле.
            X (int): Координата X муравья на поле.
        """
        self.image = ANT
        self.Y = Y
        self.X = X

    def move_away_from_player(self, player, field):
        """
        Движение муравья в противоположном направлении относительно игрока.

        Parameters:
            player (Player): Объект игрока на поле.
            field (Field): Объект поля, на котором находится муравей.
        """
        directions = ['up', 'down', 'left', 'right']
        opposite_directions = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }

        direction = random.choice(directions)
        player_distance = abs(player.Y - self.Y) + abs(player.X - self.X)
        new_Y, new_X = self.Y, self.X

        while True:
            if direction == 'up' and new_Y > 0:
                new_Y -= 1
            elif direction == 'down' and new_Y < field.rows - 1:
                new_Y += 1
            elif direction == 'left' and new_X > 0:
                new_X -= 1
            elif direction == 'right' and new_X < field.cols - 1:
                new_X += 1

            new_distance = abs(player.Y - new_Y) + abs(player.X - new_X)
            if new_distance >= player_distance:
                break

            direction = opposite_directions[direction]

        if field.cells[new_Y][new_X].content is None:
            field.cells[self.Y][self.X].content = None
            self.Y, self.X = new_Y, new_X
            field.cells[self.Y][self.X].content = self

class Field:
    """
    Класс Field представляет игровое поле.

    Attributes:
        rows (int): Количество строк на поле.
        cols (int): Количество столбцов на поле.
        cells (list): Двумерный список объектов Cell, представляющих ячейки поля.
        player (Player): Объект игрока на поле.
        ant (Ant): Объект муравья на поле.
    """

    def __init__(self, cell=Cell, player=Player, ant=Ant):
        """
        Инициализация объекта Field.

        Parameters:
            cell (Cell): Класс, представляющий ячейку на поле.
            player (Player): Класс, представляющий игрока на поле.
            ant (Ant): Класс, представляющий муравья на поле.
        """
        self.rows = ROWS
        self.cols = COLS
        self.cells = [[cell(Y=y, X=x) for x in range(COLS)] for y in range(ROWS)]
        self.player = player(Y=random.randint(0, ROWS - 1), X=random.randint(0, COLS - 1))
        self.ant = ant(Y=random.randint(0, ROWS - 1), X=random.randint(0, COLS - 1))
        self.cells[self.player.Y][self.player.X].content = self.player
        self.cells[self.ant.Y][self.ant.X].content = self.ant

    def drawrows(self):
        """
        Отображение всех строк игрового поля.
        """
        for row in self.cells:
            for cell in row:
                cell.draw()
            print()


def clear_screen():
    """
    Очистка экрана консоли, учитывая операционную систему.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Game:
    """
    Класс Game представляет игровой процесс.

    Attributes:
        field (Field): Объект игрового поля.
    """

    def __init__(self):
        """
        Инициализация объекта Game.
        """
        self.field = Field()

    def run(self):
        """
        Запуск игрового процесса.
        """
        self.field.drawrows()

        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'up':
                    self.field.player.move('up', self.field)
                    self.field.ant.move_away_from_player(self.field.player, self.field)
                    clear_screen()
                    self.field.drawrows()
                elif event.name == 'down':
                    self.field.player.move('down', self.field)
                    self.field.ant.move_away_from_player(self.field.player, self.field)
                    clear_screen()
                    self.field.drawrows()
                elif event.name == 'left':
                    self.field.player.move('left', self.field)
                    self.field.ant.move_away_from_player(self.field.player, self.field)
                    clear_screen()
                    self.field.drawrows()
                elif event.name == 'right':
                    self.field.player.move('right', self.field)
                    self.field.ant.move_away_from_player(self.field.player, self.field)
                    clear_screen()
                    self.field.drawrows()
                    

game_instance = Game()
game_instance.run()
