from components import Board
from pygame import event
from pygame.constants import (
    QUIT
    )
import curses

if __name__ == "__main__":
    width = 1200
    height = 900
    scale = 30
    board = Board(1200, 900, 30)

    while True:
        for e in event.get():
            if (e.type == QUIT) :
                quit()
        board.draw()
