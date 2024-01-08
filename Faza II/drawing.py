import sys

print(sys.executable)

import queue
import pygame
import math
import thorpy as tp
import time
from state import *

BEIGE=(208,197,170)
DARK_RED=(75,15,15)
GRAY=(86,99,142)
BLUE= (130,142,184)
BLACK=(27,32,51)
WHITE=(223,224,229)

initialState = False
appState = None
selectedMica = None
selectedSquare = None
destSquare = None
#previous_state=None

pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W, H))
tp.init(screen, tp.theme_human)  # bind screen to gui elements and set theme


matrix_size = 0
whos_first=""
isSingleplayer = False

def user_choice():
    global matrix_size
    global initialState
    global appState
    global isSingleplayer
    launcher.set_invisible(True)    
    if initialState == False:
        alert_sp.launch_alone(func_before=blit_before_gui)
        alert1.launch_alone(func_before=blit_before_gui)
        #alert1._at_click = close_alert
        if (alert_sp.choice == "singleplayer"):        
            alert2.launch_alone(func_before=blit_before_gui)
            isSingleplayer = True 

    print("User has chosen:", alert1.choice)
    try:
        matrix_size = int(alert1.choice)
        print(matrix_size)
        whos_first = alert2.choice
        print('preprint')
        print(whos_first)
        if appState == None and initialState == False:
            print("usao u if")
            appState = AppState(matrix_size, whos_first, alert_sp.choice)
            initialState = True
    except Exception as e:
        print(e)
        pass

def blit_before_gui():

    gradient = tp.graphics.color_gradient((BLUE, WHITE), (W, H), "v")
    screen.blit(gradient, (0, 0))

    if not appState:
        return
    draw_chessboard()
    draw_boxes_for_scores()

     # Da pise ciji je red 
    font = pygame.font.Font(None, 36)  # Adjust the font size as needed

    if appState and appState.currentPlayer:
        if appState.currentPlayer.type == PlayerType.Player:
            text_color=BEIGE
            turn_text = "Your turn"
            text_position = (10, 10)  
        else:
            text_color=BLUE
            turn_text = "AI's turn"
            text_position = (W - 150, 10)  
        # Render
        turn_surface = font.render(turn_text, True, text_color)  # Black text
        screen.blit(turn_surface, text_position)

    pygame.display.update()
    if appState and appState.finished == True:
        winAlert = tp.Alert("Kraj igre", "Pobednik je: " + appState.currentPlayer.type.value)
        winAlert.launch_alone()
        loop.playing = False


def draw_chessboard():
    square_size = appState.square_size
    total_width = matrix_size * square_size
    total_height = matrix_size * square_size
    if appState:
        matrix = appState.matrix.matrix
        center_x = (screen.get_width() - total_width) // 2
        center_y = (screen.get_height() - total_height) // 2

        for row in range(matrix_size):
            for col in range(matrix_size):
                draw_square(matrix[row][col], center_x+col*square_size, center_y+row*square_size, square_size, appState and appState.currentMove[0] == (row, col))

def draw_boxes_for_scores():
    if not appState:
        return
    global isSingleplayer
    box_width, box_height = 100, 50  
    border_thickness = 2  
    box_margin = 10  
    border_color = (0, 0, 0)  

    font = pygame.font.Font(None, 33)  # Adjust the font size as needed

    # ovde treba zapravo score koji brojimo
    player_name="AI" if isSingleplayer else "Player2"
    players = [("YOU", appState.players[0].score), (player_name, appState.players[1].score)]

    for i, (player_name, score) in enumerate(players):
        # i = 0, igrac je na levoj strani, inace na desnoj
        x = box_margin if i == 0 else screen.get_width() - box_width - box_margin
        y = screen.get_height() - box_height - box_margin

         # UI razliciti detalji za svakog igraca
        box_color = BEIGE if i==0 else BLUE
        text_color = BEIGE if i==0 else BLUE
        name_padding = 25 if i==0 else 15

        # Draw the border
        pygame.draw.rect(screen, border_color, (x - border_thickness, y - border_thickness, box_width + 2*border_thickness, box_height + 2*border_thickness))
        # Draw the inner box
        pygame.draw.rect(screen, box_color, (x, y, box_width, box_height))

        name_text = font.render(player_name, True, text_color)
        screen.blit(name_text, (x + name_padding, y - 30))  

        score_text = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (x + 45, y + 15))  


