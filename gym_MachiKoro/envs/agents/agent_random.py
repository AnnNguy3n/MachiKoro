from ..base.player import Player
import random
import math
import json
import numpy as np
from colorama import Fore, Style
PATH = 'gym_MachiKoro/'
class Agent(Player):
    def __init__(self, name):
        self.state_new = []
        self.action_new = []
        super().__init__(name)

    def action(self,  dict_input):
        t = self.get_list_state(dict_input)
        a = self.get_list_index_action(t)
        action = random.choice(a)
        self.state_new.append(t)
        self.action_new.append(action)
        # print(self.state_new, self.action_new)
        if self.check_victory(t) == 1:
            print(self.name, 'thắng')
            self.save_json(self.state_new, self.action_new)
        elif self.check_victory(t) == 0:
            print(self.name, 'Thua')
            self.save_json(self.state_new, self.action_new)
        return action
    
    def save_json(self, state_new, action_new):
        try:
            s_a = json.load(open('gym_TLMN/envs/agents/S_A.json'))
        except:
            s_a = {} 
        for id in range(len(state_new) - 1):
            t = state_new[id]
            t_n = state_new[id+1]
            for id_s in range(len(t)):
                if f'{id_s}_{t[id_s]}' in s_a:
                    if action_new[id] in s_a[f'{id_s}_{t[id_s]}']:
                        if t_n[id_s] in s_a[f'{id_s}_{t[id_s]}'][action_new[id]]:
                            s_a[f'{id_s}_{t[id_s]}'][action_new[id]][t_n[id_s]] += 1
                        else:
                            s_a[f'{id_s}_{t[id_s]}'][action_new[id]][t_n[id_s]] = 1
                    else:
                        s_a[f'{id_s}_{t[id_s]}'][action_new[id]] = {t_n[id_s]:1}
                else:
                    s_a[f'{id_s}_{t[id_s]}'] = {action_new[id]:{t_n[id_s]:1}}
        with open(f'{PATH}envs/agents/S_A.json', 'w') as f:
            json.dump(s_a, f)
            