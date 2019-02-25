import turtle
from random import randint
import math


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

        if self.locations[0] == point:
            turtle.color("red")

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
            if i == 0:
                turtle.color("red")
                # print("red")
            else:
                turtle.color("black")

            # turtle.color("red")

            self.draw_segment([self.locations[i][0], self.locations[i][1]])

    def move(self, direction):
        # move the snake in the direction given by adding a new
        # head position to the list of locations, and removing
        # the end of the snake.  The snake grows automatically every 10
        # moves.  That is, every 10 moves, the tail of the snake is not
        # removed.

        # if self.move_counter < 10:
        #     self.move_counter += 1

        # adding new locations
        if self.move_counter == 10:
            self.move_counter = 0
            self.locations.append(self.locations[len(self.locations) - 1])

        # updating locations
        if len(self.locations) > 1:
            for i in range(len(self.locations) - 1, 0, -1):
                self.update_location(
                    self.locations[i - 1][0], self.locations[i - 1][1], i)

        # moving the snake
        if direction == "right":
            self.locations[0][0] = self.locations[0][0] + self.size
        elif direction == "left":
            self.locations[0][0] = self.locations[0][0] - self.size
        elif direction == "up":
            self.locations[0][1] = self.locations[0][1] + self.size
        elif direction == "down":
            self.locations[0][1] = self.locations[0][1] - self.size


        # print(self.locations)


    def hit_self(self):
        # check if the head of the snake has hit one of its own segments
        is_hit = False
        for i in range(1, len(self.locations)):
            if (self.locations[0][0] == self.locations[i][0] and
                self.locations[0][1] == self.locations[i][1]):
                is_hit = True
                return is_hit
        return is_hit

        # pass

    def hit_bounds(self, bounds):  # left, top, right, bottom bounding box
        # check if the snake has hit the bounds given

        limit = bounds['top'] * self.size

        if (self.locations[0][0] <= limit - self.size and
            self.locations[0][1] <= limit - 2 * self.size and
            self.locations[0][0] >= -limit + 2 * self.size and
            self.locations[0][1] >= -limit + self.size):
            return False
        else:
            return True

    def update_location(self, row, col, index):
        self.locations[index] = [row, col]

    def draw_target(self, target_row, target_col):
        pass
        

class Target:
    def __init__(self, locations, bounds, snake_size, enemy_locations):
        self.bounds = bounds
        self.size = snake_size
        self.locations = locations
        self.enemy_locations = enemy_locations
        self.pos = [0,0]

    def get_pos(self):
        limit = self.bounds['top']

        self.pos[0] = randint(-limit + 2, limit - 2) * 20
        self.pos[1] = randint(-limit + 2, limit - 2) * 20

        for i in range (len(self.locations)):
            if ((self.pos[0] == self.locations[i][0] and self.pos[1] == self.locations[i][1]) or 
                (self.pos[0] == self.enemy_locations[i][0] and self.pos[1] == self.enemy_locations[i][1])):
                self.pos[0] = randint(-limit + 2, limit - 2) * 20
                self.pos[1] = randint(-limit + 2, limit - 2) * 20 

    def draw(self):
        if self.pos == [0,0]:
            self.get_pos()

        turtle.color("green")
        turtle.goto(self.pos[0], self.pos[1])
        turtle.pendown()
        turtle.begin_fill()
        turtle.goto(self.pos[0] - self.size, self.pos[1])
        turtle.goto(self.pos[0] - self.size, self.pos[1] + self.size)
        turtle.goto(self.pos[0], self.pos[1] + self.size)
        turtle.goto(self.pos[0], self.pos[1])
        turtle.end_fill()
        turtle.penup()

