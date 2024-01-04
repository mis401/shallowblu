import sys

print(sys.executable)

import queue
import pygame
import math
import thorpy as tp
import time
from state import *

RED=(128,0,0)
DARK_RED=(75,15,15)
GRAY=(124,124,124)
BLUE= (15,67,146)
initialState = False
appState = None
selectedMica = None
selectedSquare = None
destSquare = None

pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W, H))
tp.init(screen, tp.theme_human)  # bind screen to gui elements and set theme


matrix_size = 0
whos_first=""
#funkcije za zatvaranje popup prozora manuelno
def close_alert():
    alert1.unlaunch()
    alert_sp.unlaunch()
def my_func():
    global matrix_size
    global initialState
    global appState
    launcher.set_invisible(True)    
    if initialState == False:
        alert_sp.launch_alone(func_before=blit_before_gui)
        alert1.launch_alone(func_before=blit_before_gui)
        alert1._at_click = close_alert
        if (alert_sp.choice == "singleplayer"):
            alert2.launch_alone(func_before=blit_before_gui)
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
    white_value = 127 + math.sin(iteration * math.pi * 0.5 / loop.fps) * 127
    gradient = tp.graphics.color_gradient(((0, 0, 0), (white_value, white_value, white_value)), (W, H), "v")
    screen.blit(gradient, (0, 0))
    # draw_chessboard(matrix_size)
    # draw_small_shapes(matrix_size)
    if not appState:
        return
    draw_chessboard()
    draw_boxes_for_scores()
    pygame.display.update()
    if appState and appState.finished == True:
        winAlert = tp.Alert("Kraj igre", "Pobednik je: " + appState.currentPlayer.type.value)
        winAlert.launch()
       # loop.playing = False


def draw_chessboard(square_size=64):
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
    box_width, box_height = 100, 50  
    border_thickness = 2  
    box_margin = 10  
    border_color = (0, 0, 0)  

    font = pygame.font.Font(None, 33)  # Adjust the font size as needed

    # ovde treba zapravo score koji brojimo
    players = [("YOU", 0), ("AI", 0)]

    for i, (player_name, score) in enumerate(players):
        # i = 0, igrac je na levoj strani, inace na desnoj
        x = box_margin if i == 0 else screen.get_width() - box_width - box_margin
        y = screen.get_height() - box_height - box_margin

         # UI razliciti detalji za svakog igraca
        box_color = RED if i==0 else BLUE
        text_color = RED if i==0 else BLUE
        name_padding = 25 if i==0 else 40

        # Draw the border
        pygame.draw.rect(screen, border_color, (x - border_thickness, y - border_thickness, box_width + 2*border_thickness, box_height + 2*border_thickness))
        # Draw the inner box
        pygame.draw.rect(screen, box_color, (x, y, box_width, box_height))

        name_text = font.render(player_name, True, text_color)
        screen.blit(name_text, (x + name_padding, y - 30))  

        score_text = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (x + 45, y + 15))  


    

def draw_square(field, x, y, square_size, selected = False):
    color = (0, 0, 0) if field.color == Color.BLACK else (255, 255, 255)
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
    color = BLUE if mica.color == Color.BLACK else RED
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

    square_size = 64
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
        print(micaPos)
        appState.currentMove[0] = (selectedRow, selectedCol)
        appState.currentMove[1] = micaPos
        return True
    except Exception as e:
        appState.currentMove = [None, None, None]
        print(e)
        pass

def selectDestSquare(pos):
    square_size = 64
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
    if not checkMove(startPos, sliceIndex, destPos):
        print("nevalidan potez")
        appState.currentMove = [None, None, None]
        return
    startPos = appState.currentMove[0]
    destPos = appState.currentMove[2]
    sliceIndex = appState.currentMove[1]
    print("prihvacen potez" + str(startPos) + str(sliceIndex) + str(destPos))
    appState.set_state(startPos, sliceIndex, destPos)
    appState.currentMove = [None, None, None]


def checkMove(startPos, sliceIndex, destPos):
    dx = abs( startPos[0] - destPos[0])
    dy = abs(startPos[1] - destPos[1])
    if not dx == 1 or not dy == 1:
        return False
    if len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) + \
        len(appState.matrix.matrix[startPos[0]][startPos[1]].stack[sliceIndex:]) > 8:
        return False
    possiblePaths = possibleDestinations()
    sliceIndex = appState.currentMove[1]
    print('\n')
    print(possiblePaths)
    possibleDests = list(filter(lambda x: x[1] == destPos, possiblePaths))
    if len(possibleDests) == 0:
        return False
    if (len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) <= appState.currentMove[1] and appState.currentMove[1] != 0):
        return False
    return True

def aiMove():
    print("ai move")
    if appState:
        appState.switchPlayer()
    return

#okvir table
def validField(field):
    return field[0] >= 0 and field[0] < matrix_size and field[1] >= 0 and field[1] < matrix_size

