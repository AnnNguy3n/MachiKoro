from gym_MachiKoro.envs.agents import Phong3 as p1
from gym_MachiKoro.envs.agents import agent_C as p2
from gym_MachiKoro.envs.agents import agent_H as p3
from gym_MachiKoro.envs.agents import random as p4

# from gym_MachiKoro.envs.agents import Phong as p1
# from gym_MachiKoro.envs.agents import Phong as p2
# from gym_MachiKoro.envs.agents import Phong as p3
# from gym_MachiKoro.envs.agents import Phong as p4

agent1 = p1.Agent('Phong')
agent2 = p2.Agent('NA')
agent3 = p3.Agent('Nam')
agent4 = p4.Agent('Bắc')

list_player = [agent1, agent2, agent3, agent4]