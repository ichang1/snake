from components import Board, Snake, Location
from pygame import event, time
from pygame.constants import (
    QUIT
    )

if __name__ == "__main__":
    width = 1200
    height = 900
    scale = 30
    startLength = 3

    board = Board(1200, 900, 30)
    snake = Snake(Location(20,15)) #initial with non scaled location

    for i in range(startLength - 1):
        snake.grow()

    while (not snake.inBody() and not snake.inWall(board)):
        for e in event.get():
            if (e.type == QUIT) :
                quit()
        time.delay(50)
        snake.move()
        board.draw(snake)
