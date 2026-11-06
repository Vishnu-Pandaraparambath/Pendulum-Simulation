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
        self.SHM_gravity = gravity
        self.free_pendulum_gravity = gravity * 100
        self.starting_angle = math.radians(min(starting_angle, 180))
        self.angle = self.starting_angle
        self.angular_velocity = 0.0
        self.pivot_vel_x = 0.0

    def angularAcceleration(self, theta, accel_x):
        alpha = ((-self.free_pendulum_gravity * math.sin(theta)) - (accel_x * math.cos(theta))) / self.length
        return alpha

    def angleCompute(self, time):
        angular_velocity = math.sqrt(self.SHM_gravity / self.length)
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

    ## NN stuff

    def reset(self):
        self.angle = math.radians(165)  # Spawns just 5 degrees off-center from straight up
        self.angular_velocity = 0.0
        self.pivot_vel_x = 0.0
        self.pivotSetter(640, 360)  # Reset to center of screen

        return [self.angle, self.angular_velocity, self.pivot[0], self.pivot_vel_x]

    def render(self):
        pg.screen.fill(pg.SCREEN_COLOUR)

        piv_x, piv_y = self.pivot
        end_x = piv_x + math.sin(self.angle) * self.length
        end_y = piv_y + math.cos(self.angle) * self.length
        end_pos = (end_x, end_y)

        pg.lineDraw(colour=self.colour, start_pos=self.pivot, end_pos=end_pos, linewidth=self.width)
        pg.circleDraw(colour="Black", centre=end_pos, radius=10)

        pg.refresh()


    def step(self, action, dt):
        piv_x, piv_y = self.pivot

        accelerations = [-1500.0 + (i * (3000.0 / 32)) for i in range(33)]

        accel_x = accelerations[action]

        self.pivot_vel_x += accel_x * dt
        self.pivot_vel_x *= 0.90

        piv_x += self.pivot_vel_x * dt
        self.pivotSetter(piv_x, piv_y)

        alpha = self.angularAcceleration(self.angle, accel_x)

        self.angular_velocity += alpha * dt
        self.angular_velocity *= (1 - (self.damping * dt))
        self.angle += self.angular_velocity * dt

        target_angle = math.pi
        angle_difference = abs(self.angle - target_angle)

        reward = 1

        reward /= (1.0 + abs(self.angular_velocity))

        distance_to_center = abs(piv_x - 640.0)
        reward -= (distance_to_center / 1280.0)


        done = False
        failure_threshold = math.radians(35.0)

        if angle_difference > failure_threshold:
            done = True
            reward = -70

        elif piv_x < 0 or piv_x > 1280:
            done = True
            reward = -50.0

        next_state = [self.angle, self.angular_velocity, piv_x, self.pivot_vel_x]

        return next_state, reward, done




