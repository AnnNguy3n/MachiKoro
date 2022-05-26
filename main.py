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

    for p in env.players:
        turn_id = env.players.index(p)
        env.dict_input['Player'] = [p]
        for i in range(1, env.players.__len__()):
            env.dict_input['Player'].append(env.players[(turn_id+i) % env.players.__len__()])

        p.action(deepcopy(env.dict_input))

start = time.time()
for i in range(1):
    main()
    
    # print([p.name for p in env.players])
end = time.time()
print(end - start)