class Enemy_Snake(Snake):
    def __init__(self, home, size, min_dist):
        Snake.__init__(self, home, size)
        self.min_dist = min_dist


    def move(self):
        # updating locations
        if len(self.locations) > 1:
            for i in range(len(self.locations) - 1, 0, -1):
                self.update_location(self.locations[i - 1][0], self.locations[i - 1][1], i)

        #update head location
        self.min_dist()



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
        self.framework.add_tick_action(self.next_turn, 0)

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
        snake_home = (0, 0)
        enemy_snake_home = (randint(-15 + 2, 15 - 2) * 20, randint(-15 + 2, 15 - 2) * 20)
        self.snake = Snake(snake_home, self.snake_size)
        self.enemy_snake = Snake(enemy_snake_home, self.snake_size)
        self.target = Target(self.snake.locations, self.boundary_limit, self.snake_size, self.enemy_snake.locations)
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

        self.enemy_snake.move("none")

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
        self.enemy_snake.draw()
        self.target.draw()
        # print(self.snake.locations[0])
        # print(self.enemy_snake.locations[0])
        self.min_dist(self.target.pos[0], self.target.pos[1], self.enemy_snake.locations, self.snake.locations[0])


        if self.target.pos == self.snake.locations[0] or self.target.pos == self.enemy_snake.locations[0]:
            self.target.pos = [0, 0]
            self.enemy_snake.move_counter = 10
            # self.snake.move_counter = 10

        if self.snake.hit_self() or self.snake.hit_bounds(self.boundary_limit):
            self.framework.stop_game() # game over
            print(self.snake.locations)       
            print("game over")

    def min_dist(self, target_row, target_col, enemy_locations, snake_locations):
        # self.target_row = target_row
        # self.target_col = target_col
        # self.enemy_locations = enemy_locations
        # self.snake_locations = snake_locations

        # self.enemy_snake.locations[0] = [self.enemy_snake.locations[0][0] + self.snake_size, self.enemy_snake.locations[0][1]]        

        # print(enemy_locations[0][1])

        loc = [
            [enemy_locations[0][0] + self.snake_size, enemy_locations[0][1]],
            [enemy_locations[0][0] - self.snake_size, enemy_locations[0][1]],
            [enemy_locations[0][0], enemy_locations[0][1] + self.snake_size],
            [enemy_locations[0][0], enemy_locations[0][1] - self.snake_size]
        ]

        # # print(loc)

        # dist = [
        #     math.sqrt((target_row - enemy_locations[0][0] + self.snake_size) ** 2 + (target_col - enemy_locations[0][1]) ** 2),
        #     math.sqrt((target_row - enemy_locations[0][0] - self.snake_size) ** 2 + (target_col - enemy_locations[0][1]) ** 2),
        #     math.sqrt((target_row - enemy_locations[0][0]) ** 2 + (target_col - enemy_locations[0][1] + self.snake_size) ** 2),
        #     math.sqrt((target_row - enemy_locations[0][0]) ** 2 + (target_col - enemy_locations[0][1] - self.snake_size) ** 2)
        # ]
        # # print(dist.sort())

        # for i in range(3):
        #     for j in range(3):
        #         if dist[i] > dist[j + 1]:
        #             temp = loc[i]
        #             loc[i] = loc[j + 1]
        #             loc[j] = temp
        #             temp1 = dist[i]
        #             dist[i] = dist[j + 1]
        #             dist[j] = temp1
                    # temp1 = loc[i]
                    # temp2 = dist[i]
                    # dist[j] = dist[i]
                    # dist[i] = temp2
                    # loc[j] = loc[i]
                    # loc[i] = temp1

        # print(loc)

        # print(dist)
        # print("\n\n")

        # if not [enemy_locations[0][0] + self.snake_size, enemy_locations[0][1]] in enemy_locations:
        #     # dist.append( math.sqrt((target_row - enemy_locations[0][0] + self.snake_size) ** 2 + (target_col - enemy_locations[0][1]) ** 2))
        #     ls.append(1)
        # if not [enemy_locations[0][0] - self.snake_size, enemy_locations[0][1]] in enemy_locations:
        #     # dist.append(math.sqrt((target_row - enemy_locations[0][0] - self.snake_size) ** 2 + (target_col - enemy_locations[0][1]) ** 2))
        #     ls.append(2)
        # if not [enemy_locations[0][0], enemy_locations[0][1] + self.snake_size] in enemy_locations:
        #     # dist.append(math.sqrt((target_row - enemy_locations[0][0]) ** 2 + (target_col - enemy_locations[0][1] + self.snake_size) ** 2))
        #     ls.append(3)
        # if not [enemy_locations[0][0], enemy_locations[0][1] - self.snake_size] in enemy_locations:
        #     # dist.append(math.sqrt((target_row - enemy_locations[0][0]) ** 2 + (target_col - enemy_locations[0][1] - self.snake_size) ** 2))
        #     ls.append(4)
        
        # maxIndex = dist.index(max(dist))

        # if maxIndex:
        #     pass

        dist = [0,0,0,0]


        dist[0] = math.sqrt((target_row - enemy_locations[0][0] + self.snake_size) ** 2 + (target_col - enemy_locations[0][1]) ** 2)
        dist[1] = math.sqrt((target_row - enemy_locations[0][0] - self.snake_size) ** 2 + (target_col - enemy_locations[0][1]) ** 2)
        dist[2] = math.sqrt((target_row - enemy_locations[0][0]) ** 2 + (target_col - enemy_locations[0][1] + self.snake_size) ** 2)
        dist[3] = math.sqrt((target_row - enemy_locations[0][0]) ** 2 + (target_col - enemy_locations[0][1] - self.snake_size) ** 2)
        
        minIndex = dist.index(max(dist))

        # dist.sort()
        # dist.reverse()


        # for i in range(4):
            # if not loc[i] in enemy_locations:
                # enemy_locations[0] = loc[0]
        #         return

        while True:
            for i in range(len(dist)):
                if i == minIndex:
                    if not loc[i] in enemy_locations:
                        enemy_locations[0] = loc[i]
                        return
                        # dist = [0,0,0,0]
                    else:
                        dist.pop(i)
                        loc.pop(i)
                        # print(dist)
                        if len(dist) == 0:
                            self.framework.stop_game()
                            return
                        minIndex = dist.index(max(dist))
                    break


        # if minIndex == 0:
        #     if not [enemy_locations[0][0] + self.snake_size, enemy_locations[0][1]] in enemy_locations:
        #         enemy_locations[0] = [enemy_locations[0][0] + self.snake_size, enemy_locations[0][1]]
        # if minIndex == 1:
        #     # if not [enemy_locations[0][0] - self.snake_size, enemy_locations[0][1]] in enemy_locations:
        #         enemy_locations[0] = [enemy_locations[0][0] - self.snake_size, enemy_locations[0][1]]
        # if minIndex == 2:
        #     # if not [enemy_locations[0][0], enemy_locations[0][1] + self.snake_size] in enemy_locations:
        #         enemy_locations[0] = [enemy_locations[0][0], enemy_locations[0][1] + self.snake_size]            
        # if minIndex == 3:
        #     # if not [enemy_locations[0][0], enemy_locations[0][1] - self.snake_size] in enemy_locations:
        #         enemy_locations[0] = [enemy_locations[0][0], enemy_locations[0][1] - self.snake_size]
            


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