def draw_square(field, x, y, square_size, selected = False):
    color = BLACK if field.color == Color.BLACK else WHITE
    if selected:
        color = GRAY
    pygame.draw.rect(screen, color, [x, y, square_size, square_size])
    dy = square_size / 8
    bottom = y + square_size
    for mica in field.stack:
        draw_mica(mica, x, bottom-dy, square_size, selected and field.stack.index(mica) == appState.currentMove[1])
        bottom -= dy

def draw_mica(mica, x, y, width, selected=False):
    height = width / 8
    color = BLUE if mica.color == Color.BLACK else BEIGE
    if selected:
        color = GRAY
    border_color = (0, 0, 0)  # Green, for example
    # ovo ce biti crni okvir
    mica = pygame.draw.rect(screen, border_color, [x, y, width, height])

    border_thickness = 1  

    inner_x = x + border_thickness
    inner_y = y + border_thickness
    inner_width = width - 2 * border_thickness
    inner_height = height - 2 * border_thickness

    # Make sure inner dimensions are positive
    if inner_width > 0 and inner_height > 0:
        # Unutrasnji rect je zapravo MICA
        inner_rect = pygame.draw.rect(screen, color, [inner_x, inner_y, inner_width, inner_height])

    
def selectMica(pos):

    square_size = appState.square_size
    try:
        total_width = matrix_size * square_size
        total_height = matrix_size * square_size
        matrix = appState.matrix.matrix
        top_left_x = (screen.get_width() - total_width) // 2
        top_left_y = (screen.get_height() - total_height) // 2
        selectedCol = (pos[0] - top_left_x) // square_size  
        selectedRow = (pos[1] - top_left_y) // square_size
        selectedSquare = matrix[selectedRow][selectedCol]
        inSquare = (pos[1] - top_left_y) % square_size
        #print(inSquare)
        upInSquare = abs(inSquare - square_size)
        #print(upInSquare)
        micaPos = int(upInSquare // (square_size / 8))
        print(micaPos)
        micaPos = min(micaPos, len(selectedSquare.stack)-1)
        if micaPos < 0:
            raise Exception("Prazno polje")
        print(micaPos)
        appState.currentMove[0] = (selectedRow, selectedCol)
        appState.currentMove[1] = micaPos
        return True
    except Exception as e:
        appState.currentMove = [None, None, None]
        print(e)
        pass

def selectDestSquare(pos):
    square_size = appState.square_size
    try:
        total_width = matrix_size * square_size
        total_height = matrix_size * square_size
        matrix = appState.matrix.matrix
        top_left_x = (screen.get_width() - total_width) // 2
        top_left_y = (screen.get_height() - total_height) // 2
        selectedCol = (pos[0] - top_left_x) // square_size
        selectedRow = (pos[1] - top_left_y) // square_size
        appState.currentMove[2] = (selectedRow, selectedCol)
        return True 
    except Exception as e:
        appState.currentMove = [None, None, None]
        print(e)
        pass

def performMove():
    startPos = appState.currentMove[0]
    destPos = appState.currentMove[2]
    sliceIndex = appState.currentMove[1]
    valid, reason = checkMove(startPos, sliceIndex, destPos)
    if not valid:
        print(reason)
        appState.currentMove = [None, None, None]
        return
    startPos = appState.currentMove[0]
    destPos = appState.currentMove[2]
    sliceIndex = appState.currentMove[1]
    print("prihvacen potez" + str(startPos) + str(sliceIndex) + str(destPos))
    appState.set_state(startPos, sliceIndex, destPos)
    appState.currentMove = [None, None, None]


def checkMove(startPos, sliceIndex, destPos):
    #print("START JE U CHECK:"+ str(startPos))
    #print("END JE U CHECK:"+str(destPos))
    #print("SLICE JE: "+ str(sliceIndex))
    if not appState.matrix.matrix[startPos[0]][startPos[1]].stack:
        return False, "empty field"
    start_time = time.perf_counter_ns()
    end_time = time.perf_counter_ns()
    if (appState.matrix.matrix[startPos[0]][startPos[1]].stack[sliceIndex].color != appState.currentPlayer.color):
        end_time = time.perf_counter_ns()
        #print("check move time: " + str(end_time - start_time))
        return False, "wrong color"
    dx = abs( startPos[0] - destPos[0])
    dy = abs(startPos[1] - destPos[1])
    if not dx == 1 or not dy == 1:
        end_time = time.perf_counter_ns()
        #print("check move time: " + str(end_time - start_time))
        return False, "not adjacent"
    if len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) + \
        len(appState.matrix.matrix[startPos[0]][startPos[1]].stack[sliceIndex:]) > 8:
        end_time = time.perf_counter_ns()
        #print("check move time: " + str(end_time - start_time))
        return False, "stack overflow"
    
    possiblePaths, neighbours = possibleDestinations(startPos)
    if not neighbours:
        if (appState.matrix.matrix[startPos[0]][startPos[1]].stack[0].color == appState.currentPlayer.color):
            appState.currentMove[1] = 0
            sliceIndex = 0
        else:
            return False, "does not own stack"

    print("MOGUCI PATS SU:"+ str(possiblePaths))
    print('\n')
    print(possiblePaths)
    possibleDests = list(filter(lambda x: x[1] == destPos, possiblePaths))
    if len(possibleDests) == 0:
        end_time = time.perf_counter_ns()
        #print("check move time: " + str(end_time - start_time))
        return False, "selected field not valid"
    if (len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) <= sliceIndex and sliceIndex != 0):
        end_time = time.perf_counter_ns()
        #print("check move time: " + str(end_time - start_time))
        return False, "new position cant be lower than current"
    end_time = time.perf_counter_ns()
    #print("check move time: " + str(end_time - start_time))
    return True, "ok"

