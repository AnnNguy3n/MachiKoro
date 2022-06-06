from ..base.player import Player
import random as rd
from colorama import Fore, Style
import json
import os
import numpy as np
path = os.path.dirname(os.path.abspath(__file__)) + "/"
def predict(state,act,model,max_limit,min_limit):
    data = model[act]
    act_formula = []
    for use_data in data:
        try:
            choice = rd.choices(list(use_data.keys()),weights=list(use_data.values()))[0]
        except:
            choice = 0
        act_formula.append(choice)
    new_state = np.array(state,dtype=int) + np.array(act_formula,dtype=int)
    new_state = np.maximum(new_state,min_limit)
    new_state = np.minimum(new_state,max_limit)
    return new_state
    
 
 
 
 
class Agent(Player):
    with open(path + 'data.json', 'r') as f:
        data = json.load(f)
    with open(path + 'model.json', 'r') as f:
        model = json.load(f)
    max_limit = np.load(path+"max_limit.npy")
    min_limit = np.load(path+"min_limit.npy")
    def __init__(self, name):
        super().__init__(name)
        self.states = []
        self.actions = []

    def greedy_state(self,state):
        list_action = self.get_list_index_action(state)
        list_weight = [self.data[act][0] for act in list_action]
        action = list_action[list_weight.index(max(list_weight))]
        new_state = predict(state,action,self.model,self.max_limit,self.min_limit)
        return new_state
    
    def action(self, dict_input):
        State = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(State)
        action = None
           # min_turn = 20
        for act in list_action:
            old_state = predict(State,act,self.model,self.max_limit,self.min_limit)
            if self.check_victory(old_state) == 1:
                action = act
                print("thắng đến nơi rồi")
                break
        #     for turn in range(1,min_turn+1):
        #         new_state = self.greedy_state(old_state)
        #         if self.check_victory(new_state) == 1 and turn <= min_turn:
        #             min_turn = turn
        #             action = act
        #         old_state = new_state.copy()
        # print("dự kiến thắng sau",min_turn,"turn nữa")
        if action == None:
        # action = rd.choice(list_action)
            max_score = 0
            for act in list_action:
                weight = Agent.data[act][0]
                if weight > max_score:
                    max_score = weight
                    action = act
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
                with open(path+'data1.json') as json_file:
                    data1 = json.load(json_file)
            except:
                data1 = [[0,0] for _ in range(self.amount_action_space)]
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
                recent_score = data1[act][0]
                total_played = data1[act][1]
                data1[act][0] = (recent_score * total_played + winning)/(total_played + 1)
                data1[act][1] += 1
            with open(path+'data1.json', 'w') as outfile:
                json.dump(data1, outfile)
            with open(path+'max_limit.npy', 'wb') as f:
                np.save(f, max_limit)
            with open(path+'min_limit.npy', 'wb') as f:
                np.save(f, min_limit)
            with open(path+'model.json', 'w') as f:
                json.dump(model, f)
            self.states = []
            self.actions = []
        return action
