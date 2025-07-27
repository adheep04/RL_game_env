import sys
import tty
import termios
from game import Game2048

def getch():
    """Get a single character from stdin"""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':  # Arrow key escape sequence
            ch += sys.stdin.read(2)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def main():
    game = Game2048()
    
    # Key mappings
    moves = {
        '\x1b[A': 'up',    '\x1b[B': 'down',  
        '\x1b[C': 'right', '\x1b[D': 'left',
        'w': 'up', 's': 'down', 'a': 'left', 'd': 'right',
        0: 'up', 1: 'down', 2: 'left', 3: 'right'
    }
    
    print("2048 - Use arrow keys or WASD to play")
    print("Press 'r' to reset, 'q' to quit")
    game.print_board()
    
    while True:
        key = getch()
        
        # Handle special keys
        if key in ['q', '\x04']:  # q or Ctrl-D
            break
        elif key == '\x03':  # Ctrl-C
            raise KeyboardInterrupt
        elif key == 'r':
            game.reset()
            print("\nGame reset!")
            game.print_board()
            continue
        
        # Handle moves
        if key in moves and not game.is_game_over():
            if game.step(moves[key]):
                game.print_board()
            else:
                print("Invalid move!")
        elif game.is_game_over():
            print("No more moves! Press 'r' to reset or 'q' to quit.")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
    except ImportError:
        print("This game requires Unix-like terminal (Linux/Mac)")
        print("For Windows, use WSL or modify for msvcrt")
