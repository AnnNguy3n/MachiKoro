from copy import deepcopy
import random
import gym
import gym_MachiKoro
import time
from collections import Counter

env = gym.make('gym_MachiKoro-v0')

def main():
    env.reset()
    print([p.name for p in env.players])
    env.run_game()

    for i in range(100):
        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break

    for p in env.players:
        p.action(deepcopy(env.dict_input))
    return env.p_name_victory

start = time.time()
print(Counter(main() for i in range(1)))
end = time.time()
print(end - start)