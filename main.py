import pygame
import math

class Pendulum:
    def __init__(self, pivot, mass, length, colour):
        self.mass = mass
        self.length = length
        self.colour = colour
        self.pivot = pivot
        self.starting_angle = 90 * (math.pi / 180)


pendulumOne = Pendulum(pivot=(640, 360), mass=3, length=100, colour="Blue")

# Screen setup
X_WIDTH = 1280
Y_WIDTH = 720
FPS = 60
SCREEN_COLOUR = (255,255,255)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((X_WIDTH, Y_WIDTH))
screen.fill(SCREEN_COLOUR)
clock = pygame.time.Clock()
running = True
T = 0

def angleCompute(time, theta_max, length, damping=0):
    angular_velocity = math.sqrt(9.81 / length)
    decay = math.exp(-damping * time)
    angle = (theta_max * decay) * math.cos(angular_velocity * time)
    return angle


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE
    screen.fill(SCREEN_COLOUR)

    rotational_angle = angleCompute(T, pendulumOne.starting_angle, pendulumOne.length)
    x = pendulumOne.pivot[0] + math.sin(rotational_angle) * pendulumOne.length
    y = pendulumOne.pivot[1] + math.cos(rotational_angle) * pendulumOne.length
    endPos = (x, y)

    pygame.draw.line(surface=screen, color=pendulumOne.colour, start_pos=pendulumOne.pivot, end_pos=endPos, width=3)
    T += 0.1


    pygame.display.update()


    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60

pygame.quit()