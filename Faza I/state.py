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

class Score:
    Player = 0
    Computer = 0
    def __init__(self):
        self.Player = 0
        self.Computer = 0


class AppState:
    def __init__(self, N, firstPlayer):
        self.matrix = Matrix(N, N)
        self.matrix.startPositions()
        self.currentPlayer = firstPlayer
        self.score = Score()
        self.finished = False
        #broj mica = (n-2)*n/2, max stackova je to /8, uslov za pobedu je vise od tog /2
        self.winCondition = (N-2)*(N/2)/8/2

    # def set_state(self, newState):
    #     self.matrix = setState(self.matrix, newState)


    #valid move => (src(x, y), stackslice, dst(x, y))
    def set_state(self, src, stackslice, dst):
        extractedSlice = self.matrix.matrix[src[0]][src[1]].stack[stackslice:]
        self.matrix.matrix[src[0]][src[1]].stack = self.matrix.matrix[src[0]][src[1]].stack[:stackslice]
        self.matrix.matrix[dst[0]][dst[1]].stack = self.matrix.matrix[dst[0]][dst[1]].stack + stackslice
        
    def get_state(self):
        return self.matrix
    
def setStateImmutable(currentState, newState):
    newMatrix = Matrix(currentState.matrix.size())
    for item in newState:
        newMatrix.matrix[item[0]][item[1]].stack = [*item[2]]
    return newMatrix

class Color(Enum):
    BLACK=0
    WHITE=1

class Player(Enum):
    Player="player"
    Computer="computer"


def add(self, secondStack):
    if(len(self.stack) + len(secondStack) > 8):
        raise Exception("Stack overflow")
    self.stack = self.stack + secondStack

def scoreIncrement(player):
    if player == Player.Player:
        AppState.score.Player += 1
        if AppState.score.Player > AppState.winCondition:
            AppState.finished = True
    else:
        AppState.score.Computer += 1
        if AppState.score.Computer > AppState.winCondition:
            AppState.finished = True