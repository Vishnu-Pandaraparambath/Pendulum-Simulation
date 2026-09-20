import pygame
import math

class PygameWrapper:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.FPS = 60
        self.SCREEN_COLOUR = (255,255,255)
        self.clock = pygame.time.Clock()

    def lineDraw(self, colour, start_pos, end_pos, width):
        pygame.draw.line(surface=self.screen, color=colour, start_pos=start_pos, end_pos=end_pos, width=width)

    def circleDraw(self, colour, centre, radius):
        pygame.draw.circle(surface=self.screen, color=colour, center=centre, radius=radius, width=0)

    def refresh(self):
        pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.FPS)


class Pendulum:
    def __init__(self, pivot, mass, length, width, colour):
        self.mass = mass
        self.length = length
        self.colour = colour
        self.pivot = pivot
        self.width = width
        self.starting_angle = math.radians( 90 )


    def angleCompute(self, time, damping=0.0, gravity=9.81):
        angular_velocity = math.sqrt(gravity / self.length)
        decay = math.exp(-damping * time)
        angle = (self.starting_angle * decay) * math.cos(angular_velocity * time)
        return angle


pendulumOne = Pendulum(pivot=(640, 360), mass=3, length=200, width=3, colour="Blue")
pg = PygameWrapper()
running = True
T = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pg.screen.fill(pg.SCREEN_COLOUR)

    rotational_angle = pendulumOne.angleCompute(time=T)
    x = pendulumOne.pivot[0] + math.sin(rotational_angle) * pendulumOne.length
    y = pendulumOne.pivot[1] + math.cos(rotational_angle) * pendulumOne.length
    endPos = (x, y)

    pg.lineDraw(colour=pendulumOne.colour, start_pos=pendulumOne.pivot, end_pos=endPos, width=pendulumOne.width)
    pg.circleDraw(colour="Black", centre=endPos, radius=5)

    T += 0.1

    pg.refresh()

pygame.quit()