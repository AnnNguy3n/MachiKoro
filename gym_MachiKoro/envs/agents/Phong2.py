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
                            if dict_card[card][6] < 3:
                                return card
                else:
                    for card in a_s:
                        if card != '' and card not in self.important_land_cards.keys():
                            if dict_card[card][6] < 3:
                                if card == 'Cheese Factory':
                                    if dict_card['Livestock Farm'][6] >= 3:return card
                                elif card == 'Furniture Factory':
                                    if dict_card['Forest'][6] + dict_card['Mine'][6]>= 3:return card
                                elif card == 'Vegetable Market':
                                    if dict_card['Wheat Field'][6] +dict_card['Apple Orchard'][6] >= 3:return card
                    for card in a_s:
                        if card != '' and card not in self.important_land_cards.keys():
                            if dict_card[card][6] < 3:
                                if card in ['Livestock Farm', 'Forest', 'Mine', 'Apple Orchard', 'Family Restaurant']:return card
                if a_s[-2] in self.important_land_cards.keys():
                    return a_s[-2]
                for card in a_s:
                    if card in ['TV Station', 'Business Complex', 'Stadium']:return card
            return 460
        elif dict_input['Phase'] == 'Coin_robbery':
            # print('action_space', a_s)
            print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            list_name = [p for p in dict_input['Player']]
            list_coins = [p.coins for p in dict_input['Player']]
            list_coins[0] = -1
            print([p.name for p in dict_input['Player']])
            for i in range(len(list_name)):
                if list_coins[i] == max(list_coins):
                    print(i, list_name[i].name)
                    return i
        elif dict_input['Phase'] == 'Exchange':
            # print(dict_input['Remaining_exchange_times'])
            print('hahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            min_price = min([dict_card[card][1] for card in dict_card if (dict_card[card][6] > 0) and (card not in ['Stadium','TV Station', 'Business Complex'])])
            for card in dict_card:
                if dict_card[card][1] == min_price and (card not in ['Stadium','TV Station', 'Business Complex']) and (dict_card[card][6] > 0):
                    str_card_give = card
                    break
            list_name = [p for p in dict_input['Player']]
            max_price = 0
            for i in range(1,4):
                dict_card_p = dict_card_(list_name[i].support_cards_object, list_name[i].support_cards)
                # print(dict_card_p)
                max_price_card_p = max([dict_card_p[card][1] for card in dict_card_p if (dict_card_p[card][6] > 0) and (card not in ['Stadium','TV Station', 'Business Complex'])])
                if max_price < max_price_card_p:
                    max_price = max_price_card_p
            for i in range(1,4):
                dict_card_p = dict_card_(list_name[i].support_cards_object, list_name[i].support_cards)
                for card in dict_card_p:
                    if (dict_card_p[card][1] == max_price) and (card not in ['Stadium','TV Station', 'Business Complex']) and (dict_card_p[card][6] > 0):
                        str_card_rei = card
                        id_p = i
                        break
            print((str_card_give, str_card_rei, id_p, list_name[id_p].name))
            return (str_card_give, str_card_rei, id_p)
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
