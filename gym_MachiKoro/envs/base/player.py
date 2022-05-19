from copy import deepcopy
import pandas
import json
import numpy
from gym_MachiKoro.envs.base.card import Support_Card, Important_Land_Card


class Player:
    def __init__(self, name):
        self.__name = name
        self.__full_action = list(json.load(open('gym_MachiKoro/envs/action_space.json')).values())
        self.__amount_action_space = self.__full_action.__len__()
        self.reset()

    def reset(self):
        self.__coins = 0

        data = pandas.read_csv('gym_MachiKoro/envs/base/card.csv', index_col='name')
        temp = ['Wheat Field', 'Livestock Farm', 'Bakery', 'Cafe', 'Convenience Store', 'Forest', 'Stadium', 'TV Station', 'Business Complex',
                'Cheese Factory', 'Furniture Factory', 'Mine', 'Family Restaurant', 'Apple Orchard', 'Vegetable Market']

        self.__support_cards = {}
        for name in temp:
            if name in ['Wheat Field', 'Bakery']:
                self.__support_cards[name] = 1
            else: 
                self.__support_cards[name] = 0

        self.__support_cards_object = {}
        for name in temp:
            try:
                income = int(data['income'][name])
            except:
                income = None

            self.__support_cards_object[name] = Support_Card(data['card_type'][name], name, int(data['price'][name]), data['description'][name],[int(a) for a in data['value_to_activate'][name].split(',')],
                                                            data['activated_from'][name], income, data['income_from'][name], data['income_times'][name], data['card_type_in_effect'][name])

        temp = ['Train Station', 'Shopping Mall', 'Amusement Park', 'Radio Tower']
        self.__important_land_cards = {}
        for name in temp:
            self.__important_land_cards[name] = 0
        
        self.__important_land_cards_object = {}
        for name in temp:
            self.__important_land_cards_object[name] = Important_Land_Card(data['card_type'][name], name, int(data['price'][name]), data['description'][name])

    @property
    def amount_action_space(self):
        return self.__amount_action_space

    @property
    def name(self):
        return self.__name

    @property
    def coins(self):
        return self.__coins
    
    @property
    def support_cards(self):
        return deepcopy(self.__support_cards)

    @property
    def support_cards_object(self):
        return deepcopy(self.__support_cards_object)

    @property
    def important_land_cards(self):
        return deepcopy(self.__important_land_cards)
    
    @property
    def important_land_cards_object(self):
        return deepcopy(self.__important_land_cards_object)
    
    def check_victory(self, state: list):
        my_land = state[0:4]
        p1_land = state[20:24]
        p2_land = state[40:44]
        p3_land = state[60:64]

        temp = [sum(my_land), sum(p1_land), sum(p2_land), sum(p3_land)]
        if max(temp) == 4:
            if temp[0] == 4:
                return 1
            else:
                return 0
        else:
            return -1

    def get_list_index_action(self, state: list):
        phase = state[80]
        if phase == 0:
            return [433]
        elif phase == 1:
            return [434, 435]
        elif phase == 2:
            return [436, 437]
        elif phase == 4:
            return [438, 439, 440]
        elif phase == 5:
            my_coins = state[19]
            list_card_bought = state[98:113]
            list_land_bought = state[0:4]
            list_card_on_board = state[83:98]
            list_index = []

            if my_coins >= 8:
                for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
                    if list_card_bought[i-1] == 0 and list_card_on_board[i-1] != 0:
                        list_index.append(440+i)
            
            elif my_coins >= 7:
                for i in [1,2,3,4,5,6,7,8,10,11,12,13,14,15]:
                    if list_card_bought[i-1] == 0 and list_card_on_board[i-1] != 0:
                        list_index.append(440+i)

            elif my_coins >= 6:
                for i in [1,2,3,4,5,6,7,10,11,12,13,14,15]:
                    if list_card_bought[i-1] == 0 and list_card_on_board[i-1] != 0:
                        list_index.append(440+i)

            elif my_coins >= 5:
                for i in [1,2,3,4,5,6,10,11,13,14,15]:
                    if list_card_bought[i-1] == 0 and list_card_on_board[i-1] != 0:
                        list_index.append(440+i)

            elif my_coins >= 3:
                for i in [1,2,3,4,5,6,11,13,14,15]:
                    if list_card_bought[i-1] == 0 and list_card_on_board[i-1] != 0:
                        list_index.append(440+i)
            
            elif my_coins >= 2:
                for i in [1,2,3,4,5,15]:
                    if list_card_bought[i-1] == 0 and list_card_on_board[i-1] != 0:
                        list_index.append(440+i)
            
            elif my_coins >= 1:
                for i in [1,2,3]:
                    if list_card_bought[i-1] == 0 and list_card_on_board[i-1] != 0:
                        list_index.append(440+i)

            else:
                pass

            if my_coins >= 22:
                for i in [1,2,3,4]:
                    if list_land_bought[i-1] == 0:
                        list_index.append(455+i)
            
            elif my_coins >= 16:
                for i in [1,2,3]:
                    if list_land_bought[i-1] == 0:
                        list_index.append(455+i)

            elif my_coins >= 10:
                for i in [1,2]:
                    if list_land_bought[i-1] == 0:
                        list_index.append(455+i)

            elif my_coins >= 4:
                for i in [1]:
                    if list_land_bought[i-1] == 0:
                        list_index.append(455+i)

            else:
                pass

            list_index.append(460)
            return list_index
        
        elif phase == 3:
            list_exchange_option = []
            temp = ['Wheat Field', 'Livestock Farm', 'Bakery', 'Cafe', 'Convenience Store', 'Forest', 'Stadium', 'TV Station', 'Business Complex',
                'Cheese Factory', 'Furniture Factory', 'Mine', 'Family Restaurant', 'Apple Orchard', 'Vegetable Market']
            
            my_sp_c_ards = state[4:19]
            my_sp_cards = []
            for i in range(15):
                if temp[i] not in ['Stadium', 'TV Station', 'Business Complex'] and my_sp_c_ards[i] != 0:
                    my_sp_cards.append(temp[i])
            
            for i in range(1, 4):
                p_sp_c_ards = state[4+20*i:19+20*i]
                p_sp_cards = []
                for k in range(15):
                    if temp[k] not in ['Stadium', 'TV Station', 'Business Complex'] and p_sp_c_ards[k] != 0:
                        p_sp_cards.append(temp[k])

                for k1 in my_sp_cards:
                    for k2 in p_sp_cards:
                        list_exchange_option.append([k1,k2,i])

            return [self.__full_action.index(action) for action in list_exchange_option]
        
        else:
            return None

    def get_list_state(self, dict_input: dict):
        state_list = []
        list_p_name = [p.name for p in dict_input['Player']]
        my_id = list_p_name.index(self.name)

        # 0 - 19: Các thẻ vùng đất và hỗ trợ của bản thân, tiền
        state_list += list(numpy.array(list(self.important_land_cards.values())))
        state_list += list(numpy.array(list(self.support_cards.values())))
        state_list += [self.coins]
        
        # 20 - 79: Các thẻ vùng đất và hỗ trợ của đối thủ, tiền, theo góc nhìn của bản thân
        for i in range(1, list_p_name.__len__()):
            id_player = (list_p_name.index(self.name) + i) % list_p_name.__len__()
            state_list += list(numpy.array(list(dict_input['Player'][id_player].important_land_cards.values())))
            state_list += list(numpy.array(list(dict_input['Player'][id_player].support_cards.values())))
            state_list += [dict_input['Player'][id_player].coins]

        # 80: Phase
            # 0: Đã hết game, do đó chỉ có thể ngồi xem
            # 1: Choose number of dice
            # 2: Re-roll?
            # 3: Exchange
            # 4: Coin_robbery
            # 5: Card_shopping
        if dict_input['Phase'] == 'End game':
            state_list.append(0)
        elif dict_input['Phase'] == 'Choose number of dice':
            state_list.append(1)
        elif dict_input['Phase'] == 'Re-roll?':
            state_list.append(2)
        elif dict_input['Phase'] == 'Exchange':
            state_list.append(3)
        elif dict_input['Phase'] == 'Coin_robbery':
            state_list.append(4)
        elif dict_input['Phase'] == 'Card_shopping':
            state_list.append(5)
        
        # 81, 82: Số lần đổi thẻ và số lần cướp còn lại
        state_list += [dict_input['Remaining_exchange_times'], dict_input['Remaining_robbery_times']]

        # 83-97: Các thẻ support trên bàn chơi
        state_list += list(numpy.array(list(dict_input['Board'].support_cards.values())))

        # Các thẻ support đã mua trong turn: 98 112
        temp = ['Wheat Field', 'Livestock Farm', 'Bakery', 'Cafe', 'Convenience Store', 'Forest', 'Stadium', 'TV Station', 'Business Complex',
                'Cheese Factory', 'Furniture Factory', 'Mine', 'Family Restaurant', 'Apple Orchard', 'Vegetable Market']
        
        list_index = []
        for name in dict_input['Cards_bought']:
            try:
                a = temp.index(name)
                list_index.append(a)
            except:
                pass
        
        t_e_m_p = [0 for i in range(15)]
        for i in range(15):
            if i in list_index:
                t_e_m_p[i] = 1
        
        state_list += t_e_m_p

        return state_list

    def action_space(self, dict_input: dict):
        if dict_input['Phase'] == 'End game':
            return ['Ngồi xem do đã hết ván game']

        if dict_input['Phase'] == 'Choose number of dice':
            return [1,2]

        if dict_input['Phase'] == 'Re-roll?':
            return ['Yes', 'No']
        
        if dict_input['Phase'] == 'Exchange':
            list_exchange_option = []
            list_player_name = [player.name for player in dict_input['Player']]
            my_sp_cards = [name for name in self.support_cards.keys() if self.support_cards[name] != 0 and name not in ['Stadium', 'TV Station', 'Business Complex']]
            for i in range(1, list_player_name.__len__()):
                id_player = (list_player_name.index(self.name) + i) % list_player_name.__len__()
                players_sp_cards = [name for name in self.support_cards.keys() if dict_input['Player'][id_player].support_cards[name] != 0 and name not in ['Stadium', 'TV Station', 'Business Complex']]
                for k1 in my_sp_cards:
                    for k2 in players_sp_cards:
                        list_exchange_option.append((k1,k2,i))
            
            list_exchange_option.append(('','',0))

            return list_exchange_option
        
        if dict_input['Phase'] == 'Coin_robbery':
            return [i for i in range(1, dict_input['Player'].__len__())]
        
        if dict_input['Phase'] == 'Card_shopping':
            list_card_name = [name for name in self.support_cards.keys() if self.coins >= self.support_cards_object[name].price
                            and name not in dict_input['Cards_bought'] and dict_input['Board'].support_cards[name] > 0]
            
            list_card_name += [name for name in self.important_land_cards.keys() if self.coins >= self.important_land_cards_object[name].price
                            and self.important_land_cards[name] == 0]

            list_card_name.append('')
            
            return list_card_name