from enum import Enum

class Mica:
    def __init__(self, color):
        self._color = color

class Field:
    def __init__(self, color):
        self.stack = []
        self.color = color

class Matrix:
    def __init__(self, N):
        self.matrix = [[Field(Color.BLACK if (i+j)%2 == 0 else Color.WHITE) for i in range(N)] for j in range(N)]

    def startPositions(self):
        for j in range(0, self.matrix.size()):
            if j%2==0:
                for i in range(2, self.matrix.size()-1, 2):
                    self.matrix[i][j].stack.append(Mica(Color.WHITE))
            else:
                for i in range(1, self.matrix.size()-2, 2):
                    self.matrix[i][j].stack.append(Mica(Color.BLACK))

def setMice(currentState, newState):
    newMatrix = Matrix(currentState.matrix.size())
    for item in newState:
        newMatrix.matrix[item[0]][item[1]].stack = item[2]
    return newMatrix



class AppState:
    def __init__(self, N):
        self.matrix = Matrix(N, N)
        self.matrix.startPositions()

    def set_state(self, newState):
        self.matrix = setMice(self.matrix, newState)

    def get_state(self):
        return self.matrix
    

class Color(Enum):
    BLACK=0
    WHITE=1