def aiMove():
    print("AI move")

    best_score = float('-inf')
    best_move = None
    moves = get_valid_moves(appState, appState.currentPlayer.color)
    for move in moves:
        previous_state = apply_move(move)
        score = minmax(depth=1, maximizingPlayer=False)  # Adjust depth as needed
        undo_move(previous_state)

        if score > best_score:
            best_score = score
            best_move = move
            print(move)

    # Perform the best move
    if best_move:
        appState.currentMove = [best_move[0], best_move[1], best_move[2]]
        performMove()

    return best_move  # Optional

#okvir table
def validField(field):
    return field[0] >= 0 and field[0] < appState.matrixSize and field[1] >= 0 and field[1] < appState.matrixSize

#vraca dijagonalno susedna polja 
def getNeighbours(field):
    directions = [(1, -1), (-1, -1), (-1, 1), (1, 1)] #clockwise
    neighbours = []
    for direction in directions:
        dest = (field[0] + direction[0], field[1] + direction[1])
        if validField(dest):
            neighbours.append(dest)
    return neighbours

#BFS koji vraca najblize stackove
def findNearestDestBFS(startPos):
    print("bfs search")
    closest =[]
    q = []
    visited = set()
    q.append(startPos)
    foundStack = False
    g = {}
    g[startPos] = 0
    prev_node = {}
    prev_node[startPos] = None
    closestG = -1
    print(len(q))
    while len(q) > 0:
        current = q.pop(0)
        print(current)
        if current in visited:
            continue
        visited.add(current)
        print('visited new node')
        neighbours = getNeighbours(current)
        for neighbour in neighbours:
            print(neighbour)
            if neighbour in visited:
                continue
            print('nieghbour not visited')
            prev_node[neighbour] = current
            g[neighbour] = g[current] + 1
            if len(appState.matrix.matrix[neighbour[0]][neighbour[1]].stack) > 0:
                print('neighbour has stack')
                foundStack = True
                path = []
                prev = neighbour
                closestG = g[neighbour]
                while prev is not None:
                    path.append(prev)
                    prev = prev_node[prev]
                path.reverse()
                #closest.append((neighbour, g[neighbour], path)
                closest.append(path)
            if not foundStack:
                q.append(neighbour)
    if closest == []:
        print(startPos)
    return closest

