import torch.nn as nn

class Player(nn.Module):
    def __init__(self, in_size=16, out_size=4):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(16, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 4),
            nn.ReLU(),
            nn.Softmax(dim=0),
        )

    def forward(self, x):
        return self.layers(x) 

class PlayerRNN(nn.Module):
    # TODO
    def __init__(self, in_size=16, out_size=4):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(16, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 4),
            nn.ReLU(),
            nn.Softmax(dim=0),
        )

    def forward(self, x):
        output = self.layers(x)
        return output 
