from ..base.player import Player
import random
from colorama import Fore, Style


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dict_input):
        return random.choice(self.get_list_index_action(self.get_list_state(dict_input)))