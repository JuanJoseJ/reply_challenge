import numpy as np
import sys
class Game:
    def __init__(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        initial=lines[0].replace("\n","").split(" ")
        self.C = int(initial[0])
        self.R = int(initial[1])
        self.S = int(initial[2])
        snakes_lengths=lines[1].replace("\n","").split(" ")
        for i in lines[2:]:
            self.board=np.array



if __name__ == '__main__':
    snake_board=Game(sys.argv[1])