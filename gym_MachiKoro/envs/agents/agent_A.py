from ..base.player import Player
import random
from colorama import Fore, Style


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dict_input):
        action_space = self.action_space(dict_input)
        print(action_space)
        return random.choice(action_space)

    def action_space(self, dict_input: dict):
        if dict_input['Phase'] == 'Choose number of dice':
            return [1,2]

        if dict_input['Phase'] == 'Re-roll?':
            return ['Yes', 'No']
        
        if dict_input['Phase'] == 'Coin_robbery':
            return [i for i in range(dict_input['Player'].__len__()) if dict_input['Player'][i].name != self.name]
        
        if dict_input['Phase'] == 'Card_shopping':
            list_card_name = [name for name in self.support_cards.keys() if self.coins >= self.support_cards_object[name].price
                            and name not in dict_input['Cards_bought'] and dict_input['Board'].support_cards[name] > 0]
            
            list_card_name += [name for name in self.important_land_cards.keys() if self.coins >= self.important_land_cards_object[name].price
                            and self.important_land_cards[name] == 0]

            list_card_name.append('')
            
            return list_card_name
        
        if dict_input['Phase'] == 'Exchange':
            return [('', '', 0)]