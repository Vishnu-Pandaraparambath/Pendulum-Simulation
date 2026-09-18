import pygame
import math

class PygameWrapper:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def lineDraw(self, colour, start_pos, end_pos, width):
        pygame.draw.line(surface=self.screen, color=colour, start_pos=start_pos, end_pos=end_pos, width=width)

    def circleDraw(self, colour, centre, radius):
        pygame.draw.circle(surface=self.screen, color=colour, center=centre, radius=radius, width=0)


class Pendulum:
    def __init__(self, pivot, mass, length, width, colour):
        self.mass = mass
        self.length = length
        self.colour = colour
        self.pivot = pivot
        self.width = 3
        self.starting_angle = math.radians( 90 )



pendulumOne = Pendulum(pivot=(640, 360), mass=3, length=100, width=3, colour="Blue")

# Screen setup
X_WIDTH = 1280
Y_WIDTH = 720
FPS = 60
SCREEN_COLOUR = (255,255,255)


# pygame setup
pg = PygameWrapper()
screen = pg.screen
screen.fill(SCREEN_COLOUR)
clock = pg.clock
running = True
T = 0

def angleCompute(time, theta_max, length, damping= 0.0, gravity = 9.81):
    angular_velocity = math.sqrt(gravity / length)
    decay = math.exp(-damping * time)
    angle = (theta_max * decay) * math.cos(angular_velocity * time)
    return angle


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(SCREEN_COLOUR)

    rotational_angle = angleCompute(time=T, theta_max=pendulumOne.starting_angle, length=pendulumOne.length)
    x = pendulumOne.pivot[0] + math.sin(rotational_angle) * pendulumOne.length
    y = pendulumOne.pivot[1] + math.cos(rotational_angle) * pendulumOne.length
    endPos = (x, y)

    pg.lineDraw(colour=pendulumOne.colour, start_pos=pendulumOne.pivot, end_pos=endPos, width=pendulumOne.width)
    pg.circleDraw(colour="Black", centre=endPos, radius=5)
    T += 0.1


    pygame.display.update()
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()