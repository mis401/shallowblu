from enum import Enum
#klasa za svaku Micu
class Mica:
    def __init__(self, color):
        self.color : Color = color

#klasa za svako polje na tabli
class Field:
    def __init__(self, color):
        print("creating field")
        self.stack: Mica = []
        self.color : Color = color

#klasa za tablu
class Matrix:
    def __init__(self, N):
        print("creating matrix")
        self.matrix : Field = [[Field(Color.BLACK if (i+j)%2 == 0 else Color.WHITE) for i in range(N)] \
                               for j in range(N)]

    def startPositions(self):
        for j in range(0, len(self.matrix)):
            if j%2==0:
                for i in range(2, len(self.matrix)-1, 2):
                    self.matrix[i][j].stack.append(Mica(Color.WHITE))
            else:
                for i in range(1, len(self.matrix)-2, 2):
                    self.matrix[i][j].stack.append(Mica(Color.BLACK))

#klasa za vodjenje stanja poena
class Score:
    def __init__(self):
        self.PlayerOne = 0
        self.PlayerTwo = 0

#klasa za igraca
class Player:
    def __init__(self, typeOfPlayer, color):
        self.type : PlayerType = typeOfPlayer
        self.color : Color = color


#klasa za celokupno stanje aplikacije
class AppState:
    def __init__(self, N, firstPlayer):
        print("creating appstate")
        print(firstPlayer == PlayerType.Player.value)
        self.matrix = Matrix(N)
        self.matrix.startPositions()
        self.players = [Player(PlayerType.Player, \
                               Color.WHITE if firstPlayer==PlayerType.Player.value else Color.BLACK), \
                                Player(PlayerType.Computer, Color.WHITE if firstPlayer == PlayerType.Computer.value \
                                else Color.WHITE)]
        self.currentPlayer = self.players[0] if self.players[0].color == Color.WHITE else self.players[1]
        self.score = Score()
        self.finished = False
        #broj mica = (n-2)*n/2, max stackova je to /8, uslov za pobedu je vise od tog /2
        self.winCondition = (N-2)*(N/2)/8/2
        self.currentMove = [None, None, None]

    #valid move => (src(x, y), stackslice, dst(x, y))
    def set_state(self, src, stackslice, dst):
        extractedSlice = self.matrix.matrix[src[0]][src[1]].stack[stackslice:]
        self.matrix.matrix[src[0]][src[1]].stack = self.matrix.matrix[src[0]][src[1]].stack[:stackslice]
        self.matrix.matrix[dst[0]][dst[1]].stack = self.matrix.matrix[dst[0]][dst[1]].stack + extractedSlice
        if len(self.matrix.matrix[dst[0]][dst[1]].stack) == 8:
            self.scoreIncrement(self.matrix.matrix[dst[0]][dst[1]].stack[7].color)
            self.matrix.matrix[dst[0]][dst[1]].stack.clear()
        if self.finished==False:
            self.switchPlayer()

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

            
    def switchPlayer(self):
        print("switching players")
        self.currentPlayer = self.players[1] if self.currentPlayer == self.players[0] else self.players[0]

        

class Color(Enum):
    BLACK=0
    WHITE=1


class PlayerType(Enum):
    Player="player"
    Computer="computer"
    

