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
        t = self.get_list_state(dict_input)
        a = self.get_list_index_action(t)
        a_s = self.action_space(dict_input)
        dict_card = dict_card_(self.support_cards_object, self.support_cards)
        if dict_input['Phase'] == 'Card_shopping':
            dict_as_price = {}
            for card in a_s:
                if card != '' and card not in self.important_land_cards.keys():
                    if dict_card[card][0][0] >2:
                        dict_as_price[card] = dict_card[card][1]
            dict_as_price = dict(sorted(dict_as_price.items(), key=lambda item: item[1], reverse=True))
            if len(a_s) > 1:
                if a_s[-2] == 'Train Station':
                    return a_s[-2]
                if self.important_land_cards['Train Station'] == 0:
                    for card in a_s:
                        if card in ['Wheat Field', 'Livestock Farm', 'Forest']:
                            return card
                else:
                    for card in dict_as_price: 
                        if card == 'Cheese Factory':
                            if dict_card['Livestock Farm'][6] > 3:
                                return card
                        elif card == 'Furniture Factory':
                            if dict_card['Forest'][6] + dict_card['Mine'][6]> 3:
                                return card
                        elif card == 'Vegetable Market':
                            if dict_card['Wheat Field'][6] +dict_card['Apple Orchard'][6] > 3:
                                return card
                    for card in a_s:
                        if card in ['Livestock Farm', 'Forest', 'Mine', 'Apple Orchard', 'Family Restaurant']:
                            return card
                        # if card in 
                if a_s[-2] in self.important_land_cards.keys():
                    return a_s[-2]
            return 460
        elif dict_input['Phase'] == 'Choose number of dice':
            for card in dict_card:
                if dict_card[card][0][0] > 6 and dict_card[card][6] >0:
                    return 2
            return 1
        else: return random.choice(a)

    
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
