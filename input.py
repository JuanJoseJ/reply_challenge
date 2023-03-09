import numpy as np

class parameters:
    input_file = ''
    C = 0
    R = 0
    S = 0

    def __init__(self, input_file):
        self.input_file = input_file
        file = open(self.input_file, "r")

        values = file.readline().split(" ")
        self.C = int(values[0])
        self.R = int(values[1])
        self.S = int(values[2])

            


param = parameters("reply_challenge/00-example.txt")
print(param.matrix)