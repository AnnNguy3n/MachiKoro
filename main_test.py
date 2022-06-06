from copy import deepcopy
import random
import gym
import gym_MachiKoro
import time
from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

env = gym.make('gym_MachiKoro-v0')

def main():
    env.reset()
    env.run_game()

    for i in range(500):
        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break

    for p in env.players:
        turn_id = env.players.index(p)
        env.dict_input['Player'] = [p]
        for i in range(1, env.players.__len__()):
            env.dict_input['Player'].append(env.players[(turn_id+i) % env.players.__len__()])
        
        env.dict_input['Value_of_dice'] = 0

        p.action(deepcopy(env.dict_input))

    return env.p_name_victory


for van in range(1):
    with suppress_stdout():
        name = main()
    print(name)