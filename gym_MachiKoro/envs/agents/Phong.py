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
        # print(dict_input['Phase'])
        a_s = self.action_space(dict_input)
        print('****************************************************************************************')
        # print('card đã mua', self.support_cards)
        print('Số tiền đang có:', self.coins)
        print('action_space', a_s)
        # print('important card', self.important_land_cards)
        # my_id = dict_input['Turn_id']
        # print([p.support_cards for p in dict_input['Player']])
        dict_card = {}
        for card in self.support_cards_object:
            dict_card[card] = [self.support_cards_object[card].value_to_activate, self.support_cards_object[card].price, self.support_cards_object[card].income, self.support_cards_object[card].income_from, self.support_cards_object[card].income_times, self.support_cards_object[card].card_type_in_effect, self.support_cards[card]]
        # print(dict_card)
        if dict_input['Phase'] == 'Card_shopping':
            print(dict_input['Phase'])
            if len(a_s) > 1:
                if a_s[-2] in self.important_land_cards.keys():
                    return a_s[-2]
                if self.important_land_cards['Train Station'] == 0:
                    print('list_action', a)
                    for card in a_s[-1:0]:
                        if dict_card[card][0][0] > 0 and dict_card[card][0][0] <= 6:
                            return card
                else:
                    for card in a_s[0:-1]:
                        if dict_card[card][0][0] > 1:
                            return card
        elif dict_input['Phase'] == 'Choose number of dice':
            for card in dict_card:
                if dict_card[card][0][0] > 6 and dict_card[card][6]:
                    return 2
            return 1
        elif dict_input['Phase'] == 'Re-roll?':
            return 'No'
        elif dict_input['Phase'] == 'Coin_robbery':
            print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            list_name = [p for p in dict_input['Player']]
            list_coins = [p.coins for p in dict_input['Player']]
            print([p.name for p in dict_input['Player']])
            # for i in range(1, 4):
            #     p_id_with_me = int((my_id + i)%4)
            #     p_id = (my_id + p_id_with_me)%4
            #     print(p_id_with_me, p_id)
            #     if list_coins[p_id] == max(list_coins):
            #         print(p_id, list_name[p_id].name)
            #         return p_id_with_me
            pass
        elif dict_input['Phase'] == 'Exchange':
            # print([p.support_cards for p in dict_input['Player']])
            pass
        # else:
        #     raise ValueError("Arrays must have the same size")
        #     print('hihihihihihiihihihihihihhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        
        
        action = random.choice(a)
        self.check_vtr(dict_input)
        return action


    def check_vtr(self, dict_input):
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(self.name, 'Thắng')
            pass
        elif victory == 0:
            print(self.name, 'Thua')
            pass