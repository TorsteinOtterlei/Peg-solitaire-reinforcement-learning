import json
import random
import matplotlib.pyplot as plt
from game.triangle import Triangle
from game.diamond import Diamond
from actor_critic.actor import Actor
from actor_critic.critic import Critic

with open('parameters.json') as f:
        parameters = json.load(f)

def open_cell_list_gen(json_list):
    open_cell_list = []
    for val in parameters['open_cells']:
            open_cell_list.append((int(val[1]),int(val[3])))
    return open_cell_list

def main():
    game = None
    game_type = ""
    open_cell_list = open_cell_list_gen(parameters['open_cells'])

    if parameters['board_type'] == "diamond":
        game_type = 'd'
    elif parameters['board_type'] == "triangle":
        game_type = 't'

    learning_rate_actor = parameters['learning_rate_actor']
    learning_rate_critic = parameters['learning_rate_critic']
    discount_factor_actor = parameters['discount_factor_actor']
    discount_factor_critic = parameters['discount_factor_critic']
    decay_rate_actor = parameters['decay_rate_actor']
    decay_rate_critic = parameters['decay_rate_critic']
    init_val_e = parameters['init_val_e']
    e_decay_rate = parameters['e_decay_rate']
    num_episodes = parameters['num_episodes']

    actor = Actor(learning_rate_actor,discount_factor_actor,decay_rate_actor,init_val_e,e_decay_rate)
    critic = Critic(learning_rate_critic,discount_factor_critic,decay_rate_critic)
    
    peg_in_episode_list = []

    for i in range(num_episodes):
        if game_type == 'd':
            game = Diamond(parameters['board_size'], open_cell_list)
        elif game_type == 't':
            game = Triangle(parameters['board_size'], open_cell_list)
        else: raise Exception("Not valid game type")

        actor.reset_eligibilities()                     #Reset eligibilities in actor
        critic.reset_eligibilites()                     #Reset eligibilities in critic
        state_action_list = []

        s = game.state_string
        a = actor.get_action(s,game.get_possible_moves())


        while not game.check_is_win_state() and a:
            game.move_4tup(a)
            r = get_reward(game)
            new_s = game.state_string
            new_a = actor.get_action(new_s,game.get_possible_moves())
            state_action_list.append([s,a])
            actor.e[s,a] = 1
            critic.td_error = r + critic.discount_factor * critic.get_v(new_s) - critic.get_v(s)
            critic.e[s] = 1
            for pair in state_action_list:
                s = pair[0] 
                a = pair[1]
                critic.v[s] = critic.get_v(s) + critic.learning_rate * critic.td_error * critic.e[s]
                critic.e[s] = critic.discount_factor * critic.decay_rate * critic.e[s]
                actor.policy[s,a] = actor.get_policy(s,a) + actor.learning_rate * critic.td_error * actor.e[s,a]
                actor.e[s,a] = actor.discount_factor * actor.decay_rate * actor.e[s,a]
            s = new_s
            a = new_a

            if parameters['display_var'] and i > num_episodes-2:
                game.print(parameters['frame_delay'])

        peg_in_episode_list.append(game.state_string.count('1'))

    #if parameters['display_var']:
            #game.print_diamond()                                 #Prints board with networkx
    plt.clf()
    plt.plot(peg_in_episode_list)
    plt.ylabel('Num pegs')
    plt.show()

def get_reward(game):
    if game.check_is_win_state():
        return 10
    elif not game.get_possible_moves():
        return -10
    else:
        return 0

if __name__ == "__main__":
    main()