
import random as rand

class Critic:

    def __init__(self,learning_rate,discount_factor,decay_rate,board_size=0):
        self.e = {}
        self.v = {}
        self.td_error = None
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.decay_rate = decay_rate

        for key in self.v.keys():
            self.v[key] = rand.random()

    def reset_eligibilites(self):
        for key in self.e.keys():
            self.e[key] = 0
    
    def set_e(self, key, value):
        self.e[key] = value

    def get_e(self,key):
        if not key in self.e:
            self.e[key] = 0
        return self.e[key]

    def update_td_error(self,reward,new_state,state):
        self.td_error = reward + self.discount_factor * self.get_v(new_state) - self.get_v(state)
   
    def get_v(self,state):
        if not state in self.v:
            self.v[state] = rand.random()/10
        return self.v[state]
    
    def update_v(self,state):
        self.v[state] = self.get_v(state) + self.learning_rate * self.td_error * self.e[state]

    

    #CALCULATES TD ERROR
    #TD-error is then used to update V[S_t]
    #And sent to the actor to update the policy (T)

