class Card:
    def __init__(self, name: str, price: int, effective_value: list, card_type: str, coins: int):
        self.__name = name
        self.__price = price
        self.__effective_value = effective_value.copy()
        self.__card_type = card_type
        self