from ..base.player import Player
import random
from colorama import Fore, Style
import json
import numpy as np

# print(card.card_type)  # đang bị lỗi
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def action(self, dict_input):
        dict_card = {}
        for card in dict_input['Turn_player_cards']:
            dict_card[card] = card.score

        dict_card = dict(sorted(dict_card.items(), key = lambda item:item[1]))
        for i in dict_card:
            print(i.name, dict_card[i], 'stt :', i.stt)

        action_space = self.action_space(dict_input['Turn_player_cards'], dict_input['Board'].turn_cards, dict_input['Board'].turn_cards_owner)
        print(action_space)
        self.check_vtr(dict_input)
        state = dict_input
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        action = random.choice(a)
        return action

    def check_vtr(self, dict_input):
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(self.name, 'Thắng')
            pass
        elif victory == 0:
            print(self.name, 'Thua')
            pass