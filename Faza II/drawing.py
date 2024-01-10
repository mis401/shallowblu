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
pygame.display.set_caption('Shallow blue')
tp.init(screen, tp.theme_human)  


matrix_size = 0
whos_first=""
isSingleplayer = False
isAiFirst = False
possible_moves = []

def user_choice():
    global matrix_size
    global initialState
    global appState
    global isSingleplayer
    global isAiFirst
    alert_start.launch_alone()

    launcher.set_invisible(True)    
    if initialState == False:
        alert_sp.launch_alone(func_before=blit_before_gui)
        alert_size.launch_alone(func_before=blit_before_gui)
        #alert1._at_click = close_alert
        if (alert_sp.choice == "singleplayer"):        
            alert_whos_first.launch_alone(func_before=blit_before_gui)
            isSingleplayer = True 

    print("User has chosen:", alert_size.choice)
    try:
        matrix_size = int(alert_size.choice)
        print(matrix_size)
        whos_first = alert_whos_first.choice
        print(whos_first)
        if (whos_first == "computer"):
            isAiFirst = True
        if appState == None and initialState == False:
            print("usao u if")
            appState = AppState(matrix_size, whos_first, alert_sp.choice)
            initialState = True
    except Exception as e:
        print(e)
        pass

def blit_before_gui():
    global isAiFirst
    gradient = tp.graphics.color_gradient((BLUE, WHITE), (W, H), "v")
    screen.blit(gradient, (0, 0))

    if not appState:
        return
    draw_chessboard()
    draw_boxes_for_scores()

     # Da pise ciji je red 
    font = pygame.font.Font(None, 36)  

    if appState and appState.currentPlayer:
        if appState.currentPlayer.type == PlayerType.Player:
            text_color=BLUE if isAiFirst else BEIGE
            turn_text = "Your turn"
            text_position = (10, 10) if not isAiFirst else (W - 150, 10)
        else:
            text_color=BEIGE if isAiFirst else BLUE
            turn_text = "AI's turn"
            text_position = (W - 150, 10) if not isAiFirst else (10, 10) 

        turn_surface = font.render(turn_text, True, text_color)
        screen.blit(turn_surface, text_position)

    pygame.display.update()
    if appState and appState.finished == True:
        winAlert = tp.Alert("Kraj igre", "Pobednik je: " + appState.currentPlayer.type.value)
        winAlert.launch_alone()
        loop.playing = False


def draw_chessboard():
    global possible_moves
    square_size = appState.square_size
    total_width = matrix_size * square_size
    total_height = matrix_size * square_size
    if appState:
        matrix = appState.matrix.matrix
        center_x = (screen.get_width() - total_width) // 2
        center_y = (screen.get_height() - total_height) // 2

        for row in range(matrix_size):
            for col in range(matrix_size):
                
                selected = appState.currentMove and appState.currentMove[0] == (row, col)
                possible_move = (row, col) in possible_moves

                draw_square(matrix[row][col], center_x+col*square_size, center_y+row*square_size, square_size,  selected or possible_move)

