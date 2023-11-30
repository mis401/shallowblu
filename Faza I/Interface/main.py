import pygame
import math
import thorpy as tp


pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W, H))
tp.init(screen, tp.theme_human)  # bind screen to gui elements and set theme

def blit_before_gui():
    # blue = 127 + math.sin(iteration*math.pi*0.5/loop.fps) * 127
    # gradient = tp.graphics.color_gradient(((0, 0, blue), (255, 255, 255)), (W, H), "v")
    # screen.blit(gradient, (0, 0))
    white_value = 127 + math.sin(iteration * math.pi * 0.5 / loop.fps) * 127
    gradient = tp.graphics.color_gradient(((0, 0, 0), (white_value, white_value, white_value)), (W, H), "v")
    screen.blit(gradient, (0, 0))
    draw_chessboard(matrix_size)

def draw_chessboard(matrix_size):
    square_size = 30
    total_width = matrix_size * square_size
    total_height = matrix_size * square_size

    # Calculate the position to center the chessboard
    center_x = (screen.get_width() - total_width) // 2
    center_y = (screen.get_height() - total_height) // 2

    for row in range(matrix_size):
        for col in range(matrix_size):
            color = (0, 0, 0) if (row + col) % 2 == 0 else (255, 255, 255)
            pygame.draw.rect(screen, color, [center_x + col * square_size, center_y + row * square_size, square_size, square_size])
choices_whos_first = ("player", "computer")
whos_first_text = "Ko prvi igra?"
alert2 = tp.AlertWithChoices("Tko prvi igra?", choices_whos_first, whos_first_text, choice_mode="h")
choices_matix = ("8", "10", "12", "14", "16")
matrix_text = "Koju zelite dimeziju?"
alert1 = tp.AlertWithChoices("Grid dimenzija", choices_matix, matrix_text, choice_mode="v")

matrix_size = 0
whos_first=""
def my_func():
    global matrix_size  # Use global to modify the outer variable
    alert1.launch_alone()
    alert2.launch_alone()
    print("User has chosen:", alert1.choice)
    try:
        matrix_size = int(alert1.choice)
        whos_first = alert2.choice
    except:
        pass
launcher = tp.Button("Odaberi velicinu table")
launcher.set_topleft(10, 10)
launcher.at_unclick = my_func
launcher2= tp.Button("Ko igra prvi?")
launcher2.set_topleft(10, 50)



loop = launcher.get_updater(fps=60)
clock = pygame.time.Clock()
iteration = 0

while loop.playing:
    clock.tick(loop.fps)
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            loop.playing = False
    
    loop.update(blit_before_gui, events=events)
    pygame.display.flip()
    iteration += 1

pygame.quit()