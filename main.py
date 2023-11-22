import keyboard
import os
import random

COLS = 25
ROWS = 10
EMPTY = '☐'
PLAYER = 'P'
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
    def __init__(self, Y=None, X=None):
        self.image = ANT
        self.Y = Y
        self.X = X

    def move_away_from_player(self, player, field):
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
    def __init__(self, cell=Cell, player=Player, ant=Ant):
        self.rows = ROWS
        self.cols = COLS
        self.cells = [[cell(Y=y, X=x) for x in range(COLS)] for y in range(ROWS)]
        self.player = player(Y=random.randint(0, ROWS - 1), X=random.randint(0, COLS - 1))
        self.ant = ant(Y=random.randint(0, ROWS - 1), X=random.randint(0, COLS - 1))
        self.cells[self.player.Y][self.player.X].content = self.player
        self.cells[self.ant.Y][self.ant.X].content = self.ant

    def drawrows(self):
        for row in self.cells:
            for cell in row:
                cell.draw()
            print()

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class Game:
    def __init__(self):
        self.field = Field()

    def handle_keyboard_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'up':
                self.field.player.move('up', self.field)
                self.field.ant.move_away_from_player(self.field.player, self.field)
            elif event.name == 'down':
                self.field.player.move('down', self.field)
                self.field.ant.move_away_from_player(self.field.player, self.field)
            elif event.name == 'left':
                self.field.player.move('left', self.field)
                self.field.ant.move_away_from_player(self.field.player, self.field)
            elif event.name == 'right':
                self.field.player.move('right', self.field)
                self.field.ant.move_away_from_player(self.field.player, self.field)
            elif event.name == 'esc':
                print("Выход из игры.")
                return True
            return False

    def update_game_state(self):
        clear_screen()
        self.field.drawrows()

    def run(self):
        self.field.drawrows()

        while True:
            event = keyboard.read_event(suppress=True)
            if self.handle_keyboard_event(event):
                break

            self.update_game_state()

game_instance = Game()
game_instance.run()
