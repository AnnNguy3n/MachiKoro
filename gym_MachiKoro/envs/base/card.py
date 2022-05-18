from copy import deepcopy


class Card:
    def __init__(self, card_type: str, name: str, price: int, description: str):
        self.__card_type = card_type # Cái biểu tượng bên cạnh tên thẻ
        self.__name = name
        self.__price = price # Giá để mua thẻ
        self.__description = description

    @property
    def card_type(self):
        return self.__card_type
    
    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def description(self):
        return self.__description

    def convert_to_dict(self):
        return deepcopy({
            'card_type': self.__card_type,
            'name': self.__name,
            'price': self.__price
        })
        

class Important_Land_Card(Card):
    def __init__(self, card_type: str, name: str, price: int, description: str):
        super().__init__(card_type, name, price, description)

class Support_Card(Card):
    def __init__(self, card_type: str, name: str, price: int, description: str, value_to_activate: list, activated_from: str,
                income: None or int, income_from: str, income_times: str, card_type_in_effect: None or str):
        super().__init__(card_type, name, price, description)
        self.__value_to_activate = value_to_activate.copy()
        self.__activated_from = activated_from
        self.__income = income
        self.__income_from = income_from
        self.__income_times = income_times
        self.__card_type_in_effect = card_type_in_effect
    
    @property
    def value_to_activate(self):
        return self.__value_to_activate.copy()
    
    @property
    def activated_from(self):
        return self.__activated_from
    
    @property
    def income(self):
        return self.__income
    
    @property
    def income_from(self):
        return self.__income_from
    
    @property
    def income_times(self):
        return self.__income_times
    
    @property
    def card_type_in_effect(self):
        return self.__card_type_in_effect

    def convert_to_dict(self):
        return deepcopy({
            'card_type': self.card_type,
            'name': self.name,
            'price': self.price,
            'value_to_activate': self.__value_to_activate.copy(),
            'activated_from': self.__activated_from,
            'income': self.__income,
            'income_from': self.__income_from,
            'income_times': self.__income_times,
            'card_type_in_effect': self.__card_type_in_effect
        })