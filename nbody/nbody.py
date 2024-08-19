import pygame, sys, math
from pygame.locals import *

pygame.init()

width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))

G = 1000000
scale = 10
maxvel = 1000

pi = math.pi
sin = math.sin
cos = math.cos
atan2 = math.atan2
clock = pygame.time.Clock()

bodies = []


class Body:
    def __init__(self, m, x, y, vx, vy):
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0

    def force(self, Fx, Fy):
        self.ax += Fx/self.m
        self.ay += Fy/self.m

    def attract(self, other):
        dx = other.x - self.x
        dy = other.y - self.y 
        r2 = dx**2 + dy**2
        if r2 < 100: r2 = 100
        if r2 > 10000: r2 = 10000
        Fg = (G*(self.m*other.m))/r2
        Fy = Fg*sin(atan2(dy,dx))
        Fx = Fg*cos(atan2(dy,dx))
        self.force(Fx, Fy)

    def accelerate(self, dt, bodies):
        self.ax = 0
        self.ay = 0
        
        for body in bodies:
            if body is self:
                continue
            self.attract(body)

        vel = (self.vx**2 + self.vy**2)**0.5
        if vel > maxvel:
            self.vy = maxvel*sin(atan2(self.vy, self.vx))
            self.vx = maxvel*sin(atan2(self.vy, self.vx))
        self.vx += self.ax*dt
        self.vy += self.ay*dt
        self.x += self.vx*dt
        self.y += self.vy*dt


def checkevents():
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()


def drawinfo():
    pass

# Circular motion
#bodies.append(Body(1, 1000, 300, 250, 0))
#bodies.append(Body(10, 1000, 500, 0, 0))

# 3-body
bodies.append(Body(1, 1000, 300, 0, 0))
bodies.append(Body(1.5, 300, 300, 0, 0))
bodies.append(Body(1, 650, 700, 0, 0))

while True:
    checkevents()
    dt = clock.tick(120)/1000

    # If the game is too slow (usually due to being dragged and paused), skip the frame
    if dt >= 0.05:
        continue

    screen.fill((0,0,0))

    for body in bodies:
        body.accelerate(dt, bodies)

    for body in bodies:
        pygame.draw.circle(screen, (255,255,255), (body.x,body.y), scale*body.m)

    drawinfo()

    pygame.display.update()
