import numpy as np
import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Game:
    def __init__(self, filename):
        with open(filename) as f:
            file = f.read()
        lines = file.splitlines()
        initial=lines[0].split(" ")
        self.height = int(initial[1])
        self.width = int(initial[0])
        self.S = int(initial[2])
        self.snakes_lengths=lines[1].split(" ")
        self.board=lines[2:]
        self.wormholes = []
        self.wormholes_list=[]
        for i in range(len(self.board)):
            self.board[i]=self.board[i].split(' ')
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if self.board[i][j] == "*":
                        self.board[i][j]=int(0)
                        row.append(True)
                        self.wormholes_list.append((i,j))
                    else:
                        row.append(False)
                        self.board[i][j]=int(self.board[i][j])
                except IndexError:
                    row.append(False)
            self.wormholes.append(row)
        self.wormholes=np.array(self.wormholes)
        self.board=np.array(self.board, dtype=int)
        self.solution = None

    def neighbors(self, state):
        row, col = state
        if self.wormholes[row][col]:
            candidates=[]
            #aca van los candidatos de el wormhole
            for i in self.wormholes_list:
                if i!=(row,col):
                    candidates.append("U", (i[0] - 1, i[1])),
                    candidates.append("D", (i[0] + 1, i[1])),
                    candidates.append("L", (i[0], i[1] - 1)),
                    candidates.append("R", (i[0], i[1] + 1))
        else:
            candidates = [
                ("U", (row - 1, col)),
                ("D", (row + 1, col)),
                ("L", (row, col - 1)),
                ("R", (row, col + 1))
            ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width:
                result.append((action, (r, c)))
            elif not 0 <= r < self.height:
                if r>=self.height:
                    result.append((action, (0, c)))
                else:
                    result.append((action, (self.height-1, c)))
            elif not 0 <= c < self.width:
                if c>=self.width:
                    result.append((action, (r, 0)))
                else:
                    result.append((action, (r, self.width-1)))
        return result

if __name__ == '__main__':
    snake_board=Game(sys.argv[1])