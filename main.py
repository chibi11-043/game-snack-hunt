import pygame, sys, random
from pygame.locals import *
SCREEN_WIDTH = 641
SCREEN_HEIGHT = 541
FPS = 3
TILE_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def headMap():
    global screen
    global bodySnake
    global level
    fontName = pygame.font.SysFont('arial', 50)
    fontPoint = pygame.font.SysFont('arial', 25)
    fontLevel = pygame.font.SysFont('arial', 25)
    gameHeader = fontName.render('Snake Game', True, RED)
    gamePoint = fontPoint.render('Point: ' + str(len(bodySnake) - 3), True,
                                 GREEN)
    gameLevel = fontLevel.render('Level: ' + str(level), True, GREEN)
    screen.blit(gameHeader, (5, 5))
    screen.blit(gamePoint, (400, 35))
    screen.blit(gameLevel, (530, 35))


def drawMap():
    for i in range(3, 28, 1):
        pygame.draw.line(screen, WHITE, (0, i * TILE_SIZE),
                         (639, i * TILE_SIZE))
    for i in range(33):
        pygame.draw.line(screen, WHITE, (i * TILE_SIZE, 60),
                         (i * TILE_SIZE, 539))


def drawSnake(bodynake):
    for i in bodySnake:
        x, y = i
        drawBody = pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1,
                               TILE_SIZE - 1, TILE_SIZE - 1)
        pygame.draw.rect(screen, GREEN, drawBody)


def wallCollide(direction):
    return not (0 <= bodySnake[0][0] <= 31 and 3 <= bodySnake[0][1] <= 26)


def bodyCollide(bodySnake):
    if bodySnake[0] in bodySnake[1:]:
        return True
    return False


def lose():
    global screen
    font = pygame.font.SysFont('arial', 50)
    gameOver = font.render('Game Over!', True, RED)
    screen.blit(gameOver, (180, 250))


def move(direction):
    global bodySnake
    if direction == 'East':
        for i in range(len(bodySnake) - 1, 0, -1):
            bodySnake[i] = bodySnake[i - 1].copy()
        bodySnake[0][0] += 1
    elif direction == 'West':
        for i in range(len(bodySnake) - 1, 0, -1):
            bodySnake[i] = bodySnake[i - 1].copy()
        bodySnake[0][0] -= 1
    elif direction == 'South':
        for i in range(len(bodySnake) - 1, 0, -1):
            bodySnake[i] = bodySnake[i - 1].copy()
        bodySnake[0][1] += 1
    elif direction == 'North':
        for i in range(len(bodySnake) - 1, 0, -1):
            bodySnake[i] = bodySnake[i - 1].copy()
        bodySnake[0][1] -= 1
    drawSnake(bodySnake)


def randomFood():
    global bodySnake
    randomXY = [random.randint(0, 31), random.randint(3, 26)]
    while randomXY in bodySnake:
        randomXY = [random.randint(0, 31), random.randint(3, 26)]
    return randomXY


def drawFood(randomXY):
    global screen
    food = pygame.Rect(randomXY[0] * TILE_SIZE + 1,
                       randomXY[1] * TILE_SIZE + 1, TILE_SIZE - 1,
                       TILE_SIZE - 1)
    pygame.draw.rect(screen, RED, food)


def eatFood(direction):
    global bodySnake
    last = len(bodySnake) - 1
    if direction == 'East':
        newRear = [bodySnake[last][0] + 1, bodySnake[last][1]]
        bodySnake.insert(last + 1, newRear)
    elif direction == 'West':
        newRear = [bodySnake[last][0] - 1, bodySnake[last][1]]
        bodySnake.insert(last + 1, newRear)
    elif direction == 'South':
        newRear = [bodySnake[last][0], bodySnake[last][1] + 1]
        bodySnake.insert(last + 1, newRear)
    elif direction == 'North':
        newRear = [bodySnake[last][0], bodySnake[last][1] - 1]
        bodySnake.insert(last + 1, newRear)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
bodySnake = [[15, 11], [14, 11], [13, 11]]
level = 1
direction = 'East'
eaten = True
speed = pygame.time.Clock()
while True:
    for i in pygame.event.get():
        if i.type == QUIT:
            pygame.quit()
            sys.exit()
        elif i.type == KEYDOWN:
            if i.key == K_w and direction != 'South':
                direction = 'North'
            elif i.key == K_s and direction != 'North':
                direction = 'South'
            elif i.key == K_a and direction != 'East':
                direction = 'West'
            elif i.key == K_d and direction != 'West':
                direction = 'East'
    screen.fill(BLACK)
    headMap()
    drawMap()
    if wallCollide(direction) or bodyCollide(bodySnake):
        lose()
    else:
        if eaten:
            randomXY = randomFood()
            eaten = False
        drawFood(randomXY)
        move(direction)
        if bodySnake[0] == randomXY:
            eaten = True
            eatFood(direction)
        if len(bodySnake) % 7 == 6 and eaten:
            level = level + 1
    pygame.display.update()
    speed.tick(FPS + level)