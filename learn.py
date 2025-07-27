import torch
import torch.nn.functional as F
from game import Game2048
from models import Player
import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, terminated):
        self.buffer.append((
            torch.tensor(state, dtype=torch.float32).flatten(),
            torch.tensor(action, dtype=torch.long),
            torch.tensor(reward, dtype=torch.float32),
            torch.tensor(next_state, dtype=torch.float32).flatten(),
            torch.tensor(terminated, dtype=torch.float32)
        ))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, terminated = zip(*batch)
        return (
            torch.stack(state),
            torch.stack(action),
            torch.stack(reward),
            torch.stack(next_state),
            torch.stack(terminated)
        )
    
    def __len__(self):
        return len(self.buffer)

def train(env, policy, target):

    def get_eps():
        return max(epsilon_end, epsilon_start - (epsilon_start - epsilon_end) * (step / epsilon_decay_steps))

    def explore_exploit():
        # explore
        if random.random() < get_eps():
            action = random.choice(list(actions.values())) 
        # exploit
        else:
            with torch.no_grad():
                values = policy(env.tensor())
                action = actions[int(torch.argmax(values, dim=0))]
        
        state, action, reward, next_state, terminated = env.step(action)
        buffer.push(state, action, reward, next_state, terminated)
        return terminated


    def update_weights():
        states, actions, rewards, next_states, terminated = buffer.sample(batch_size)
        values = policy(states) 
        values_taken = values.gather(1, actions.unsqueeze(1)).squeeze()

        with torch.no_grad():
            next_values = target(next_states)
            max_next_values = next_values.max(1)[0]
            targets = rewards + discount * max_next_values * (1 - terminated)
            import code; code.interact(local=locals())

        # Loss and update
        loss = F.mse_loss(values_taken, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        return

    actions = {
        0: 'up', 1: 'down', 2: 'left', 3: 'right'
    }

    epsilon_start = 1.0
    epsilon_end = 0.001
    epsilon_decay_steps = 5000
    max_episodes = 10000
    step = 0 
    discount = 0.9
    sync_interval = 1000
    lr = 0.0001
    optimizer = torch.optim.Adam(policy.parameters(), lr=lr)
    buffer = ReplayBuffer(capacity=10000)
    batch_size = 32
    max_steps = 100

    for episode in range(max_episodes):
        
        while True:
            terminated = explore_exploit()
            step += 1

            if len(buffer) > batch_size:
                update_weights()

            if terminated == 1 or step >= max_steps:
                env.reset()
                break
    return

def main():
    env = Game2048()
    policy = Player()
    target = Player().load_state_dict(policy.state_dict())
    env.show()
    train(env, policy, target)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")