def draw_boxes_for_scores():
    if not appState:
        return
    global isSingleplayer
    global isAiFirst
    box_width, box_height = 100, 50  
    border_thickness = 2  
    box_margin = 10  
    border_color = (0, 0, 0)  

    font = pygame.font.Font(None, 33)  # Adjust the font size as needed

    player_name="AI" if isSingleplayer else "Player2"
    if isAiFirst:
        players = [("AI", appState.players[0].score), ("YOU", appState.players[1].score)]
    else:
        players = [("YOU", appState.players[0].score), (player_name, appState.players[1].score)]

    for i, (player_name, score) in enumerate(players):
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

    color = GRAY if selected else (BLACK if field.color == Color.BLACK else WHITE)
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
    border_color = (0, 0, 0)  
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

    global possible_moves

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
        upInSquare = abs(inSquare - square_size)
        micaPos = int(upInSquare // (square_size / 8))
        print(micaPos)
        micaPos = min(micaPos, len(selectedSquare.stack)-1)
        if micaPos < 0:
            raise Exception("Prazno polje")
        print(micaPos)
           # da li je slektovana protivnicka mica
        if selectedSquare.stack and selectedSquare.stack[micaPos].color!= appState.currentPlayer.color:
            raise Exception("Pogresna boja")
        appState.currentMove[0] = (selectedRow, selectedCol)
        appState.currentMove[1] = micaPos


        possible_moves = []
        if appState and appState.currentMove[0]:
        # moguci potezi za selektovanu micu
            startPos = appState.currentMove[0]
            sliceIndex = appState.currentMove[1]
            moves = get_valid_moves(appState, appState.currentPlayer.color)
            for move in moves:
                if move[0] == startPos and move[1] == sliceIndex:
                    possible_moves.append(move[2])  

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
    global possible_moves
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

    possible_moves = []
    draw_chessboard()


def checkMove(startPos, sliceIndex, destPos):
    if not appState.matrix.matrix[startPos[0]][startPos[1]].stack:
        return False, "empty field"
    start_time = time.perf_counter_ns()
    end_time = time.perf_counter_ns()
    if (appState.matrix.matrix[startPos[0]][startPos[1]].stack[sliceIndex].color != appState.currentPlayer.color):
        end_time = time.perf_counter_ns()
        return False, "wrong color"
    
    dx = abs( startPos[0] - destPos[0])
    dy = abs(startPos[1] - destPos[1])
    if not dx == 1 or not dy == 1:
        end_time = time.perf_counter_ns()
        return False, "not adjacent"
    if len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) + \
        len(appState.matrix.matrix[startPos[0]][startPos[1]].stack[sliceIndex:]) > 8:
        end_time = time.perf_counter_ns()
        return False, "stack overflow"
    
    possiblePaths, neighbours = possibleDestinations(startPos)
    if not neighbours:
        if (appState.matrix.matrix[startPos[0]][startPos[1]].stack[0].color == appState.currentPlayer.color):
            appState.currentMove[1] = 0
            sliceIndex = 0
        else:
            return False, "does not own stack"

    print('\n')
    possibleDests = list(filter(lambda x: x[1] == destPos, possiblePaths))
    if len(possibleDests) == 0:
        end_time = time.perf_counter_ns()
        return False, "selected field not valid"
    if (len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) <= sliceIndex and sliceIndex != 0):
        end_time = time.perf_counter_ns()
        return False, "new position cant be lower than current"
    end_time = time.perf_counter_ns()
    return True, "ok"

waiting_bar = tp.WaitingBar("", length=200,rect_color=BEIGE, speed=2.5, rel_width=0.2, height=10,font_color=BLUE)
tp.set_waiting_bar(waiting_bar)

def aiMove():
    print("AI move")
    best_score = float('-inf')
    best_move = None
    moves = get_valid_moves(appState, appState.currentPlayer.color)
    for move in moves:
        previous_state = apply_move(move)
        score = minmax(depth=1, maximizingPlayer=False)  
        undo_move(previous_state)

        if score > best_score:
            best_score = score
            best_move = move
            print(move)

        tp.refresh_waiting_bar()

    if best_move:
        appState.currentMove = [best_move[0], best_move[1], best_move[2]]
        performMove()
        
    return best_move  

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



#f-------------------------for AI --------------------------

def get_valid_moves(appState, ai_color):
    valid_moves = []
    stack_count = 0
    for row in range(appState.matrixSize):
        for col in range(appState.matrixSize):
            field = appState.matrix.matrix[row][col]
            if field.stack and list(filter(lambda x: x.color == ai_color, field.stack)):
                stack_count += 1
                # generisi moguce poteze za svaki stek
                for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    destPos = (row + dx, col + dy)
                    if validField(destPos):
                        for sliceIndex in range(len(field.stack)):
                            validity, reason = checkMove((row, col), sliceIndex, destPos)
                            if validity:
                                valid_moves.append(((row, col), sliceIndex, destPos))

    return valid_moves

