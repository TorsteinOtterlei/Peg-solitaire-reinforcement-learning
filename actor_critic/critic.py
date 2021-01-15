
import random as rand

class Critic:

    def __init__(self,learning_rate,discount_factor,decay_rate):
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


    def get_v(self,state):
        if not state in self.v:
            self.v[state] = rand.random()/10
        return self.v[state]

    #CALCULATES TD ERROR
    #TD-error is then used to update V[S_t]
    #And sent to the actor to update the policy (T)

