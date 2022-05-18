from copy import deepcopy
import pandas
from gym_MachiKoro.envs.base.card import Support_Card, Important_Land_Card


class Player:
    def __init__(self, name):
        self.__name = name
        self.__full_action = []
        self.__amount_action_space = 0
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