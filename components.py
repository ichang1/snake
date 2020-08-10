import pygame
from pygame.constants import (
    QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN, K_UP
)
import random

class Board(object):
        def __init__(self, width, height, scale):
            # height and width of board in pixels
            self.width = width
            self.height = height
            self.scale = scale  #pixel length of size of each grid square
            self.window = pygame.display.set_mode((width, height))

        def drawBoxes(self):
            #draw grid squares
            for row in range(0, self.height, self.scale):
                pygame.draw.line(self.window, (255, 255, 255), (0, row), (self.width, row))
            for col in range(0, self.width, self.scale):
                pygame.draw.line(self.window, (255, 255, 255), (col, 0), (col, self.height))

        def draw(self, snake, food):
            #draw grid and objects onto grid
            self.window.fill((0, 0, 0))
            self.drawBoxes()
            snake.draw(self)
            food.draw(self)
            pygame.display.update()

class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, loc):
        sum = Location(self.x + loc.x, self.y + loc.y)
        return sum

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Snake(object):
    # head is at position 0 and the next block in at position 1 and so on...
    bodyLoc = [] # list of locations for each block in body
    bodyDir = []  #list of directions each block in body is facing
    size = 1 #length of body

    def __init__(self, location):
        initDir = Location(1, 0)
        self.bodyLoc.append(location)
        self.bodyDir.append(initDir)

    def grow(self):
        tailLocX = self.bodyLoc[-1].x
        tailLocY = self.bodyLoc[-1].y
        tailDirX = self.bodyDir[-1].x
        tailDirY = self.bodyDir[-1].y
        newSegLoc = Location(tailLocX - tailDirX, tailLocY - tailDirY)
        newSegDir = Location(tailDirX, tailDirY)
        self.bodyLoc.append(newSegLoc)
        self.bodyDir.append(newSegDir)
        self.size += 1

    def moveBy(self, delta):
        for i in range(self.size - 1, 0, -1):
            self.bodyLoc[i] = self.bodyLoc[i - 1]
            self.bodyDir[i] = self.bodyDir[i - 1]
        self.bodyLoc[0] += delta
        self.bodyDir[0] = delta

    def move(self):
        nextLoc = self.bodyDir[0] # by default head moves by direction it is facing

        # locations for logic in for loop
        leftLoc = Location(-1, 0)
        rightLoc = Location(1, 0)
        upLoc = Location(0 , -1)
        downLoc = Location(0, 1)

        for event in pygame.event.get():
            if (event.type == QUIT) :
                quit()
            keys = pygame.key.get_pressed() # get keys pressed
            for key in keys:
                if (keys[K_LEFT] and not (nextLoc == rightLoc)):
                    # left is clicked and the head direction is not right
                    nextLoc = leftLoc
                elif (keys[K_RIGHT] and not (nextLoc == leftLoc)):
                    # right is clicked and the head direction is not left
                    nextLoc = rightLoc
                elif (keys[K_UP] and not (nextLoc == downLoc)):
                    # up is clicked and the head direction is not down
                    nextLoc = upLoc
                elif (keys[K_DOWN] and not (nextLoc == upLoc)):
                    # down is clicked and the head direction is not up
                    nextLoc = downLoc
                break
        self.moveBy(nextLoc)

    def shouldGrow(self, food, board):
        if (self.bodyLoc[0] == food.location):
            self.grow()
            food.changeLocation(self, board)

    def inBody(self):
        # get bool for head location is in body
        return self.bodyLoc[0] in self.bodyLoc[1:len(self.bodyLoc) - 1]

    def inWall(self, board):
        # get bool for head past board borders
        headLoc = self.bodyLoc[0]
        if (headLoc.x == -1 or headLoc.x == board.width//board.scale):
            return True
        elif (headLoc.y == -1 or headLoc.y == board.height//board.scale):
            return True
        else:
            return False

    def draw(self, board):
        # draw snake onto board
        scale = board.scale
        for i in range(len(self.bodyLoc)):
            recTopLeftx = self.bodyLoc[i].x
            recTopLefty = self.bodyLoc[i].y
            #light green for head
            if (i == 0):
                pygame.draw.rect(board.window, (0,255,127),
                        (recTopLeftx*scale + 2, recTopLefty* scale + 2, scale - 3 , scale - 3))
            #dark green for body
            else:
                pygame.draw.rect(board.window, (0,100,0),
                        (recTopLeftx*scale + 2, recTopLefty* scale + 2, scale - 3 , scale - 3))

class Food(object):
    def __init__(self, board, snake):
        while True:
            randX = random.randrange(board.width//board.scale)
            randY = random.randrange(board.height//board.scale)
            randLoc = Location(randX, randY)
            if (randLoc == snake.bodyLoc[0]):
                continue
            else:
                break
        self.location = randLoc

    def draw(self, board):
        scale = board.scale
        recTopLeftx = self.location.x
        recTopLefty = self.location.y
        pygame.draw.rect(board.window, (255, 0, 0),
                (recTopLeftx*scale + 2, recTopLefty*scale + 2, scale - 3 , scale - 3))

    def changeLocation(self, snake, board):
        if (self.location == snake.bodyLoc[0]):
            while True:
                randX = random.randrange(board.width//board.scale)
                randY = random.randrange(board.height//board.scale)
                randLoc = Location(randX, randY)
                if (len(list(filter(lambda loc:loc == randLoc, snake.bodyLoc))) > 0):
                    # if the random location matches any of the locations of the
                    # body, make another new random location for the food
                    continue
                else:
                    break
            self.location = randLoc