#moguca odredista za trenutno selektovano polje
def possibleDestinations(startPos):
    destinations = []
    neighbours = getNeighbours(startPos)
    for neighbour in neighbours:
        if len(appState.matrix.matrix[neighbour[0]][neighbour[1]].stack) > 0:
            destinations.append(neighbour)
    if (len(destinations) > 0):
        return list(map(lambda x: [startPos, x], destinations)), True
    print(startPos)
    nearestStacks = findNearestDestBFS(startPos)
    print(nearestStacks)
    return nearestStacks, False

# def diagonalHeuristics(pos, dest):
#     dx = abs(pos[0] - dest[0])
#     dy = abs(pos[1] - dest[1])
#     return (dx + dy) - 0.587 * min(dx, dy)

# def findShortestRoute(startPos, destPos):
#     end = False
#     openSet = set()
#     closedSet = set()
#     openSet.add(startPos)
#     g = {}
#     g[startPos] = 0
#     prev_node = {}
#     prev_node[startPos] = None
#     while len(openSet) > 0 and not end:
#         current = None
#         for pos in openSet:
#             if current is None or g[pos] + diagonalHeuristics(pos, destPos) < g[current] + diagonalHeuristics(current, destPos):
#                 current = pos
#         if current == destPos:
#             end = True
#             break
#         for neighbour in getNeighbours(current):
#             if neighbour not in openSet and neighbour not in closedSet:
#                 openSet.add(neighbour)
#                 prev_node[neighbour] = current
#                 g[neighbour] = g[current] + 1
#             else:
#                 if g[neighbour] > g[current] + 1:
#                     g[neighbour] = g[current] + 1
#                     prev_node[neighbour] = current
#                     if neighbour in closedSet:
#                         closedSet.remove(neighbour)
#                         openSet.add(neighbour)
#         openSet.remove(current)
#         closedSet.add(current)
#     path = []
#     if end:
#         pos = destPos
#         while prev_node[pos] is not None:
#             path.append(pos)
#             pos = prev_node[pos]
#         path.append(startPos)
#         path.reverse()
#     return path

# def findNearestDests(startPos):
#     paths = []
#     searchesConducted = 0
#     print("for search")
#     for i in range(appState.matrixSize):
#         for j in range(appState.matrixSize):
#             if len(appState.matrix.matrix[i][j].stack) > 0 and (i, j) != startPos:
#                 newPath = findShortestRoute(startPos, (i, j))
#                 searchesConducted += 1
#                 if not paths:
#                     paths.append(newPath)
#                 if paths and len(newPath) < len(paths[0]):
#                     paths.clear()
#                 if paths and len(newPath) > len(paths[0]):
#                     continue
#                 paths.append(newPath)
                
#     print("Searches: " + str(searchesConducted))
#     return paths
    


#f-------------------------for AI --------------------------
def get_valid_moves(appState, ai_color):
    valid_moves = []
    stack_count = 0
    for row in range(appState.matrixSize):
        for col in range(appState.matrixSize):
            field = appState.matrix.matrix[row][col]
            if field.stack and list(filter(lambda x: x.color == ai_color, field.stack)):
                stack_count += 1
                # Generate valid moves for each stack
                for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    destPos = (row + dx, col + dy)
                    if validField(destPos):
                        for sliceIndex in range(len(field.stack)):
                            print("ROW I COL SU "+str(row)+str(col))
                            validity, reason = checkMove((row, col), sliceIndex, destPos)
                            if validity:
                                valid_moves.append(((row, col), sliceIndex, destPos))

    return valid_moves

