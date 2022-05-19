from ..base.player import Player
import random
import math
import json
import numpy as np
from colorama import Fore, Style

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  dict_input):
        state = dict_input
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        action = random.choice(a)

        try:
            s_a = json.load(open('S_A.json'))
        except:
            s_a = {} 
        dict_a = {}
        for id_a in a:
            dict_a[f'{id_a}'] = 0

        for id_s in range(len(t)):
            if f'{id_s}_{t[id_s]}' in s_a:
                for id_a in a:
                    if f'{id_a}' in s_a[f'{id_s}_{t[id_s]}']:
                        s_a[f'{id_s}_{t[id_s]}'][f'{id_a}'] += 1
                    else:
                        s_a[f'{id_s}_{t[id_s]}'][f'{id_a}'] = 0
            else:
                s_a[f'{id_s}_{t[id_s]}'] = dict_a

        with open('S_A.json', 'w') as f:
            json.dump(s_a, f)
        # for i in s_a:
        #     print(i, s_a[i])
        if self.check_victory(t) == 1:
            print(self.name, 'thắng')
        elif self.check_victory(t) == 0:
            print(self.name, 'Thua')
        return action
