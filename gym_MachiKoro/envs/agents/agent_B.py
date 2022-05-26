from ..base.player import Player
import random
from colorama import Fore, Style


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dict_input):
        # print(self.name, end=', ')
        # print([p.name for p in dict_input['Player']])
        # print(dict_input['Turn_id'], 'Turn_id')
        # print(dict_input['Phase'])
        # print(self.action_space(dict_input))
        # print('#################################################################')
        state = self.get_list_state(dict_input)

        list_action = self.get_list_index_action(self.get_list_state(dict_input))

        # print(list_action, 'action có thể làm')
        action = random.choice(list_action)
        print(action, 'action chọn')
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(Fore.LIGHTYELLOW_EX + self.name + ' thắng', end='')
            print(Style.RESET_ALL)
            pass
        elif victory == 0:
            print(Fore.LIGHTYELLOW_EX + self.name + ' thua', end='')
            print(Style.RESET_ALL)
            pass
        elif victory == -1:
            # print(Fore.LIGHTYELLOW_EX + 'Chưa hết game', end='')
            # print(Style.RESET_ALL)
            pass

        # print(state)

        return action