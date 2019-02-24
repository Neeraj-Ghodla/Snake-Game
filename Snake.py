import turtle


class Snake:
    # The snake moves by jumping one square at a time.
    def __init__(self, home, size):
        # home is the starting location (by default is 0, 0)
        # size is the size of the square in each cell of the snake
        # The snake location is stored as a list of tuples, where each tuple
        # is the position of a segment of the snake
        self.home = home
        self.size = size
        self.move_counter = 0
        self.locations = [[self.home[0], self.home[1]]]

    def draw_segment(self, point):
        # Draws a square equal to the size of the snake, where the location
        # given is the bottom left corner of the square
        turtle.goto(point[0], point[1])
        turtle.pendown()
        turtle.begin_fill()
        turtle.goto(point[0] - self.size, point[1])
        turtle.goto(point[0] - self.size, point[1] + self.size)
        turtle.goto(point[0], point[1] + self.size)
        turtle.goto(point[0], point[1])
        turtle.end_fill()
        turtle.penup()

    def draw(self):
        # Draws each of the segments, and then draws the head with red colour
        for i in range(len(self.locations)):
            self.draw_segment([self.locations[i][0], self.locations[i][1]])

    def move(self, direction):
        # move the snake in the direction given by adding a new
        # head position to the list of locations, and removing
        # the end of the snake.  The snake grows automatically every 10
        # moves.  That is, every 10 moves, the tail of the snake is not
        # removed.

        #adding new locations

        if self.move_counter < 10:
            self.move_counter += 1

        if self.move_counter == 10:
            self.move_counter = 0
            self.locations.append(self.locations[len(self.locations) - 1])

        #updating locations
        if len(self.locations) > 1:
            for i in range(len(self.locations) - 2, 0, -1):
                self.update_location(self.locations[i][0], self.locations[i][1], i + 1)

        #moving the snake
        if direction == "right":
            self.locations[0][0] = self.locations[0][0] + self.size
        elif direction == "left":
            self.locations[0][0] = self.locations[0][0] - self.size
        elif direction == "up":
            self.locations[0][1] = self.locations[0][1] + self.size
        else:
            self.locations[0][1] = self.locations[0][1] - self.size


    def hit_self(self):
        # check if the head of the snake has hit one of its own segments
        pass

    def hit_bounds(self, bounds):  # left, top, right, bottom bounding box
        # check if the snake has hit the bounds given
        if self.home[0] <= 280 and self.home[1] <= 280 and self.home[0] > -280 and self.home[1] > -280:
            return False
        else:
            return True

    def update_location(self, row, col, index):
        self.locations[index] = [row, col]


class SnakeGame:
    def __init__(self):
        # set up the window for the game, the methods that are called when keys are pressed, and
        # the method that is called each new game turn
        self.framework = GameFramework(800, 800, 'COMPSCI 130 Project')
        self.framework.add_key_action(self.move_right, 'Right')
        self.framework.add_key_action(self.move_up, 'Up')
        self.framework.add_key_action(self.move_down, 'Down')
        self.framework.add_key_action(self.move_left, 'Left')
        # Pressing space will restart the game
        self.framework.add_key_action(self.setup_game, ' ')
        # Delay (speed) is 100.  Smaller is faster.
        self.framework.add_tick_action(self.next_turn, 100)

    # set of methods to keep track of which key was most recently pressed
    def move_right(self):
        self.last_key = 'Right'

    def move_left(self):
        self.last_key = 'Left'

    def move_down(self):
        self.last_key = 'Down'

    def move_up(self):
        self.last_key = 'Up'

    def setup_game(self):
        # initializes starting variables and begins the animation loop
        self.last_key = 'None'  # No initial direction specified
        self.snake_size = 20
        self.boundary_limit = {'left': -15,
                               'right': 15, 'top': 15, 'bottom': -15}
        snake_home = [0, 0]
        self.snake = Snake(snake_home, self.snake_size)
        self.framework.start_game()

    def draw_bounds(self):
        # draws the box that defines the limit for the snake
        left = self.boundary_limit['left']
        top = self.boundary_limit['top']
        size = self.snake_size
        turtle.goto(left * size, top * size)
        turtle.pendown()
        for i in range(0, 4):  # Draw a bounding square
            turtle.rt(90)
            turtle.forward(abs(left) * size * 2)
        turtle.penup()

    def next_turn(self):
        # called each time the game 'ticks'
        turtle.clear()
        # snake = self.snake
        if self.last_key == 'Right':
            self.snake.move('right')
        if self.last_key == 'Up':
            self.snake.move('up')
        if self.last_key == 'Down':
            self.snake.move('down')
        if self.last_key == 'Left':
            self.snake.move('left')
        self.draw_bounds()
        self.snake.draw()
        if self.snake.hit_self() or self.snake.hit_bounds(self.boundary_limit):
            self.framework.stop_game()
            print(self.snake.locations)  # game over
            print("game over")

    def start(self):
        # starts the game
        self.setup_game()  # set up the game.
        turtle.mainloop()  # must appear last.


# Shouldn't need to edit this at all
class GameFramework:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.game_running = False
        self.tick = None  # function to call for each animation cycle
        self.delay = 100  # default is .1 second.
        turtle.title(title)  # title for the window
        turtle.setup(width, height)  # set window display
        turtle.hideturtle()  # prevent turtle appearance
        turtle.tracer(False)  # prevent turtle animation
        turtle.listen()  # set window focus to the turtle window
        turtle.mode('logo')  # set 0 direction as straight up
        turtle.penup()  # don't draw anything
        self.__animation_loop()

    def start_game(self):
        self.game_running = True

    def stop_game(self):
        self.game_running = False

    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func, delay):
        self.tick = func
        self.delay = delay

    def __animation_loop(self):
        if self.game_running:
            self.tick()
        turtle.ontimer(self.__animation_loop, self.delay)


g = SnakeGame()
g.start()
