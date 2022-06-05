import random
from ..base.player import Player

class Agent(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.history = []
    
    def action(self, dict_input):
        list_action = self.get_list_index_action(self.get_list_state(dict_input))
        # print(self.history.__len__())
        # self.history.append(self.history.__len__())
        return random.choice(list_action)