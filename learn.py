import numpy as np
import torch
from game import Game2048
from models import Player
import time


def main():
    env = Game2048()
    policy = Player()
    target = Player().load_state_dict(policy.state_dict())
    env.show()
    invalid_action_count = 0
    train(env, policy, target)


def train(env, policy, target):
    actions = {
        0: 'up', 1: 'down', 2: 'left', 3: 'right'
    }
    epsilon_start = 1.0
    epsilon_end = 0.001
    epsilon_decay_steps = 5000
    total_steps = 0 
    discount = 0.9
    epsilon = max(epsilon_end, 
                  epsilon_start - (epsilon_start - epsilon_end) * 
                  (total_steps / epsilon_decay_steps))
    lr = 0.0001
    optimizer = torch.optim.Adam(policy.parameters(), lr=lr)

    while True:

        time.sleep(0.9)
        q_values = policy(env.tensor())
        action = actions[int(torch.argmax(q_values, dim=0))]
        
        # Handle actions
        new_state, reward, status = env.step(action)
        import code; code.interact(local=locals())

    return


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")

