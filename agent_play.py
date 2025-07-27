import numpy as np
import torch
from game import Game2048
from models import Player
import time


def main():
    game = Game2048()
    player = Player()
    action_map = {
        0: 'up', 1: 'down', 2: 'left', 3: 'right'
    }
    game.print_board()
    invalid_move_count = 0
    while True:
        time.sleep(0.9)
        q_values = player(game.state_tensor())
        action = action_map[int(q_values.argmax())]
        
        # Handle moves
        if not (game.game_over or invalid_move_count > 3):
            if game.step(action):
                game.print_board()
                invalid_move_count = 0
            else:
                invalid_move_count +=1
                print("Invalid move!")
        else:
            game.update_game_over(end_game=True)
            game.print_board()
            return 1


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
