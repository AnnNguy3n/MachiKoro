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


    def action(self, dict_input):
        State = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(State)
        action = random.choice(list_action)
        pair = [State,action]
        self.states.append(State)
        self.actions.append(action)
        winning = self.check_victory(State)
        if winning != -1:
            try:
                with open(path+'data.json') as json_file:
                    data = json.load(json_file)
            except:
                data = [[0,0] for _ in range(self.amount_action_space)]
            for act in self.actions:
                recent_score = data[act][0]
                total_played = data[act][1]
                data[act][0] = (recent_score * total_played + winning)/(total_played + 1)
                data[act][1] += 1
            with open(path+'data.json', 'w') as outfile:
                json.dump(data, outfile)
        return action