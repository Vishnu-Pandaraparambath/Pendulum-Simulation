import torch
import torch.nn as nn
import random
import math
from collections import deque


EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.995
GAMMA = 0.99  # Discount factor for future rewards
BATCH_SIZE = 128
LR = 0.001

epsilon = EPSILON_START

def select_action(state, brain, output_size=33):
    global epsilon

    if random.random() < epsilon:
        return random.randint(0, output_size - 1)

    else:
        with torch.no_grad():
            device = next(brain.parameters()).device
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
            q_values = brain(state_tensor)
            return torch.argmax(q_values).item()


def optimize_model(memory, policy_net, target_net, optimizer):
    if len(memory) < BATCH_SIZE:
        return

    device = next(policy_net.parameters()).device

    transitions = memory.sample(BATCH_SIZE)

    batch = list(zip(*transitions))

    state_batch = torch.tensor(batch[0], dtype=torch.float32).to(device)
    action_batch = torch.tensor(batch[1], dtype=torch.int64).unsqueeze(1).to(device)
    reward_batch = torch.tensor(batch[2], dtype=torch.float32).to(device)

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not True, batch[4])), dtype=torch.bool).to(device)
    non_final_next_states = torch.tensor([s for s, done in zip(batch[3], batch[4]) if done is not True],
                                         dtype=torch.float32).to(device)

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]

    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()

    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)

    optimizer.step()


class BalancingAI(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()

        self.register_buffer(
            "scale_factors",
            torch.tensor([math.pi * 2, 20.0, 1280.0, 1500.0], dtype=torch.float32)
        )

        self.network = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )

    def forward(self, state):
        normalized_state = state / self.scale_factors
        return self.network(normalized_state)


class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)