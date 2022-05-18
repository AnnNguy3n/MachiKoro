from copy import deepcopy
import random
import gym
import gym_MachiKoro


def main():
    env = gym.make('gym_MachiKoro-v0')
    env.reset()

    for i in range(1000):
        print(i, 'iiiii')
        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break

        if i % 100 == 99:
            input()

main()