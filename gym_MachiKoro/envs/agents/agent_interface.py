# from gym_MachiKoro.envs.agents import S_a as p1
# from gym_MachiKoro.envs.agents import S_a as p2
# from gym_MachiKoro.envs.agents import S_a as p3
# from gym_MachiKoro.envs.agents import S_a as p4

from gym_MachiKoro.envs.agents import Phong_new as p1
from gym_MachiKoro.envs.agents import random as p2
from gym_MachiKoro.envs.agents import random as p3
from gym_MachiKoro.envs.agents import agent_C as p4

agent1 = p1.Agent('Phong')
agent2 = p2.Agent('Tây')
agent3 = p3.Agent('Nam')
agent4 = p4.Agent('Bắc')

list_player = [agent1, agent2, agent3, agent4]