#vraca dijagonalno susedna polja 
def getNeighbours(field):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbours = []
    for direction in directions:
        dest = (field[0] + direction[0], field[1] + direction[1])
        if validField(dest):
            neighbours.append(dest)
    return neighbours

#BFS koji vraca najblize stackove
# def findNearestDests(startPos):
#     print("find nearest dests")
#     closest = set()
#     q = []
#     visited = set()
#     q.append(startPos)
#     foundStack = False
#     g = {}
#     g[startPos] = 0
#     prev_node = {}
#     prev_node[startPos] = None
#     while len(q) > 0:
#         current = q.pop()
#         if current in visited:
#             continue
#         visited.add(current)
#         neighbours = getNeighbours(current)
#         for neighbour in neighbours:
#             if neighbour in visited:
#                 continue
#             prev_node[neighbour] = current
#             g[neighbour] = g[current] + 1
#             if len(appState.matrix.matrix[neighbour[0]][neighbour[1]].stack) > 0:
#                 foundStack = True
#                 path = []
#                 prev = neighbour
#                 while prev is not None:
#                     path.append(prev)
#                     prev = prev_node[prev]
#                 path.reverse()
#                 #closest.append((neighbour, g[neighbour], path)
#                 closest.add(path[1])
#             if not foundStack:
#                 q.append(neighbour)
#     return closest



def diagonalHeuristics(pos, dest):
    dx = abs(pos[0] - dest[0])
    dy = abs(pos[1] - dest[1])
    return (dx + dy) - 0.587 * min(dx, dy)

def findShortestRoute(startPos, destPos):
    end = False
    openSet = set()
    closedSet = set()
    openSet.add(startPos)
    g = {}
    g[startPos] = 0
    prev_node = {}
    prev_node[startPos] = None
    while len(openSet) > 0 and not end:
        current = None
        for pos in openSet:
            if current is None or g[pos] + diagonalHeuristics(pos, destPos) < g[current] + diagonalHeuristics(current, destPos):
                current = pos
        if current == destPos:
            end = True
            break
        for neighbour in getNeighbours(current):
            if neighbour not in openSet and neighbour not in closedSet:
                openSet.add(neighbour)
                prev_node[neighbour] = current
                g[neighbour] = g[current] + 1
            else:
                if g[neighbour] > g[current] + 1:
                    g[neighbour] = g[current] + 1
                    prev_node[neighbour] = current
                    if neighbour in closedSet:
                        closedSet.remove(neighbour)
                        openSet.add(neighbour)
        openSet.remove(current)
        closedSet.add(current)
    path = []
    if end:
        pos = destPos
        while prev_node[pos] is not None:
            path.append(pos)
            pos = prev_node[pos]
        path.append(startPos)
        path.reverse()
    return path

def findNearestDests(startPos):
    paths = []
    for i in range(appState.matrixSize):
        for j in range(appState.matrixSize):
            if len(appState.matrix.matrix[i][j].stack) > 0 and (i, j) != startPos:
                newPath = findShortestRoute(startPos, (i, j))
                if not paths:
                    paths.append(newPath)
                if paths and len(newPath) < len(paths[0]):
                    paths.clear()
                if paths and len(newPath) > len(paths[0]):
                    continue
                paths.append(newPath)
    return paths
    
#moguca odredista za trenutno selektovano polje
def possibleDestinations():
    if not appState and not appState.currentMove[0]:
        return []
    startPos = appState.currentMove[0]
    destinations = []
    neighbours = getNeighbours(startPos)
    for neighbour in neighbours:
        if len(appState.matrix.matrix[neighbour[0]][neighbour[1]].stack) > 0:
            destinations.append(neighbour)
    if (len(destinations) > 0):
        return list(map(lambda x: [appState.currentMove[0], x], destinations))
    nearestStacks = findNearestDests(startPos) 
    appState.currentMove[1] = 0 #mora da pomeri ceo stack jer nema suseda na koji moze da se popne
    print(nearestStacks)
    return nearestStacks

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

alert1.set_bck_color((0, 0, 0), "all", True, True, False)
alert1.set_font_color(RED, ["hover", "pressed"], True, True, True)
alert2.set_bck_color((0, 0, 0), "all", True, True, False)
alert2.set_font_color(RED,  ["hover", "pressed"], True, True, True)
alert_sp.set_bck_color((0, 0, 0), "all", True, True, False)
alert_sp.set_font_color(RED, ["hover", "pressed"], True, True, True)


launcher = tp.Button("Kreni sa igrom")
launcher.set_topleft(10, 10)
launcher.at_unclick = my_func
launcher.set_font_color(RED, "all", True, True, True)
launcher.at_hover = lambda: launcher.set_font_color((255, 0, 0), "all", True, True, True)
launcher.set_bck_color((0, 0, 0))
loop = launcher.get_updater(fps=60)

clock = pygame.time.Clock()
iteration = 0

while loop.playing:
    clock.tick(loop.fps)
    events = pygame.event.get()
    if appState and appState.currentPlayer.type == PlayerType.Player:
        for e in events:
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