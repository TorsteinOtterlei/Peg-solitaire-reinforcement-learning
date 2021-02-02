import random as rand
import numpy as np
import json

import torch
import torch.nn as nn
from actor_critic.network import Network
import torch.optim as optim

class Critic_neural:

    #Tar inn state, action, reward, new_state, new_action for å så kalkulere TD-error og gi denne til Actor

    def __init__(self,learning_rate,discount_factor,decay_rate,board_size=0, hidden_layers_dim=[]):
        self.e = {}
        self.v = {}
        self.td_error = None
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.decay_rate = decay_rate

        board_size = (board_size)**2
        self.net = Network(input_size=board_size, hidden_layers_dim=hidden_layers_dim)

        self.optimizer = optim.SGD(self.net.parameters(), lr=self.learning_rate)

        self.criterion = nn.MSELoss()

        for key in self.v.keys():
            self.v[key] = rand.random()

    def reset_eligibilites(self):
        for key in self.e.keys():
            self.e[key] = 0

    def set_e(self, key, value):
        pass

    def get_e(self,key):
        if not key in self.e:
            self.e[key] = 0
        return self.e[key]


    def update_td_error(self,reward,new_state,state):
        self.td_error = reward + self.discount_factor * self.get_v(new_state) - self.get_v(state)
  
    def get_v(self,state):
        #print(self.net(torch.tensor([int(s) for s in state], dtype=torch.float32)).item())
        return self.net(torch.tensor([int(s) for s in state], dtype=torch.float32)).item()
        #return 0.0
    
    def update_v(self,state):
        #self.v[state] = self.get_v(state) + self.learning_rate * self.td_error  * self.e[state]

        #T = torch.tensor([self.td_error + self.get_v(state)])

        input_tensor = torch.tensor([int(s) for s in state], dtype=torch.float32)
        
        self.optimizer.zero_grad()

        output = self.net(input_tensor)

        td_error = self.td_error
        if td_error == 0:
            td_error = 1.0E-10
        
        loss = self.criterion(output + td_error, output)

        loss.backward()

        #UPDATE WEIGHTS:
        for num, f in enumerate(self.net.parameters()):
            self.e[num] = self.get_e(num) + f.grad * ((2 * float(td_error)) ** (-1))
            f.grad = float(td_error) * self.e[num]
            self.e[num] = self.discount_factor * self.decay_rate * self.e[num]
    

        self.optimizer.step()

        #print(self.net.fc1.weight.data)
    

    #CALCULATES TD ERROR
    #TD-error is then used to update V[S_t]
    #And sent to the actor to update the policy (T)

#T = V(s) = r + learning_rate*V(s')
#T-V(s) er td_error
#T = td_error + V(S)


#learning_rate = 0.01
#td_error = 0.1
#e = 0
#v = 0.1

#torch.set_grad_enabled(False)
#torch.manual_seed(0)
#input_tensor = torch.tensor([1,0,1,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1,0], dtype=torch.float32)
#
#net = Network()
#output = net(input_tensor)
#
#
#target = torch.tensor([td_error + v])
#criterion = nn.MSELoss()
#loss = criterion(output, target)
#
#net.zero_grad()     # zeroes the gradient buffers of all parameters
#
#print('conv1.bias.grad before backward')
#print(net.fc1.bias.grad)
##
#loss.backward()
##
#print('conv1.bias.grad after backward')
#print(net.fc1.bias.grad)
#
#
#print("____________________")
#
#print(output)
#UPDATE WEIGHTS:
#for f in net.parameters():
#    #f.data.sub_(f.grad.data * learning_rate)
#    e = 1
#    f.data.add_(f.grad.data + learning_rate*td_error*e)
#    print(f.grad)
