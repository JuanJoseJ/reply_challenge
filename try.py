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
                else:
                    lines[i+2][j]=np.nan
        self.board=np.array(lines[2:])
    
    def initialize(self):
        halfC = int(self.C/2)
        halfR = int(self.R/2)
        q1 = self.board[0:halfR, 0:halfC]
        q2 = self.board[0:halfR, halfC:]
        q3 = self.board[halfR:, 0:halfC]
        q4 = self.board[halfR:, halfC:]
        quadrants = [q1, q2, q3, q4]
        maxSums = [q1[~(np.isnan(q1))].sum(), q2[~(np.isnan(q2))].sum(), q3[~(np.isnan(q3))].sum(), q4[~(np.isnan(q4))].sum()]
        maxQuadr = maxSums.index(max(maxSums))
        
        bestQuadrant = quadrants[maxQuadr]
        maxPoint = bestQuadrant[~(np.isnan(bestQuadrant))].max()
        initialPoint = np.where(bestQuadrant == maxPoint)
        
        coord = [initialPoint[0][0], initialPoint[1][0]]
        if maxQuadr == 1 or maxQuadr == 3:
            coord[1] += halfC
        if maxQuadr == 2 or maxQuadr == 3:
            coord[0] += halfR
        return (coord[0], coord[1])


class Snake:
    def __init__(self, length):
        self.length = length
        segments = np.zeros((self.length, 2))
        nextStep = np.array((4, 2))
        

def main():
    snake_board=Game(sys.argv[1])
    # print(snake_board.board)
    coord = snake_board.initialize()
    print(coord)
    print(snake_board.board[coord[0], coord[1]])
    return

if __name__ == '__main__':
    main()