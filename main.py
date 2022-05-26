from copy import deepcopy
import random
import gym
import gym_MachiKoro
import time

env = gym.make('gym_MachiKoro-v0')

def main():
    env.reset()
    env.run_game()

    for i in range(500):
        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break
    
    k = 0
    for p in env.players:
        env.dict_input['Turn_id'] = k
        p.action(deepcopy(env.dict_input))
        k += 1

start = time.time()
for i in range(1):
    main()
    
    print([p.name for p in env.players])
end = time.time()
print(end - start)