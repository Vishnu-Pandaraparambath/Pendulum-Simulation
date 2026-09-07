import pygame

# Screen setup
X_WIDTH = 1280
Y_WIDTH = 720
FPS = 60

CircleX = X_WIDTH / 2
CircleY = Y_WIDTH / 2
velocity = pygame.math.Vector2(0, 0)

GRAVITY = 9.81
RADIUS = 40
COLOUR = "Blue"
MASS = 3
energy = MASS * GRAVITY * (Y_WIDTH - CircleY)
WALL_ENERGY_COEFFICIENT = 0.3

# pygame setup
pygame.init()
screen = pygame.display.set_mode((X_WIDTH, Y_WIDTH))
clock = pygame.time.Clock()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE



    newYPos = CircleY + GRAVITY
    CircleY = min(newYPos, 720 - RADIUS)

    pygame.draw.circle(screen, COLOUR, (CircleX, CircleY), RADIUS)

    screen.fill("black")
    # redraw the circle
    pygame.draw.circle(screen, COLOUR, (CircleX, CircleY), 50)

    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60

pygame.quit()