import numpy as np
import sys

class Node():
    def __init__(self, state, parent, action, current_length):
        self.state = state
        self.parent = parent
        self.action = action
        self.current_length=current_length

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
            print("done")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            print("done")
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
        print("Board:\n",self.board)
        #print("Wormholes:\n",self.wormholes)
        print("Wormholes:\n",self.wormholes_list)
        self.solution = None

    def neighbors(self, state):
        row, col = state
        if self.wormholes[row][col]:
            candidates=[]
            #aca van los candidatos de el wormhole
            for i in self.wormholes_list:
                if i!=(row,col):
                    candidates.append((str(i[0])+str(i[1])+"U", (i[0] - 1, i[1]))),
                    candidates.append((str(i[0])+str(i[1])+"D", (i[0] + 1, i[1]))),
                    candidates.append((str(i[0])+str(i[1])+"L", (i[0], i[1] - 1))),
                    candidates.append((str(i[0])+str(i[1])+"R", (i[0], i[1] + 1)))
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
    

    def solve(self,start_point, snake_length):
        """Finds best path for a starting point"""

        # Initialize frontier to just the starting position
        start = Node(state=start_point, parent=None, action=None, current_length=1)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()
        self.solutions=[]

        # Keep looping until solution found
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                #print(self.solutions)
                max=-999999
                index=0
                for i in self.solutions:
                    if i[2]>max:
                        max=i[2]
                        max_actions=i[0]
                        max_cells=i[1]
                print("Score: ",max)
                print("Actions: ",max_actions)
                print("Cells: ",max_cells)
                return

            # Choose a node from the frontier
            node = frontier.remove()

            # If node is the goal, then we have a solution
            if node.current_length == snake_length:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                cells.append(start.state)
                actions.reverse()
                cells.reverse()
                score=0
                for i in cells:
                    score+=self.board[i[0]][i[1]]
                self.solutions.append((actions, cells, score))

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action, current_length=node.current_length+1)
                    frontier.add(child)

if __name__ == '__main__':
    print("Game generated...")
    snake_board=Game(sys.argv[1])
    print("Solving...")
    snake_board.solve((0,0),6)