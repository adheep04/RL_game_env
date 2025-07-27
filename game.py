import numpy as np
import random
import torch
import os 

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.game_over = False
        self.reset()
    
    def reset(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.old = np.zeros((self.size, self.size), dtype=int)
        self.score = 0
        self._spawn_tile()
        self._spawn_tile()

    def state_tensor(self):
        return torch.tensor(self.board).flatten().to(dtype=torch.float32)
    
    def _spawn_tile(self):
        empty = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i,j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i,j] = 2 if random.random() < 0.9 else 4
    
    def _compress(self, row):
        # Move non-zeros to the left
        nums = [n for n in row if n > 0]
        merged = []
        i = 0
        score_change = 
        # merge adjacents
        while i < len(nums): 
            if i + 1 < len(nums) and nums[i] == nums[i + 1]:
                merged.append(nums[i] * 2)
                self.score += nums[i] * 2
                i += 2
            else:
                merged.append(nums[i])
                i += 1
        # return new row
        return merged + [0] * (self.size - len(merged))

    def _move(self, direction):
        self.old = self.board.copy()
        old_score = self.score.copy()

        if direction == 'left':
            self.board = np.array([self._compress(row) for row in self.board])
        elif direction == 'right':
            self.board = np.array([self._compress(row[::-1])[::-1] for row in self.board])
        elif direction == 'up':
            self.board = np.array([self._compress(col) for col in self.board.T]).T
        elif direction == 'down':
            self.board = np.array([self._compress(col[::-1])[::-1] for col in self.board.T]).T

        return (not np.array_equal(self.old, self.board), self.score - old_score)

    def step(self, action):
        valid_move, score_change = self._move(action)
        self.update_game_over()
        if valid_move:
            self._spawn_tile()
        return self.board, self.reward(score_change), self.game_status()

    def game_status(self):
        self.update_game_over()
        if 2048 in self.board:
            return 1 # win condition
        elif self.game_over:
            return -1 # loss
        else:
            return 0

    def update_game_over(self, end_game=False):
        if not end_game:
            if 0 in self.board:
                self.game_over = False
                return self.game_over
            for i in range(self.size):
                for j in range(self.size):
                    val = self.board[i,j]
                    if (j < self.size-1 and self.board[i,j+1] == val) or \
                    (i < self.size-1 and self.board[i+1,j] == val):
                        self.game_over = False
                        return 
        self.game_over = True

    def reward(self, score_change):
        return

    def print_board(self):
        os.system('clear')
        print(f"Score: {self.score}")
        print("=" * 30)
        print(self.board.astype(float))
        if 2048 in self.board:
            print("You reached 2048!")
        if self.game_over:
            print("Game Over!")
