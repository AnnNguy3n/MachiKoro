from ..base.player import Player
import random
from colorama import Fore, Style
import json
path = "/content/MachiKoro/gym_MachiKoro/envs/agents/"

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
        self.states = []
        self.actions = []
        with open(path+'data.json') as json_file:
            self.data = json.load(json_file)

    def action(self, dict_input):
        State = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(State)
        action = random.choice(list_action)
        weight = [self.data[act][0] for act in list_action]
        action = list_action[weight.index(max(weight))]
        return action