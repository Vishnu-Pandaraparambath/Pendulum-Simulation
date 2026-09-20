from pgwrapper import PygameWrapper
import math
import pygame

pg = PygameWrapper(screen_width=1280, screen_height=720)
class Pendulum:
    def __init__(self, pivot, mass, length, width, colour, starting_angle, damping, gravity):
        self.mass = mass
        self.length = length
        self.colour = colour
        self.pivot = pivot
        self.width = width
        self.damping = damping
        self.gravity = gravity
        self.starting_angle = math.radians( starting_angle )

    def angleCompute(self, time):
        angular_velocity = math.sqrt(self.gravity / self.length)
        decay = math.exp(-self.damping * time)
        angle = (self.starting_angle * decay) * math.cos(angular_velocity * time)
        return angle

    def pivotSetter(self, x, y):
        self.pivot = (x, y)

    def SHMSimulation(self):
        running = True
        t = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pg.screen.fill(pg.SCREEN_COLOUR)
            piv_x, piv_y = self.pivot
            piv_x = pg.keyMove(piv_x)

            rotational_angle = self.angleCompute(time=t)
            end_x = self.pivot[0] + math.sin(rotational_angle) * self.length
            end_y = self.pivot[1] + math.cos(rotational_angle) * self.length
            end_pos = (end_x, end_y)

            self.pivotSetter(piv_x, piv_y)

            pg.lineDraw(colour=self.colour, start_pos=self.pivot, end_pos=end_pos, linewidth=self.width)
            pg.circleDraw(colour="Black", centre=end_pos, radius=5)

            t += 0.1
            pg.refresh()

        pygame.quit()

    def staticPendulum(self):
        pass


