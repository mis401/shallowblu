import time
from drawing import possibleDestinations
from state import AppState, Color

def checkMove(appState, startPos, sliceIndex, destPos):
    
    start_time = time.perf_counter_ns()
    end_time = time.perf_counter_ns()
    if (appState.matrix.matrix[startPos[0]][startPos[1]].stack[sliceIndex].color != appState.currentPlayer.color):
        end_time = time.perf_counter_ns()
        print("check move time: " + str(end_time - start_time))
        return False
    dx = abs( startPos[0] - destPos[0])
    dy = abs(startPos[1] - destPos[1])
    if not dx == 1 or not dy == 1:
        end_time = time.perf_counter_ns()
        print("check move time: " + str(end_time - start_time))
        return False
    if len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) + \
        len(appState.matrix.matrix[startPos[0]][startPos[1]].stack[sliceIndex:]) > 8:
        end_time = time.perf_counter_ns()
        print("check move time: " + str(end_time - start_time))
        return False
    possiblePaths = possibleDestinations()
    sliceIndex = appState.currentMove[1]
    print('\n')
    print(possiblePaths)
    possibleDests = list(filter(lambda x: x[1] == destPos, possiblePaths))
    if len(possibleDests) == 0:
        end_time = time.perf_counter_ns()
        print("check move time: " + str(end_time - start_time))
        return False
    if (len(appState.matrix.matrix[destPos[0]][destPos[1]].stack) <= appState.currentMove[1] and appState.currentMove[1] != 0):
        end_time = time.perf_counter_ns()
        print("check move time: " + str(end_time - start_time))
        return False
    end_time = time.perf_counter_ns()
    print("check move time: " + str(end_time - start_time))
    return True


    

