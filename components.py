import pygame

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

        def draw(self):
            #draw grid and objects onto grid
            self.window.fill((0, 0, 0))
            self.drawBoxes()
            pygame.display.update()
