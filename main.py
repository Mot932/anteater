import keyboard
import os
import random
import time

COLS = 25
ROWS = 10
EMPTY = '☐'
PLAYER = 'P'
ANTHILL = 'A'
ANT = 'a'

class Cell:
    def __init__(self, Y=None, X=None):
        self.image = EMPTY
        self.Y = Y
        self.X = X
        self.content = None

    def draw(self):
        if self.content:
            print(self.content.image, end=' ')
        else:
            print(self.image, end=' ')


class Player:
    def __init__(self, Y=None, X=None):
        self.image = PLAYER
        self.Y = Y
        self.X = X

    def move(self, direction, field):
        new_Y, new_X = self.Y, self.X

        if direction == 'up' and self.Y > 0 and field.cells[self.Y - 1][self.X].content != Anthill:
            new_Y -= 1
        elif direction == 'down' and self.Y < field.rows - 1 and field.cells[self.Y + 1][self.X].content != Anthill:
            new_Y += 1
        elif direction == 'left' and self.X > 0 and field.cells[self.Y][self.X - 1].content != Anthill:
            new_X -= 1
        elif direction == 'right' and self.X < field.cols - 1 and field.cells[self.Y][self.X + 1].content != Anthill:
            new_X += 1

        if field.cells[new_Y][new_X].content is None:
            field.cells[self.Y][self.X].content = None
            self.Y, self.X = new_Y, new_X
            field.cells[self.Y][self.X].content = self


class Anthill:
    def __init__(self, Y=None, X=None):
        self.image = ANTHILL
        self.Y = Y
        self.X = X

    def spawn_ant(self, field):
        ant = Ant(self.Y, self.X)
        field.cells[self.Y][self.X].content = ant
        return ant


class Ant:
    def __init__(self, Y=None, X=None):
        self.image = ANT
        self.Y = Y
        self.X = X

    def move_away_from_player(self, player, field):
        directions = ['up', 'down', 'left', 'right']
        random.shuffle(directions)

        for direction in directions:
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
                break


class Field:
    def __init__(self, cell=Cell, player=Player, anthill=Anthill, ant=Ant):
        self.rows = ROWS
        self.cols = COLS
        self.cells = [[cell(Y=y, X=x) for x in range(COLS)] for y in range(ROWS)]
        self.player = player(Y=random.randint(0, ROWS - 1), X=random.randint(0, COLS - 1))
        self.anthill = anthill(Y=random.randint(0, ROWS - 1), X=random.randint(0, COLS - 1))
        self.cells[self.player.Y][self.player.X].content = self.player
        self.cells[self.anthill.Y][self.anthill.X].content = self.anthill

    def drawrows(self):
        for row in self.cells:
            for cell in row:
                cell.draw()
            print()


class Game:
    def __init__(self):
        self.field = Field()

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def run(self):
        self.clear_screen()
        self.field.drawrows()

        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'up' or event.name == 'down' or event.name == 'left' or event.name == 'right':
                    self.field.player.move(event.name, self.field)

                    if random.random() < 0.2:  # 20% chance to spawn an ant
                        ant = self.field.anthill.spawn_ant(self.field)
                        time.sleep(0.5)  # Delay to avoid spawning multiple ants at once
                        ant.move_away_from_player(self.field.player, self.field)

                self.clear_screen()
                self.field.drawrows()


# Create an instance of the Game class and run the game loop
my_game = Game()
my_game.run()
