from game.triangle import Triangle
from game.diamond import Diamond
import random as rand

class Actor:

    def __init__(self,learning_rate,discount_factor,decay_rate,init_val_e,e_decay_rate):
        self.e = {}
        self.policy = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.decay_rate = decay_rate
        self.e_greedy = init_val_e
        self.e_decay_rate = e_decay_rate


    def get_policy(self,state,action):
        if not (state,action) in self.policy:
            self.policy[state,action] = 0
        return self.policy[state,action]


    def reset_eligibilities(self):
        for key in self.e.keys():
            self.e[key] = 0


    def get_action(self,state,possible_actions):
        if not possible_actions:
            return None

        current_best_action = possible_actions[0]                           
        for action in possible_actions:                                                         #Find best action
            if self.get_policy(state,action) > self.get_policy(state,current_best_action):
                current_best_action = action

        randnum = rand.random()                                               #Exploration. An action among the non-best actions is chosen at random
        if randnum < self.e_greedy and len(possible_actions)>1:               #If e_greedy is larger means larger probability of random
            possible_actions_without_best = possible_actions.copy()
            possible_actions_without_best.remove(current_best_action)
            index = rand.randint(0,len(possible_actions_without_best)-1)
            current_best_action = possible_actions_without_best[index]
            self.e_greedy = self.e_greedy * (1 - self.e_decay_rate)
        
        return current_best_action
            
        
        




    #def update(self):
    #    #State,value = Former state,value  +  ALPHA * δ * e(s,a)


    #Actor utilizes the TD-error for its own update


