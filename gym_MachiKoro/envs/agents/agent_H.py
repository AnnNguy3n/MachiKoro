import imp
from platform import libc_ver
from ..base.player import Player
import random
from colorama import Fore, Style
import itertools
import numpy as np

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dict_input):
        action_space = self.action_space(dict_input)
        action = random.choice(action_space)
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


        if dict_input['Phase'] == 'Choose number of dice':
            #chọn số xúc sắc muốn dùng để đổ
            # print("TOANG NÀY", self.coins)
            action = self.get_expected_reward(dict_input)
            # return self.get_expected_reward(dict_input)
        elif dict_input['Phase'] == 'Re-roll?':
            #cân nhắc có nên đổ lại xúc sắc hay k
            #define là ko đổ lại
            action = self.get_expected_reward(dict_input, method= 'Reroll')
            # return action
        elif dict_input['Phase'] == 'Exchange':
            #cân nhắc có đổi thẻ với ai hay ko, măc định là ko đổi
            print(action_space)
            action = ('','',0)
            # return action
        elif dict_input['Phase'] == 'Coin_robbery':
            #cân nhắc xem cướp tiền của ai, mặc định cướp người liền sau
            print('nguoi bi cuop', self.get_player_to_robbery(dict_input))
            action = self.get_player_to_robbery(dict_input) 
            print('cuop', action)
            # return action
        else:
            # print(action_space)
            #cân nhắc xem mua thẻ nào, mặc định là ko mua thẻ
            # if self.decide_buy_card(dict_input) == 0:
            #     print('mua random', action)
            #     return action
            # else:
            #     action = self.decide_buy_card(dict_input)
            #     print('check này', self.coins, action)
            #     return action
            action = self.decide_buy_card(dict_input)  
            # return self.decide_buy_card(dict_input)  
        print('check này Hiếu', dict_input['Phase'],'action: ',  action, self.coins)  
        return action

    def decide_buy_card(self, dict_input):
        price_card_import = [card.price for card in self.important_land_cards_object.values()]
        name_card_import = [card.name for card in self.important_land_cards_object.values()]
        card_import_open = list(self.important_land_cards.values())
        action_space = self.action_space(dict_input)
        #kiểm tra xem chưa mua thẻ công trình lớn nào
        all_self_coins = self.coins
        list_card_buy = []
        for i in range(len(price_card_import)-1, -1,-1):
            if card_import_open[i] == 1:
                price_card_import[i] = 10000
        #mua được thẻ công trình lớn nào thì mua
        for i in range(len(price_card_import)-1, -1,-1):
            if all_self_coins >= price_card_import[i]:
                list_card_buy.append(name_card_import[i])
                all_self_coins -= price_card_import[i]
            else:
                continue
        #sau khi xem xét mua thẻ công trình lớn
        max_reward = self.get_expected_reward(dict_input, method= 'expected')
        # print('max_reward', max_reward, min(price_card_import), all_self_coins)
        if 8*max_reward >= min(price_card_import):
            if len(list_card_buy) > 0:
                return list_card_buy[0]
            else:
                return ''
        else:
            #xem xét số xúc sắc được đổ
            # if self.important_land_cards['Train Station'] == 1:
            #     #xem xét vs việc đc đổ 2 xúc sắc
            #     x = 1
            # else:
            #     #xem xét với việc chỉ được đổ 1 xúc sắc:
            #     x = 2
            dict_card_support_value = self.get_all_card_support_value(dict_input)
            sort_card_support = sorted(dict_card_support_value.items(), key=lambda item: item[1], reverse= True)
            # print('qua', dict_input['Board'].support_cards)
            for item in sort_card_support:
                if item[0].name == 'Business Complex':
                    continue
                if item[0].price <= all_self_coins and dict_input['Board'].support_cards[item[0].name] > 0 and item[0].name in action_space:
                    list_card_buy.append(item[0].name)
                    break
                else:
                    continue

            if len(list_card_buy) > 0:
                return list_card_buy[0]
            else:
                return ''
        
    def get_all_card_support_value(self, dict_input):
        probability_1 = [1/6]*6
        situation = [1,2,3,4,5,6]
        all_player_coins = self.coins
        all_situation = [sum(item) for item in list(itertools.permutations(situation, 2))+ [(i,i) for i in situation]]
        probability_2 = [0]*11
        for i in range(2, 13):
            probability_2[i-2] = all_situation.count(i)/36
        all_card_support = list(self.support_cards_object.values())
        all_card_support_name = [card.name for card in all_card_support]
        dict_card_support_value = {}
        dict_card_support_val_name = {}
        for card in all_card_support:
            prob1 = 0
            prob2 = 0
            if len(card.value_to_activate) == 1:
                if card.value_to_activate[0] <= 6:
                    prob1 = 1/6
                    if card.value_to_activate[0] > 1:
                        prob2 = probability_2[card.value_to_activate[0] - 2]
            else:
                if max(card.value_to_activate) <= 6:
                    prob1 = 1/6*2
                    if max(card.value_to_activate) > 1:
                        prob2 = probability_2[card.value_to_activate[0]-2] + probability_2[card.value_to_activate[1]-2]
            mean_time_use = 0 
            if card.activated_from == 'You':
                mean_time_use = 1/4
            else: 
                mean_time_use = 1
            card_val = max(prob1, prob2)*card.income*mean_time_use
            dict_card_support_value[card] = card_val
            dict_card_support_val_name[card.name] = card_val
        return dict_card_support_value

    def get_expected_reward(self, dict_input, method= 'Roll'):
        probability_1 = [1/6]*6
        situation = [1,2,3,4,5,6]
        all_situation = [sum(item) for item in list(itertools.permutations(situation, 2))+ [(i,i) for i in situation]]
        probability_2 = [0]*11
        for i in range(2, 13):
            probability_2[i-2] = all_situation.count(i)/36
        number_card_support = list(self.support_cards.values())
        all_card_support = list(self.support_cards_object.values())
        list_reward = [0]*12
        for card in all_card_support:
            mul = number_card_support[all_card_support.index(card)]
            if card.activated_from in ['Anyone', 'You']:
                for idx in range(0,12):
                    if idx + 1 in card.value_to_activate:
                        if card.income_from == 'Each Player':
                            list_reward[idx] += card.income*3*mul
                        else:
                            # print('check', card.income, mul)
                            list_reward[idx] += card.income*mul
            else:
                continue
        
        reward_roll_1 = np.mean(np.array(probability_1)*np.array(list_reward[:6]))
        reward_roll_2 = np.mean(np.array(probability_2)*np.array(list_reward[1:]))
        max_reward = max(reward_roll_1, reward_roll_2)
        value_decide_reroll = 'NO'
        # print("TÍNH TOÁN", reward_roll_1, reward_roll_2)
        if method == 'Roll':
            if reward_roll_2 >= reward_roll_1:
                return 2
            else:
                return 1
        elif method == 'expected':
            return max_reward
        elif method == 'Reroll':
            return value_decide_reroll
      

    def get_player_to_robbery(self, dict_input):
        id_robbery = 0
        players_coin = [player.coins for player in dict_input['Player'][1:]]
        players_value_important_card = [np.sum(np.array(list(player.important_land_cards.values()))*np.array([card.price for card in list(player.important_land_cards_object.values())]))
                                        for player in dict_input['Player'][1:]]
        players_all_property = np.array(players_coin) + np.array(players_value_important_card)
        idx_max_coin = np.argmax(np.array(players_coin))
        idx_max_value_important_card = np.argmax(np.array(players_value_important_card))
        idx_richest = np.argmax(np.array(players_all_property))

        if players_coin[idx_richest] >= 5:
            id_robbery = idx_richest + 1
            return id_robbery
        else:
            id_robbery = idx_max_coin + 1
            return id_robbery
