from copy import deepcopy
import pandas
from gym_MachiKoro.envs.base.card import Support_Card


class Board:
    def __init__(self):
        data = pandas.read_csv('gym_MachiKoro/envs/base/card.csv', index_col='name')
        temp = ['Wheat Field', 'Livestock Farm', 'Bakery', 'Cafe', 'Convenience Store', 'Forest', 'Stadium', 'TV Station', 'Business Complex',
                'Cheese Factory', 'Furniture Factory', 'Mine', 'Family Restaurant', 'Apple Orchard', 'Vegetable Market']

        self.__support_cards_object = {}
        for name in temp:
            try:
                income = int(data['income'][name])
            except:
                income = None

            self.__support_cards_object[name] = Support_Card(data['card_type'][name], name, int(data['price'][name]), data['description'][name],[int(a) for a in data['value_to_activate'][name].split(',')],
                                                            data['activated_from'][name], income, data['income_from'][name], data['income_times'][name], data['card_type_in_effect'][name])
                                                            
        self.reset()
    
    def reset(self):
        temp = ['Wheat Field', 'Livestock Farm', 'Bakery', 'Cafe', 'Convenience Store', 'Forest', 'Stadium', 'TV Station', 'Business Complex',
                'Cheese Factory', 'Furniture Factory', 'Mine', 'Family Restaurant', 'Apple Orchard', 'Vegetable Market']

        self.__support_cards = {}
        for name in temp:
            if name not in ['Stadium', 'TV Station', 'Business Complex']:
                self.__support_cards[name] = 6
            else:
                self.__support_cards[name] = 4

    @property
    def support_cards(self):
        return deepcopy(self.__support_cards)

    @property
    def support_cards_object(self):
        return deepcopy(self.__support_cards_object)