import keyboard
import os
import random

COLS = 25
ROWS = 10
EMPTY = '☐'
PLAYER = 'P'
ANT = 'a'
ANTHILL = 'A'
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'
ANTHILL_MAX = 4
ANTHILL_MINI = 1


class GameObject:
    def __init__(self, y, x, image):
        self.y = y
        self.x = x
        self.image = image

    def move(self, direction, field):
        new_y, new_x = self.y, self.x

        if direction == UP and self.y > 0 and not isinstance(field.cells[self.y - 1][self.x].content, Anthill):
            new_y -= 1
        elif direction == DOWN and self.y < field.rows - 1 and not isinstance(field.cells[self.y + 1][self.x].content, Anthill):
            new_y += 1
        elif direction == LEFT and self.x > 0 and not isinstance(field.cells[self.y][self.x - 1].content, Anthill):
            new_x -= 1
        elif direction == RIGHT and self.x < field.cols - 1 and not isinstance(field.cells[self.y][self.x + 1].content, Anthill):
            new_x += 1

        field.cells[self.y][self.x].content = None
        self.y, self.x = new_y, new_x
        field.cells[self.y][self.x].content = self

    def place(self, field):
        if field.cells[self.y][self.x].content is None:
            field.cells[self.y][self.x].content = self
        else:
            empty_cells = [(i, j) for i in range(field.rows) for j in range(field.cols) if field.cells[i][j].content is None]
            if empty_cells:
                new_y, new_x = random.choice(empty_cells)
                field.cells[new_y][new_x].content = self
                self.y, self.x = new_y, new_x

    def draw(self, field):
        field.cells[self.y][self.x].content = self


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


class Player(GameObject):
    def __init__(self, y=None, x=None):
        super().__init__(y, x, PLAYER)

    def move(self, direction, field):
        super().move(direction, field)


class Anthill(GameObject):
    def __init__(self, x, y, quantity):
        super().__init__(y, x, ANTHILL)
        self.quantity = quantity

    def place(self, field):
        super().place(field)

    def draw(self, field):
        super().draw(field)


class Field:
    def __init__(self, cell=Cell, player=Player, anthill=Anthill):
        self.rows = ROWS
        self.cols = COLS
        self.anthills = []
        self.cells = [[cell(Y=y, X=x) for x in range(COLS)] for y in range(ROWS)]
        self.player = player(y=random.randint(0, ROWS - 1), x=random.randint(0, COLS - 1))
        self.player.place(self)
        self.player.draw(self)
        
    def drawrows(self):
        for row in self.cells:
            for cell in row:
                cell.draw()
            print()

    def add_anthill(self, anthill):
        self.anthills.append(anthill)
        anthill.place(self)

    def add_anthills_randomly(self):
        available_cells = [(x, y) for x in range(self.cols) for y in range(self.rows) if (x, y) != (self.player.x, self.player.y)]

        quantity = random.randint(ANTHILL_MINI, ANTHILL_MAX)
        
        for i in range(quantity):
            if not available_cells:
                break
            anthill_x, anthill_y = random.choice(available_cells)
            available_cells.remove((anthill_x, anthill_y))

            anthill = Anthill(x=anthill_x, y=anthill_y, quantity=random.randint(ANTHILL_MINI, ANTHILL_MAX))
            self.add_anthill(anthill)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Game:
    def __init__(self):
        self.field = Field()
        self.field.add_anthills_randomly()

    def handle_keyboard_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == UP:
                self.field.player.move(UP, self.field)
            elif event.name == DOWN:
                self.field.player.move(DOWN, self.field)
            elif event.name == LEFT:
                self.field.player.move(LEFT, self.field)
            elif event.name == RIGHT:
                self.field.player.move(RIGHT, self.field)
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
