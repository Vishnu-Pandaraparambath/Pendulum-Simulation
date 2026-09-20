import pygame

BORDER_WIDTH = 100

class PygameWrapper:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.FPS = 60
        self.SCREEN_COLOUR = (255,255,255)
        self.clock = pygame.time.Clock()

    def lineDraw(self, colour, start_pos, end_pos, linewidth):
        pygame.draw.line(surface=self.screen, color=colour, start_pos=start_pos, end_pos=end_pos, width=linewidth)

    def circleDraw(self, colour, centre, radius):
        pygame.draw.circle(surface=self.screen, color=colour, center=centre, radius=radius)

    def keyMove(self, pivot_x, vel = 3):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and pivot_x > BORDER_WIDTH:
            pivot_x -= vel

        if keys[pygame.K_RIGHT] and pivot_x < self.width - BORDER_WIDTH:
            pivot_x += vel

        return pivot_x

    def refresh(self):
        pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.FPS)