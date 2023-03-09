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
        self.snakes_lengths=lines[1].replace("\n","").split(" ")
        for i in range(len(lines[2:])):
            lines[i+2]=lines[i+2].replace("\n","").split(" ")
            for j in range(len(lines[i+2])):
                if (lines[i+2][j]!='*'):
                    lines[i+2][j]=int(lines[i+2][j])
        self.board=np.array(lines[2:])

class Snake:
    def __init__(self, length):
        self.length = length
        segments = np.zeros((self.length, 2))
        nextStep = np.array((4, 2)) 
        

def main():
    snake_board=Game(sys.argv[1])
    print(snake_board.board)
    return

if __name__ == '__main__':
    main()