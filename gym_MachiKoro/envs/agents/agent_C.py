from ..base.player import Player
from colorama import Fore, Style
import random as rd
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def action(self, dict_input):
        if dict_input["Phase"] == 'Coin_robbery':
            return rd.choice(self.get_list_index_action(self.get_list_state(dict_input)))
        if self.coins > 9 and self.important_land_cards['Shopping Mall'] == 0:
            return 'Shopping Mall'
        if self.coins > 43:
            return 'Radio Tower'
        if self.important_land_cards['Amusement Park'] == 1:
            return 'Train Station'
        if self.important_land_cards['Radio Tower'] == 1:
            return 'Amusement Park'
        for card in dict_input["Board"].support_cards.keys():
            if card not in dict_input['Cards_bought'] and max(dict_input["Board"].support_cards_object[card].value_to_activate) < 7 and dict_input["Board"].support_cards_object[card].price <= self.coins and dict_input["Board"].support_cards[card] > 0 and card != "Cafe" and card != 'Business Complex':
                return card