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
        self.actions = np.array([0 for _ in range(self.amount_action_space)])


    def action(self, dict_input):
        State = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(State)
        action = random.choice(list_action)
        self.actions[action] += 1
        winning = self.check_victory(State)
        if winning != -1:
            try:
                value = np.load(path+"value.npy")
            except:
                value = np.array([0 for _ in range(self.amount_action_space)])
            try:
                times = np.load(path+"times.npy")
            except:
                times = np.array([0 for _ in range(self.amount_action_space)])
            value += self.actions * winning
            times += self.actions
            with open(path+'value.npy', 'wb') as f:
                np.save(f, value)
            with open(path+'times.npy', 'wb') as f:
                np.save(f, times)
        return action