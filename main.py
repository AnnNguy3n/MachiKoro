from copy import deepcopy
import random
import gym
import gym_MachiKoro
import time

env = gym.make('gym_MachiKoro-v0')

def main():
    env.reset()
    print([p.name for p in env.players])
    env.run_game()

    for i in range(1000):
        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break

    for p in env.players:
        p.action(deepcopy(env.dict_input))

start = time.time()
for i in range(1):
    main()
end = time.time()
print(end - start)