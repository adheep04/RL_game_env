import numpy as np
import random
import torch
import os 

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.score = 0
        self.reset()
    
    def reset(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.old = np.zeros((self.size, self.size), dtype=int)
        self._spawn_tile()
        self._spawn_tile()

    def tensor(self):
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
        # store copy of old score
        old_score = self.score

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
        if valid_move:
            self.invalid_moves = 0
            self._spawn_tile()
        else:
            self.invalid_moves += 1
        return self.board, self.reward(score_change), self.status()

    def status(self):
        if 2048 in self.board:
            return 'win' 
        elif self.loss_condition():
            return 'loss'
        else:
            return 'play'

    def loss_condition(self):
        if 0 in self.board:
            return False
        for i in range(self.size):
            for j in range(self.size):
                val = self.board[i,j]
                if (j < self.size-1 and self.board[i,j+1] == val) or \
                    (i < self.size-1 and self.board[i+1,j] == val):
                    return False
        return True

    def reward(self, score_change): 
        status = self.status()
        if status == 'play':
            if not score_change:
                # no merge penalty
                return -0.3
            else:
                # rewarded for merges normalized by 2048
                return float(score_change) / 2048.0 
        elif status == 'loss':
            # loss penalty
            return -1
        else:
            # win reward
            return 1 

    def show(self):
        os.system('clear')
        print(f"Score: {self.score}")

        print("=" * 30)
        for row in self.board: 
            print(row.astype(int), end='\n', flush=True)

        if self.status() == 'win':
            print("You reached 2048!")
        if self.status() == 'loss':
            print("Game Over!")

    def edit(self, coords, value):
        self.board[coords[0]][coords[1]] = value

    def up(self):
        self.step('up')

    def down(self):
        self.step('down')

    def left(self):
        self.step('left')

    def right(self):
        self.step('right')

g = Game2048()
import code; code.interact(local=locals())
