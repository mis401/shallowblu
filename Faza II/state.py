from copy import deepcopy
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

#klasa za igraca
class Player:
    def __init__(self, typeOfPlayer, color):
        self.type : PlayerType = typeOfPlayer
        self.color : Color = color
        self.score = 0


#klasa za celokupno stanje aplikacije
class AppState:
    def __init__(self, N, firstPlayer, mode):
        print("creating appstate")
        self.matrix = Matrix(N)
        self.matrix.startPositions()
        self.players = [Player(PlayerType.Player, \
                               Color.WHITE if firstPlayer==PlayerType.Player.value else Color.BLACK), \
                                Player(PlayerType.Computer, Color.WHITE if firstPlayer == PlayerType.Computer.value \
                                else Color.WHITE)] if mode == "singleplayer" else \
                                [Player(PlayerType.Player, Color.WHITE), Player(PlayerType.Player, Color.BLACK)]
        self.currentPlayer = self.players[0] if self.players[0].color == Color.WHITE else self.players[1]
        self.finished = False
        #broj mica = (n-2)*n/2, max stackova je to /8, uslov za pobedu je vise od tog /2
        self.winCondition = (N-2)*(N/2)/8/2
        self.currentMove = [None, None, None]
        self.matrixSize = N

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

    def scoreIncrement(self):
        self.currentPlayer.score += 1
        if self.currentPlayer.score >= self.winCondition:
            self.finished = True

            
    def switchPlayer(self):
        print("switching players")
        self.currentPlayer = self.players[1] if self.currentPlayer == self.players[0] else self.players[0]

    def evaluate_game_state(self, ai_color):
        ai_control = 0
        potential_moves = 0

        for row in self.matrix.matrix:
            for field in row:
                if field.stack:
                    # Count stacks controlled by AI
                    if field.stack[-1].color == ai_color:
                        ai_control += 1
                    # Count potential moves for AI
                    if field.stack[0].color == ai_color:
                        potential_moves += len(self.get_valid_moves(field))

        # Scoring function can be adjusted based on game strategy
        return ai_control + potential_moves

    def get_opponent(self, currentPlayer):
        return self.players[1] if currentPlayer == self.players[0] else self.players[0]
    def copy_state(self):
        # Create a deep copy of the current state
        state_copy = {
            "matrix": deepcopy(self.matrix), 
            "currentPlayer": self.currentPlayer,
            "players": deepcopy(self.players),
            "finished": self.finished
        }
        return state_copy

    def restore_state(self, state_copy):
        # Restore all elements of the game state
        self.matrix = state_copy["matrix"]
        self.currentPlayer = state_copy["currentPlayer"]
        self.players = state_copy["players"]
        self.finished = state_copy["finished"]
    
    def minmax(self, depth, maximizingPlayer):
        if depth == 0 or self.is_terminal_node():
            return self.evaluate_game_state()

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in self.get_valid_moves(self.currentPlayer.color):
                self.apply_move(move)
                eval = self.minmax(depth - 1, False)
                maxEval = max(maxEval, eval)
                self.undo_move(move)
            return maxEval
        else:
            minEval = float('inf')
            for move in self.get_valid_moves(self.get_opponent(self.currentPlayer).color):
                self.apply_move(move)
                eval = self.minmax(depth - 1, True)
                minEval = min(minEval, eval)
                self.undo_move(move)
            return minEval


        

class Color(Enum):
    BLACK=0
    WHITE=1


class PlayerType(Enum):
    Player="player"
    Computer="computer"
    

