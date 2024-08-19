import pygame, sys, math
from pygame.locals import *

pygame.init()

width = 1200
height = 600
screen = pygame.display.set_mode((width, height))

g = 9.81
pi = math.pi
sin = math.sin
cos = math.cos
clock = pygame.time.Clock()

lscale = 1000  # Scale length when drawing from metres to pixels
mscale = 250   # Scale mass when drawing from kilogrammes to pixel radius
dampen = 1 # Dampening factor

p0 = (width/2, height/4) # Initial position

l1 = 0.2  # Length 1, in metres
l2 = 0.2  # Length 2, in metres
m1 = 0.1   # Mass 1, in kilogrammes
m2 = 0.1   # Mass 2, in kilogrammes
t1 = -pi/2  # Initial angle 1, in radians
t2 = pi/1  # Initial angle 2, in radians
v1 = 0     # Initial velocity 1, in m/s
v2 = 0     # Initial velocity 2, in m/s
a1 = 0     # Initial acceleration 1, in m/s^2
a2 = 0     # Initial acceleration 2, in m/s^2


def checkevents():
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()


def drawinfo():
    pass


def acceleration1():
    num1 = -g*(2*m1 + m2)*sin(t1)
    num2 = -m2*g*sin(t1-2*t2)
    num3 = -2*sin(t1-t2)*m2
    num4 = v2*v2*l2+v1*v1*l1*cos(t1-t2)
    den = l1*(2*m1 + m2 - m2*cos(2*t1 - 2*t2))
    return (num1 + num2 + num3*num4)/den


def acceleration2():
    num1 = 2*sin(t1-t2)
    num2 = v1*v1*l1*(m1+m2)
    num3 = g*(m1+m2)*cos(t1)
    num4 = v2*v2*l2*m2*cos(t1-t2)
    den = l2*(2*m1 + m2 - m2*cos(2*t1 - 2*t2))
    return (num1*(num2+num3+num4))/den


while True:
    checkevents()
    dt = clock.tick(60)/1000
    
    # If the game is too slow (usually due to being dragged and paused), skip the frame
    if dt >= 0.05:
        continue
    
    screen.fill((0,0,0))

    x1 = l1*sin(t1)
    y1 = l1*cos(t1)
    x2 = l2*sin(t2)
    y2 = l2*cos(t2)

    p1 = (int(p0[0] + x1*lscale), int(p0[1] + y1*lscale))
    p2 = (int(p1[0] + x2*lscale), int(p1[1] + y2*lscale))

    w1 = int(m1*mscale)
    w2 = int(m2*mscale)

    pygame.draw.line(screen, (255,255,255), p0, p1)
    pygame.draw.circle(screen, (255,255,255), p1, w1)
    pygame.draw.line(screen, (255,255,255), p1, p2)
    pygame.draw.circle(screen, (255,255,255), p2, w2)
    
    a1 = acceleration1()
    a2 = acceleration2()
    v1 += a1*dt
    v2 += a2*dt
    v1 *= dampen
    v2 *= dampen
    t1 += v1*dt
    t2 += v2*dt
    
    drawinfo()

    pygame.display.update()
