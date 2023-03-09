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
        for i in range(len(self.board)):
            self.board[i]=self.board[i].split(' ')
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if self.board[i][j] == "*":
                        print("asterizco")
                        self.board[i][j]=int(0)
                        row.append(True)
                    else:
                        row.append(False)
                        self.board[i][j]=int(self.board[i][j])
                except IndexError:
                    row.append(False)
            self.wormholes.append(row)
        self.wormholes=np.array(self.wormholes)
        self.board=np.array(self.board, dtype=int)
        self.solution = None
        print(self.wormholes)
        print(self.board)

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("U", (row - 1, col)),
            ("D", (row + 1, col)),
            ("L", (row, col - 1)),
            ("R", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

if __name__ == '__main__':
    snake_board=Game(sys.argv[1])