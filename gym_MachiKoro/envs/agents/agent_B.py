from ..base.player import Player
import random
from colorama import Fore, Style


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dict_input):
        # action_space = self.action_space(dict_input['Turn_player_cards'], dict_input['Board'].turn_cards, dict_input['Board'].turn_cards_owner)
        # list_action = []
        # for key in action_space.keys():
        #     list_action += action_space[key]

        state = self.get_list_state(dict_input)


        list_action = self.get_list_index_action(self.get_list_state(dict_input))

        print(list_action, 'action có thể làm')
        action = random.choice(list_action)
        print(action, 'action chọn')
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(Fore.LIGHTYELLOW_EX + self.name + ' thắng', end='')
            pass
        elif victory == 0:
            print(Fore.LIGHTYELLOW_EX + self.name + ' thua', end='')
            pass
        elif victory == -1:
            print(Fore.LIGHTYELLOW_EX + 'Chưa hết game', end='')
            pass
        
        print(Style.RESET_ALL)

        return action