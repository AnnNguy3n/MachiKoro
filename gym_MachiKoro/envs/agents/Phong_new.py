from ..base.player import Player
import random
from colorama import Fore, Style
import json
import numpy as np

# #   print(card.card_type)  # đang bị lỗi
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def action(self, dict_input):
        t = self.get_list_state(dict_input)
        a = self.get_list_index_action(t)
        a_s = self.action_space(dict_input)
        dict_card = dict_card_(self.support_cards_object, self.support_cards)
        # print(self.important_land_cards)
        if dict_input['Phase'] == 'Card_shopping':
            if  self.important_land_cards['Train Station'] == 0:
                if dict_card['Family Restaurant'][6] >2:
                    if 'Train Station' in a_s:
                        return 'Train Station'
            for card_name in ['Bakery','Shopping Mall', 'Convenience Store', 'Cafe', 'Family Restaurant', 'Livestock Farm']:
                if card_name in a_s:
                    return card_name
            if self.important_land_cards['Train Station'] == 0:
                if self.coins >= 42:return 'Train Station'
            else:
                if self.coins >= 38:return 'Radio Tower'
                if self.important_land_cards['Radio Tower'] == 1:
                    if self.coins >= 16:return 'Amusement Park'
            if self.important_land_cards['Shopping Mall'] == 1:
                for card_name in card_name[-1:0]:
                    if max(dict_card[card_name][0]) < 6:
                        if card_name in a_s:
                            return  card_name
                if self.important_land_cards['Train Station'] == 1:
                    for card_name in ['Apple Orchard', 'Mine']:
                        if card_name in a_s:
                            return card_name
        if dict_input['Phase'] == 'Choose number of dice':
            if dict_card['Family Restaurant'][6] >=2:
                return 2
            else: return 1
        return ''
            
def dict_card_(support_cards_object, support_cards):
    dict_card = {}
    for card in support_cards_object:
        dict_card[card] = [support_cards_object[card].value_to_activate, 
                            support_cards_object[card].price, 
                            support_cards_object[card].income, 
                            support_cards_object[card].income_from, 
                            support_cards_object[card].income_times, 
                            support_cards_object[card].card_type_in_effect, 
                            support_cards[card], 
                            support_cards_object[card].card_type,
                            support_cards_object[card].activated_from]
    return dict_card