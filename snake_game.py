'''
Game Description
valid coordinate : ([0, 380], [0, 380])
pygame 좌표가 x축 방향은 똑같은데 y축 방향이 반대에 주의!
'''
import pygame
from pygame.locals import *
import random, time

class Snake():

    def __init__(self, x, y):
        self.x = x # head
        self.y = y # head
        self.length = 1
        self.go = 100
        self.gone = 100
        self.edible = False
        self.space = [(self.x, self.y)] # queue
        self.rect = []
        self.surf = []
        self.gene = [] # FIXME
        self.wall = None
        self.prey = None
    
    def update(self, delta_x=None, delta_y=None, prey_x=None, prey_y=None):
        if delta_x is not None:
            self.x += delta_x
        if delta_y is not None:
            self.y += delta_y
        self.space.insert(0, (self.x, self.y))
        if not self.edible:
            self.space.pop()
        elif self.edible:
            self.edible = False
        self.wall = ((self.x - 0) / STEP, (self.x - SCREEN_SIZE + SIZE) / STEP, 
                    (self.y - 0) / STEP, (self.y - SCREEN_SIZE + SIZE) / STEP)
        self.prey = ((prey_x - self.x) / STEP, (prey_y - self.y) / STEP)
    
    def where(self):
        print(self.length, self.space, self.wall)
    
    def move(self):
        self.rect = []
        self.surf = []
        for idx, sp in enumerate(self.space):
            self.rect.append(pygame.Rect((sp[0], sp[1]), (SIZE, SIZE)))
            self.surf.append(pygame.Surface((SIZE, SIZE)))
            if idx == 0:
                self.surf[idx].fill(GREEN)
            elif idx == len(self.space) - 1:
                self.surf[idx].fill(BLUE)
            else:
                self.surf[idx].fill(WHITE)

    def eat(self):
        self.length += 1
        self.edible = True


# hyperparameter control (GAME)
## screen and objects
SCREEN_SIZE = 400
FPS = 60 # how many frames we update per second.
SIZE = 20
STEP = 20
INIT_POS_X = 20 * random.randint(0, 19)
INIT_POS_Y = 20 * random.randint(0, 19)
## colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
## others
START = True
# hyperparameter control (Neural Network)
## TODO

# pygame initialization
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
assert not failures, "pygame initialization error"

# screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('snake game')
clock = pygame.time.Clock()

# objects
snake = Snake(INIT_POS_X, INIT_POS_Y)

snakeRect = pygame.Rect((INIT_POS_X, INIT_POS_Y), (SIZE, SIZE))
snakeSurf = pygame.Surface((SIZE, SIZE))
snakeSurf.fill(GREEN)

preySurf = pygame.Surface((SIZE, SIZE))
preySurf.fill(RED)

# game operation
while True:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snakeRect.move_ip(0, -STEP) # changes the snakeRect's position
                snake.update(delta_y=-STEP, prey_x=prey_x, prey_y=prey_y)
                snake.go = 1
                snake.where()

            elif event.key == pygame.K_DOWN:
                snakeRect.move_ip(0, STEP)
                snake.update(delta_y=STEP, prey_x=prey_x, prey_y=prey_y)
                snake.go = -1
                snake.where()

            elif event.key == pygame.K_LEFT:
                snakeRect.move_ip(-STEP, 0)
                snake.update(delta_x=-STEP, prey_x=prey_x, prey_y=prey_y)
                snake.go = -2
                snake.where()

            elif event.key == pygame.K_RIGHT:
                snakeRect.move_ip(STEP, 0)
                snake.update(delta_x=STEP, prey_x=prey_x, prey_y=prey_y)
                snake.go = 2
                snake.where()

            elif event.key == pygame.K_ESCAPE:
                quit()

    # game end rule
    if (not 0 <= snake.x <= (SCREEN_SIZE - SIZE)) or (not 0 <= snake.y <= (SCREEN_SIZE - SIZE)):
        print('out of boundary')
        quit()
    elif (snake.x, snake.y) in snake.space[1:]  or (snake.length > 1 and snake.go + snake.gone == 0):
        print('it\'s you!')
        quit()
    elif snake.length == 400:
        print('you win!')
        quit()

    # prey
    if START == True or (prey_x, prey_y) == (snake.x, snake.y):
        prey_x = SIZE * random.randint(0, int((SCREEN_SIZE - SIZE) / STEP))
        prey_y = SIZE * random.randint(0, int((SCREEN_SIZE - SIZE) / STEP))
        while (prey_x, prey_y) in snake.space:
            prey_x = SIZE * random.randint(0, int((SCREEN_SIZE - SIZE) / STEP))
            prey_y = SIZE * random.randint(0, int((SCREEN_SIZE - SIZE) / STEP))
        preyRect = pygame.Rect((prey_x, prey_y), (SIZE, SIZE))
        
        if START:
            START = False
        elif not START:
            snake.eat()

    # update direction of snake
    snake.gone = snake.go

    screen.fill(BLACK)
    screen.blit(snakeSurf, snakeRect)
    snake.move()
    for surf, rect in zip(snake.surf, snake.rect):
        screen.blit(surf, rect)
    screen.blit(preySurf, preyRect)
    pygame.display.update()