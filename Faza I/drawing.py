import pygame
import math
import thorpy as tp
import time
from state import *

initialState = False
appState = None
selectedMica = None
selectedSquare = None
destSquare = None

pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W, H))
tp.init(screen, tp.theme_human)  # bind screen to gui elements and set theme


def blit_before_gui():
    white_value = 127 + math.sin(iteration * math.pi * 0.5 / loop.fps) * 127
    gradient = tp.graphics.color_gradient(((0, 0, 0), (white_value, white_value, white_value)), (W, H), "v")
    screen.blit(gradient, (0, 0))
    # draw_chessboard(matrix_size)
    # draw_small_shapes(matrix_size)
    if not appState:
        return
    draw_chessboard()
    if appState and appState.finished == True:
        winAlert = tp.Alert("Kraj igre", "Pobednik je: " + appState.currentPlayer.type.value)
        winAlert.launch_alone()
    
# def hardCodedStateChange():
#     move = ((2, 0), 0, (3, 0))
#     print(appState.matrix.matrix[3][0].stack)
#     appState.set_state(move[0], move[1], move[2])


def draw_square(field, x, y, square_size):
    color = (0, 0, 0) if field.color == Color.BLACK else (255, 255, 255)
    pygame.draw.rect(screen, color, [x, y, square_size, square_size])
    dy = square_size / 8
    bottom = y + square_size
    for mica in field.stack:
        draw_mica(mica, x, bottom-dy, square_size)
        bottom -= dy

def draw_mica(mica, x, y, width):

    height = width / 8
    color = (90, 90, 90) if mica.color == Color.BLACK else (150, 150, 150)
    mica=pygame.draw.rect(screen, color, [x, y, width, height])
    
def selectMica(pos):
    global selectedMica
    global selectedSquare
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
        print(inSquare)
        upInSquare = abs(inSquare - square_size)
        print(upInSquare)
        micaPos = int(upInSquare // (square_size / 8))
        #micaPos = ((len(selectedSquare.stack))+micaPos)%(len(selectedSquare.stack))
        print(micaPos)
        micaPos = min(micaPos, len(selectedSquare.stack)-1)
        #micaPos = selectedSquare["square"].stack[-micaPos] if micaPos >= len(selectedSquare["square"].stack) else selectedSquare["square"].stack[len(selectedSquare["square"].stack)-1]
        selectedMica = selectedSquare.stack[micaPos]
        #if not selectedMica.color == appState.currentPlayer.color:
        #    raise Exception("pogresna boja")
        appState.currentMove[0] = (selectedRow, selectedCol)
        appState.currentMove[1] = micaPos
        return True
    except Exception as e:
        appState.currentMove = [None, None, None]
        print(e)
        pass

def selectDestSquare(pos):
    global destSquare
    global selectedSquare
    global selectedMica
    square_size = 64
    try:
        total_width = matrix_size * square_size
        total_height = matrix_size * square_size
        matrix = appState.matrix.matrix
        top_left_x = (screen.get_width() - total_width) // 2
        top_left_y = (screen.get_height() - total_height) // 2
        selectedCol = (pos[0] - top_left_x) // square_size
        selectedRow = (pos[1] - top_left_y) // square_size
        destSquare = matrix[selectedRow][selectedCol]
        appState.currentMove[2] = (selectedRow, selectedCol)
        return True 
    except Exception as e:
        appState.currentMove = [None, None, None]
        print(e)
        pass
    

def draw_chessboard(square_size=64):
    total_width = matrix_size * square_size
    total_height = matrix_size * square_size

    # Calculate the position to center the chessboard


    # 
    
    if appState:
        matrix = appState.matrix.matrix
        center_x = (screen.get_width() - total_width) // 2
        center_y = (screen.get_height() - total_height) // 2

        for row in range(matrix_size):
            for col in range(matrix_size):
                draw_square(matrix[row][col], center_x+col*square_size, center_y+row*square_size, square_size)


choices_whos_first = ("player", "computer")
whos_first_text = "Ko prvi igra?"
alert2 = tp.AlertWithChoices("ko prvi igra?", choices_whos_first, whos_first_text, choice_mode="h")
choices_matix = ("8", "10", "12", "14", "16")
matrix_text = "Koju zelite dimeziju?"
alert1 = tp.AlertWithChoices("Grid dimenzija", choices_matix, matrix_text, choice_mode="v")


matrix_size = 0
whos_first=""
def my_func():
    global matrix_size  # Use global to modify the outer variable
    global initialState
    global appState
    if initialState == False:
        alert1.launch_alone()
        alert2.launch_alone()
    print("User has chosen:", alert1.choice)
    try:
        matrix_size = int(alert1.choice)
        print(matrix_size)
        whos_first = alert2.choice
        print('preprint')
        print(whos_first)
        if appState == None and initialState == False:
            print("usao u if")
            appState = AppState(matrix_size, whos_first)
            initialState = True
        

    except Exception as e:
        print(e)
        pass
launcher = tp.Button("Odaberi velicinu table")
launcher.set_topleft(10, 10)
launcher.at_unclick = my_func
launcher2= tp.Button("Ko igra prvi?")
launcher2.set_topleft(10, 50)



loop = launcher.get_updater(fps=60)
clock = pygame.time.Clock()
iteration = 0


def performMove():
    startPos = appState.currentMove[0]
    destPos = appState.currentMove[2]
    sliceIndex = appState.currentMove[1]
    if not checkMove(startPos, sliceIndex, destPos):
        print("nevalidan potez")
        appState.currentMove = [None, None, None]
        return
    print("prihvacen potez" + str(startPos) + str(sliceIndex) + str(destPos))
    appState.set_state(startPos, sliceIndex, destPos)
    appState.currentMove = [None, None, None]


def checkMove(startPos, sliceIndex, destPos):
    dx = abs( startPos[0] - destPos[0])
    dy = abs(startPos[1] - destPos[1])
    validity = False
    if dx == 1 and dy == 1:
        validity = True
    if len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) + len(appState.matrix.matrix[startPos[0]][startPos[1]].stack[sliceIndex:]) > 8:
        validity = False
    return validity

def aiMove():
    print("ai move")
    if appState:
        appState.switchPlayer()
    return


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