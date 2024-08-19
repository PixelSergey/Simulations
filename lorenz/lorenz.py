import pygame, sys, math, colorsys, os, random
from pygame.locals import *

pygame.init()

width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))

os.environ["SDL_VIDEO_CENTERED"]='1'
size = (width, height)
white, black = (200, 200, 200), (0, 0, 0)

sigma = 10+0.01*random.randint(-100,100)
row = 28+0.01*random.randint(-100,100)
beta = 8/3+0.005*random.randint(-100,100)
x, y, z = 0.01, 0, 0
points = []
colors = []
scale = 15
angle = 0
previous = None

clock = pygame.time.Clock()

def matrix_multiplication(a, b):
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    output = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                total = 0
                for k in range(columns_a):
                    total += a[x][k] * b[k][y]
                output[x][y] = total
        return output
    else:
        print("error! the columns of the first matrix must be equal with the rows of the second matrix")
        return None


def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


def checkevents():
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()


while True:
    checkevents()
    dt = clock.tick(120)/1000

    # If the game is too slow (usually due to being dragged and paused), skip the frame
    if dt >= 0.05:
        continue

    screen.fill((0,0,0))
    
    rotation_x = [[1, 0, 0],
                  [0, math.cos(angle), -math.sin(angle)],
                  [0, math.sin(angle), math.cos(angle)]]

    rotation_y = [[math.cos(angle), 0, -math.sin(angle)],
                  [0, 1, 0],
                  [math.sin(angle), 0, math.cos(angle)]]

    rotation_z =[[math.cos(angle), -math.sin(angle), 0],
                 [math.sin(angle), math.cos(angle), 0 ],
                  [0, 0, 1]]
    
    dx = (sigma * (y - x))*dt
    dy = (x * (row - z) - y)*dt
    dz = (x * y - beta * z)*dt

    x = x + dx
    y = y + dy
    z = z + dz
    hue = 0

    point = [[x], [y], [z]]
    points.append(point)
    
    for p in points:
        rotated_2d = matrix_multiplication(rotation_y, p)
        distance = 5

        val = 1/(distance - rotated_2d[2][0])
        projection_matrix = [[1, 0, 0],
                             [0, 1, 0]]

        projected2d = matrix_multiplication(projection_matrix, rotated_2d)
        x_pos = int(projected2d[0][0] * scale) + width//2 + 100
        y_pos = int(projected2d[1][0] * scale) + height//2
        if hue > 1:
            hue = 0
        
        if previous is not None:
            if hue >  0.006:
                pygame.draw.line(screen, (hsv2rgb(hue, 1, 1)), (x_pos, y_pos), previous, 4)

        previous = (x_pos, y_pos)
        hue += 0.006


    angle += 0.01

    pygame.display.update()