def evaluate_game_state():
    global AppState
    ai_control = 0
    potential_moves = 0
    ai_color = list(filter(lambda x: x.type == PlayerType.Computer, appState.players))[0].color
    for row in range(appState.matrixSize):
        for col in range(appState.matrixSize):
            field = appState.matrix.matrix[row][col]
            if field.stack:
                    # Count stacks controlled by AI
                if field.stack[-1].color == ai_color:
                    ai_control += 1
                    # Count potential moves for AI
                if field.stack[0].color == ai_color:
                    potential_moves += len(possibleDestinations((row, col)))

        # Scoring function can be adjusted based on game strategy
    return ai_control + potential_moves

def is_terminal_node():
        # Check if the game has reached the win condition for either player
        if appState.finished == True:
            return True
        return False

def apply_move(move):  # samo privremeno nek ode potez u appState
    global appState
    previous_state = appState.copy_state()
    # 'move' should contain all necessary information like startPos, sliceIndex, and destPos
    appState.set_state(move[0], move[1], move[2])
    return previous_state
def undo_move(previous_state):
        global appState 
        appState = previous_state

def minmax(depth, maximizingPlayer):
        if depth == 0 or is_terminal_node():
            return evaluate_game_state()

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in get_valid_moves(appState, appState.get_opponent(appState.currentPlayer).color):
                prevState = apply_move(move)
                eval = minmax(depth - 1, False)
                maxEval = max(maxEval, eval)
                undo_move(prevState)
            return maxEval
        else:
            minEval = float('inf')
            for move in get_valid_moves(appState, appState.currentPlayer.color):
                prevState = apply_move(move)
                eval = minmax(depth - 1, True)
                minEval = min(minEval, eval)
                undo_move(prevState)
            return minEval
#--------------------------------------------------------------------------------------
choice_singleplayer = ("singleplayer", "multiplayer")
singleplayer_text = "Izaberite mod igre"
alert_sp = tp.AlertWithChoices("", choice_singleplayer, singleplayer_text, choice_mode="h")
choices_whos_first = ("player", "computer")
whos_first_text = "Ko prvi igra?"
alert2 = tp.AlertWithChoices("", choices_whos_first, whos_first_text, choice_mode="h")
choices_matix = ("8", "10", "12", "14", "16")
matrix_text = "Koju zelite dimeziju grida?"
alert1 = tp.AlertWithChoices("", choices_matix, matrix_text, choice_mode="v")
#set alert bacground color to be black and text color to be white and for theis hover state to be red for the choices

alert1.set_bck_color(WHITE, "all", True, True, False)
alert1.set_font_color(BLUE, ["hover", "pressed"], True, True, True)
alert2.set_bck_color(WHITE, "all", True, True, False)
alert2.set_font_color(BLUE,  ["hover", "pressed"], True, True, True)
alert_sp.set_bck_color(WHITE, "all", True, True, False)
alert_sp.set_font_color(BLUE, ["hover", "pressed"], True, True, True)


launcher = tp.Button("Kreni sa igrom")
launcher.set_topleft(10, 10)
launcher.at_unclick = user_choice
launcher.set_font_color(BLUE, "all", True, True, True)
launcher.at_hover = lambda: launcher.set_font_color(WHITE, "all", True, True, True)
launcher.set_bck_color(BLACK)
loop = launcher.get_updater(fps=60)

clock = pygame.time.Clock()
iteration = 0

while loop.playing:
    clock.tick(loop.fps)
    events = pygame.event.get()
    if appState and appState.currentPlayer.type == PlayerType.Player:
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    appState.switchPlayer()
            if e.type == pygame.QUIT:
                loop.playing = False
            if e.type == pygame.MOUSEBUTTONUP:
                if appState and not appState.currentMove[0]:
                    print("selekting mica")
                    selectMica(pygame.mouse.get_pos())
                    
                elif appState and appState.currentMove[0] and not appState.currentMove[2]:
                    print("selekting dest square")
                    dest = selectDestSquare(pygame.mouse.get_pos())
                    if (dest):
                        performMove()
                        if (appState.finished):
                            print("finished")
                            
                            
    elif appState and appState.currentPlayer.type == PlayerType.Computer:
        aiMove()

    loop.update(blit_before_gui, events=events)
    pygame.display.flip()
    iteration += 1


pygame.quit()