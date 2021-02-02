




import gym

#env = gym.make('CartPole-v0')
env = gym.make('gym_peg_solitare:diamond-v0')
env.reset()
#for _ in range(1000):
#    env.render()
#    env.step(env.action_space.sample()) # take a random action
#env.close()




if __name__ == "__main__":
    main()