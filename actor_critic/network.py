import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Network(nn.Module):
    def __init__(self,input_size,hidden_layers_dim=[]):
        super(Network, self).__init__()
        #self.fc1 = nn.Linear(input_size,6)
        #self.fc2 = nn.Linear(6,6)
        #self.fc3 = nn.Linear(6,1)

        self.layers = nn.ModuleList()

        current_dim = input_size

        for hdim in hidden_layers_dim:
            self.layers.append(nn.Linear(current_dim,hdim))
            current_dim = hdim

        self.layers.append(nn.Linear(current_dim, 1))



    
    def forward(self, tensor):
        # (1) input layer
        t = tensor

        # (2) Hidden layers
        for layer in self.layers[:-1]:
            t = F.relu(layer(t))
        
        # (3) Output layer
        out = torch.tanh(self.layers[-1](t))
        return out