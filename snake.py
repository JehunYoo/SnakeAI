'''
snake game module
valid coordinate : ([0, 380], [0, 380])
'''
import pygame
from pygame.locals import *
import random, time
import queue

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
assert not failures, "pygame initialization error"

# hyperparameter control (GAME)
## screen and objects
SCREEN_SIZE = 400
FPS = 60 # how many frames we update per second.
SIZE = 20
STEP = 20
## colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Snake():

    def __init__(self, gnn):
        # snake
        self.x = 20 * random.randint(0, 19) # x head of snake
        self.y = 20 * random.randint(0, 19) # y head of snake
        self.prey_x = None                  # x of prey
        self.prey_y = None                  # y of prey
        self.length = 1                     # length of snake
        self.go = 100                       # go nowhere   (initial value)
        self.gone = 100                     # gone nowhere (initial value)
        self.edible = False                 # whether space of snake's head is same as space of prey
        self.space = [(self.x, self.y)]     # queue | the space that the snake takes
        self.rect = []                      # list of pygame.Rect instances
        self.surf = []                      # list of pygame.Surface instances
        self.wall = None                    # tuple of distance from the wall to the head of the snake
        self.prey = None                    # tuple of distance from the prey to the head of the snake
        self.__START = True                 # private variable | whether the game just started

        # screen
        self.screen = None
        self.clock = None

        # objects
        self.snakeRect = None               # pygame.Rect    | head of snake
        self.snakeSurf = None               # pygame.Surface | head of snake
        
        self.preyRect = None                # pygame.Rect    | prey
        self.preySurf = None                # pygame.Surface | prey

        # genetic neural network
        self.gnn = gnn
    
    def __str__(self, score=False, length=False, pos=False, space=False):
        info = ''
        if score or length:
            info += 'score : {0}  '.format(self.length)
        if pos:
            info += '(x,y) : ({0},{1})  '.format(self.x, self.y)
        if space:
            info += 'space : {0}'
        return info.strip()
    
    def __call__(self):
        pass        
    
    def update(self, delta_x=None, delta_y=None):
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
        self.prey = ((self.prey_x - self.x) / STEP, (self.prey_y - self.y) / STEP)
    
    def info(self):
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

    def where(self): # FIXME generator? or just method?
        if True:
            # a = [1, 2, -1, -2] * 100
            a = [1,1,1,1,1,2,2,2,2,2,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2] * 100
            yield from a
        if False:
            status = self.wall + self.prey
            return gnn.predict(status)


    def play(self):

        if self.__START:
            # screen
            self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
            pygame.display.set_caption('snake game')
            self.clock = pygame.time.Clock()

            # objects
            self.snakeRect = pygame.Rect((self.x, self.y), (SIZE, SIZE))
            self.snakeSurf = pygame.Surface((SIZE, SIZE))
            self.snakeSurf.fill(GREEN)

            self.preyRect = None
            self.preySurf = pygame.Surface((SIZE, SIZE))
            self.preySurf.fill(RED)

        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                    elif event.key == pygame.K_UP:
                        self.snakeRect.move_ip(0, -STEP)
                        self.update(delta_y=-STEP)
                    elif event.key == pygame.K_DOWN:
                        self.snakeRect.move_ip(0, STEP)
                        self.update(delta_y=STEP)
                    elif event.key == pygame.K_LEFT:
                        self.snakeRect.move_ip(-STEP, 0)
                        self.update(delta_x=-STEP)
                    elif event.key == pygame.K_RIGHT:
                        self.snakeRect.move_ip(STEP, 0)
                        self.update(delta_x=STEP)

        
            if not self.__START:
                if self.go == 2: # go UP
                    self.snakeRect.move_ip(0, -STEP) # changes the self.snakeRect's position
                    self.update(delta_y=-STEP)

                elif self.go == -2: # go DOWN
                    self.snakeRect.move_ip(0, STEP)
                    self.update(delta_y=STEP)

                elif self.go == -1: # go LEFT
                    self.snakeRect.move_ip(-STEP, 0)
                    self.update(delta_x=-STEP)

                elif self.go == 1: # go RIGHT
                    self.snakeRect.move_ip(STEP, 0)
                    self.update(delta_x=STEP)
                else:
                    pass

            self.info()

            # game end rule
            if (not 0 <= self.x <= (SCREEN_SIZE - SIZE)) or (not 0 <= self.y <= (SCREEN_SIZE - SIZE)):
                print('out of boundary')
                quit()
            elif (self.x, self.y) in self.space[1:]  or (self.length > 1 and self.go + self.gone == 0):
                print('it\'s you!')
                quit()
            elif self.length == 400:
                print('you win!')
                quit()

            # prey
            if self.__START == True or (self.prey_x, self.prey_y) == (self.x, self.y):
                self.prey_x = SIZE * random.randint(0, int((SCREEN_SIZE - SIZE) / STEP))
                self.prey_y = SIZE * random.randint(0, int((SCREEN_SIZE - SIZE) / STEP))
                while (self.prey_x, self.prey_y) in self.space:
                    self.prey_x = SIZE * random.randint(0, int((SCREEN_SIZE - SIZE) / STEP))
                    self.prey_y = SIZE * random.randint(0, int((SCREEN_SIZE - SIZE) / STEP))
                self.preyRect = pygame.Rect((self.prey_x, self.prey_y), (SIZE, SIZE))
                
                if self.__START:
                    self.__START = False
                    where = self.where() # generator
                elif not self.__START:
                    self.eat()

            # update direction of snake
            self.gone = self.go
            self.go = next(where)
            # time.sleep(0.25)

            # screen display
            self.screen.fill(BLACK)
            self.screen.blit(self.snakeSurf, self.snakeRect)
            self.move()
            for surf, rect in zip(self.surf, self.rect):
                self.screen.blit(surf, rect)
            self.screen.blit(self.preySurf, self.preyRect)
            pygame.display.update()