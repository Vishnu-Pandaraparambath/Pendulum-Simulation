import pygame

import torch.optim as optim
import NN

from pendulumLib import Pendulum
from NN import BalancingAI, ReplayMemory, select_action, optimize_model

INPUT_SIZE = 4
OUTPUT_SIZE = 33
NUM_EPISODES = 500
FPS = 60
dt = 1.0 / FPS

TARGET_UPDATE = 1000
pendulum_one = Pendulum(
    pivot=(640, 360), mass=5, length=150, width=10,
    colour=(0, 100, 0), starting_angle=175, damping=0.01, gravity=9.81
)

pendulum_one.SHMSimulation()

def main():
    pygame.init()
    clock = pygame.time.Clock()

    pendulum_one = Pendulum(
        pivot=(640, 360), mass=5, length=150, width=10,
        colour=(0, 100, 0), starting_angle=175, damping=0.01, gravity=9.81
    )

    brain = BalancingAI(input_size=INPUT_SIZE, output_size=OUTPUT_SIZE)
    target_brain = BalancingAI(input_size=INPUT_SIZE, output_size=OUTPUT_SIZE)

    target_brain.load_state_dict(brain.state_dict())
    target_brain.eval()

    memory = ReplayMemory(capacity=10000)
    optimizer = optim.Adam(brain.parameters(), lr=0.001)

    print("Starting Training Loop with Target Network...")

    total_steps = 0
    max_frames_survived = 0

    try:
        for episode in range(NUM_EPISODES):
            state = pendulum_one.reset()
            total_reward = 0
            done = False
            total_frames = 0

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                action = select_action(state, brain, OUTPUT_SIZE)
                next_state, reward, done = pendulum_one.step(action, dt)

                memory.push(state, action, reward, next_state, done)

                optimize_model(memory, brain, target_brain, optimizer)

                state = next_state
                total_reward += reward
                total_steps += 1

                if total_steps % TARGET_UPDATE == 0:
                    target_brain.load_state_dict(brain.state_dict())

                pendulum_one.render()

                clock.tick(0)

                total_frames = total_reward

                max_frames_survived = max(max_frames_survived, total_frames)

            NN.epsilon = max(NN.EPSILON_END, NN.epsilon * NN.EPSILON_DECAY)
            print(f"Episode {episode + 1} | Reward: {total_reward:6.1f} | Epsilon: {NN.epsilon:.3f}")

    except KeyboardInterrupt:
        print("\nTraining interrupted. Shutting down...")
        print(f"Maximum frames survived: {max_frames_survived:6.1f}")
        pygame.quit()


#if __name__ == '__main__':
 #   main()
