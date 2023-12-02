from enum import Enum
class Mica:
    def __init__(self, color):
        self.color : Color = color

class Field:
    def __init__(self, color):
        print("creating field")
        self.stack: Mica = []
        self.color : Color = color


class Matrix:
    def __init__(self, N):
        print("creating matrix")
        self.matrix : Field = [[Field(Color.BLACK if (i+j)%2 == 0 else Color.WHITE) for i in range(N)] for j in range(N)]

    def startPositions(self):
        for j in range(0, len(self.matrix)):
            if j%2==0:
                for i in range(2, len(self.matrix)-1, 2):
                    self.matrix[i][j].stack.append(Mica(Color.WHITE))
            else:
                for i in range(1, len(self.matrix)-2, 2):
                    self.matrix[i][j].stack.append(Mica(Color.BLACK))

class Score:
    def __init__(self):
        self.PlayerOne = 0
        self.PlayerTwo = 0


class AppState:
    def __init__(self, N, firstPlayer):
        print("creating appstate")
        print(firstPlayer == PlayerType.Player.value)
        self.matrix = Matrix(N)
        self.matrix.startPositions()
        self.players = [Player(PlayerType.Player, Color.WHITE if firstPlayer==PlayerType.Player.value else Color.BLACK), Player(PlayerType.Computer, Color.WHITE if firstPlayer == PlayerType.Computer.value else Color.WHITE)]
        self.currentPlayer = self.players[0] if self.players[0].color == Color.WHITE else self.players[1]
        self.score = Score()
        self.finished = False
        #broj mica = (n-2)*n/2, max stackova je to /8, uslov za pobedu je vise od tog /2
        self.winCondition = (N-2)*(N/2)/8/2
        self.currentMove = [None, None, None]

    # def set_state(self, newState):
    #     self.matrix = setState(self.matrix, newState)
    def switchPlayer(self):
        print("switching players")
        self.currentPlayer = self.players[1] if self.currentPlayer == self.players[0] else self.players[0]

    def scoreIncrement(self, color):
        print("inkrementira se skor za " + color.name)
        if self.players[0].color == color:
            self.score.PlayerOne +=1
            if self.score.PlayerOne > self.winCondition:
                self.finished = True
        else:
            self.score.PlayerTwo += 1
            if self.score.PlayerTwo > self.winCondition:
                self.finished = True
        print(self.score.PlayerOne)
        print(self.score.PlayerTwo)

    #valid move => (src(x, y), stackslice, dst(x, y))
    def set_state(self, src, stackslice, dst):
        extractedSlice = self.matrix.matrix[src[0]][src[1]].stack[stackslice:]
        print("Menja se stanje:")
        self.matrix.matrix[src[0]][src[1]].stack = self.matrix.matrix[src[0]][src[1]].stack[:stackslice]
        self.matrix.matrix[dst[0]][dst[1]].stack = self.matrix.matrix[dst[0]][dst[1]].stack + extractedSlice
        if len(self.matrix.matrix[dst[0]][dst[1]].stack) > 8:
            self.currentMove = [None, None, None]
            raise Exception("Stack overflow")
        if len(self.matrix.matrix[dst[0]][dst[1]].stack) == 8:
            self.scoreIncrement(self.matrix.matrix[dst[0]][dst[1]].stack[7].color)
            self.matrix.matrix[dst[0]][dst[1]].stack.clear()
        if self.finished==False:
            self.switchPlayer()
        
    def get_state(self):
        return self.matrix
    



    
def setStateImmutable(currentState, newState):
    newMatrix = Matrix(len(currentState.matrix))
    for item in newState:
        newMatrix.matrix[item[0]][item[1]].stack = [*item[2]]
    return newMatrix

class Color(Enum):
    BLACK=0
    WHITE=1

class PlayerType(Enum):
    Player="player"
    Computer="computer"
    
class Player:
    def __init__(self, typeOfPlayer, color):
        self.type : PlayerType = typeOfPlayer
        self.color : Color = color

def add(self, secondStack):
    if(len(self.stack) + len(secondStack) > 8):
        raise Exception("Stack overflow")
    self.stack = self.stack + secondStack

