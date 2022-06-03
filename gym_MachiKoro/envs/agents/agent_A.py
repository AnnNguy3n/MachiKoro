from ..base.player import Player
import random
from colorama import Fore, Style
import json
import os
import numpy as np
path = os.path.dirname(os.path.abspath(__file__)) + "/"


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
        self.states = []
        self.actions = []


    def action(self, dict_input):
        State = self.get_list_state(dict_input)
        print(State)
        list_action = self.get_list_index_action(State)
        action = random.choice(list_action)
        pair = [State,action]
        self.states.append(State)
        self.actions.append(action)
        winning = self.check_victory(State)
        if winning != -1:
            try:
                with open(path + "model.json", 'r') as openfile:
                    model = json.load(openfile)
            except:
                model = [[{} for _ in range(len(State))] for _ in range(self.amount_action_space)]
            try:
                with open(path+'data.json') as json_file:
                    data = json.load(json_file)
            except:
                data = [[0,0] for _ in range(self.amount_action_space)]
            try:
                max_limit = np.load(path+"max_limit.npy")
            except:
                max_limit = [0 for _ in range(len(State))]
            try:
                min_limit = np.load(path+"min_limit.npy")
            except:
                min_limit = [99999 for _ in range(len(State))]

            for id_pair in range(len(self.states)):
                old_state = self.states[id_pair]
                old_action = self.actions[id_pair]
                if id_pair != len(self.states) -1:
                    new_state = self.states[id_pair+1]
                else:
                    new_state = State
                act_formula = np.array(new_state) - np.array(old_state)
                for id_state in range(len(act_formula)):
                    data_a = int(act_formula[id_state])
                    # print(old_action,id_state)
                    if data_a not in model[old_action][id_state].keys():
                        model[old_action][id_state][data_a] = 1
                    else:
                        model[old_action][id_state][data_a] += 1
            for state in self.states:
                max_limit = np.maximum(max_limit,state)
                min_limit = np.minimum(min_limit,state)
            max_limit = np.maximum(max_limit,State)
            min_limit = np.minimum(min_limit,State)
            for act in self.actions:
                recent_score = data[act][0]
                total_played = data[act][1]
                data[act][0] = (recent_score * total_played + winning)/(total_played + 1)
                data[act][1] += 1
            with open(path+'data.json', 'w') as outfile:
                json.dump(data, outfile)
            with open(path+'max_limit.npy', 'wb') as f:
                np.save(f, max_limit)
            with open(path+'min_limit.npy', 'wb') as f:
                np.save(f, min_limit)
            with open(path+'model.json', 'w') as f:
                json.dump(model, f)
        return action