def evaluate_game_state():
    global appState
    ai_control = 0
    potential_moves = 0
    center_control = 0
    stack_mobility = 0
    ai_color = list(filter(lambda x: x.type == PlayerType.Computer, appState.players))[0].color
    center = appState.matrixSize // 2

    for row in range(appState.matrixSize):
        for col in range(appState.matrixSize):
            field = appState.matrix.matrix[row][col]
            if field.stack:
                # prebroj stekove koje kontrolise AI
                if field.stack[-1].color == ai_color:
                    ai_control += 1
                    # dodatni poeni za kontrolisanje stekova blizu centra
                    center_distance = max(abs(center - row), abs(center - col))
                    center_control += (center - center_distance) ** 2
                #Racuna moguce poteze za AI
                if field.stack[0].color == ai_color:
                    move_options = len(possibleDestinations((row, col)))
                    potential_moves += move_options
                    #dodatni poeni za stekove sa vise opcija
                    stack_mobility += move_options ** 2

    # skoring funkcija je linearna kombinacija svih faktora
    return ai_control + potential_moves + center_control + stack_mobility


def is_terminal_node():
        # proveri da li je igra zavrsena
        if appState.finished == True:
            return True
        return False

def apply_move(move):  # samo privremeno nek ode potez u appState
    global appState
    previous_state = appState.copy_state()
    appState.set_state(move[0], move[1], move[2])
    return previous_state
def undo_move(previous_state):
        global appState 
        appState = previous_state

def minmax(depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or is_terminal_node():
        return evaluate_game_state()

    if maximizingPlayer:
        maxEval = float('-inf')
        for move in get_valid_moves(appState, appState.get_opponent(appState.currentPlayer).color):
            prevState = apply_move(move)
            eval = minmax(depth - 1, False, alpha, beta)
            maxEval = max(maxEval, eval)
            undo_move(prevState)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for move in get_valid_moves(appState, appState.currentPlayer.color):
            prevState = apply_move(move)
            eval = minmax(depth - 1, True, alpha, beta)
            minEval = min(minEval, eval)
            undo_move(prevState)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
#--------------------------------------------------------------------------------------
choice_singleplayer = ("singleplayer", "multiplayer")
singleplayer_text = "Izaberite mod igre"
alert_sp = tp.AlertWithChoices("", choice_singleplayer, singleplayer_text, choice_mode="h")
choices_whos_first = ("player", "computer")
whos_first_text = "Ko prvi igra?"
alert_whos_first = tp.AlertWithChoices("", choices_whos_first, whos_first_text, choice_mode="h")
choices_matix = ("8", "10", "12", "14", "16")
matrix_text = "Koju zelite dimeziju grida?"
alert_size = tp.AlertWithChoices("", choices_matix, matrix_text, choice_mode="v")

alert_size.set_bck_color(WHITE, "all", True, True, False)
alert_size.set_font_color(BLUE, ["hover", "pressed"], True, True, True)
alert_whos_first.set_bck_color(WHITE, "all", True, True, False)
alert_whos_first.set_font_color(BLUE,  ["hover", "pressed"], True, True, True)
alert_sp.set_bck_color(WHITE, "all", True, True, False)
alert_sp.set_font_color(BLUE, ["hover", "pressed"], True, True, True)

alert_start = tp.Alert("", "Dobrodosli u igru Byte. \n Pravila igre su sledeca: \n 1. Igra se na tabli dimenzija NxN, gde je N broj koji cete izabrati. \n 2. Igra se izmedju dva igraca, crni i beli. \n 3. Prvi igrac selektuje jednu od svojih mica, a zatim jedno od polja na koje moze da se pomeri. \n 4. Mica se moze pomeriti na sva polja koja su dijagonalno susedna, i na kojima se ne nalazi veci stek. \n 5. Ukoliko ne postoji moguci potez za igranje pritisnite SPACE  \n 6. Igrac dobija onaj napunjeni stek na cijem je vrhu njegova boja  \n  7. Pobednik je igrac koji ima vise osvojenih stekova na kraju igre. \n  Srecno!")
alert_start.set_font_color(BLUE, "all", True, True, True)
alert_start.set_bck_color(WHITE, "all", True, True, False)
alert_start.set_opacity_bck_color(200, "all", True, True, False)

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