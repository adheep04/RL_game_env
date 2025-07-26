import numpy as np
import torch
from game import Game2048
from models import Player
import time


def main():
    game = Game2048()
    player = Player()
    moves = {
        0: 'up', 1: 'down', 2: 'left', 3: 'right'
    }
    game.print_board()
    invalid_move_count = 0
    while True:
        time.sleep(0.9)
        move = player(game.state_tensor())
        move = int(torch.argmax(move, dim=0))
        
        # Handle moves
        if move in moves and not (game.game_over or invalid_move_count > 3):
            if game.move(moves[move]):
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
    except ImportError:
        print("This game requires Unix-like terminal (Linux/Mac)")
        print("For Windows, use WSL or modify for msvcrt")
