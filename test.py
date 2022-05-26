import numpy as np
def tiletungxucxac(count_dice, number_of_dice):
    tile = {}
    if count_dice == 1:
        for i in range(1, 7):tile[i] = 1/6
        try: ratio = tile[number_of_dice]
        except: ratio = 0
        return ratio
    else:
        for i in range(2, 13):
            if i >= 7:tile[i] = ((13-i)/18)
            else:tile[i] =  ((i-1)/18)
        try: ratio = tile[number_of_dice]
        except: ratio = 0
        return ratio

def values_card(count_dice, arr, i, card_vl):
    values_of_card = 0
    for number_of_dice in arr[0]:
        if 'Exchange' in arr:values_of_card += tiletungxucxac(count_dice, number_of_dice)*3 - arr[1]
        elif 'Each Player' in arr:values_of_card += tiletungxucxac(count_dice, number_of_dice)*3 + arr[2]*4 - arr[1]
        elif 'Anyone' in arr:values_of_card += tiletungxucxac(count_dice, number_of_dice)*4+ arr[2]*4 - arr[1]
        else:values_of_card += tiletungxucxac(count_dice, number_of_dice)+ arr[2]*4 - arr[1]
    return values_of_card

print(tiletungxucxac(1, 7))
card_bought = {'Wheat Field': 3, 'Livestock Farm': 3, 'Bakery': 4, 'Cafe': 1, 'Convenience Store': 3, 'Forest': 1, 'Stadium': 2, 'TV Station': 1, 'Business Complex': 1, 'Cheese Factory': 2, 'Furniture Factory': 2, 'Mine': 4, 'Family Restaurant': 1, 'Apple Orchard': 2, 'Vegetable Market': 1}
card_bought_vl = card_bought.values()
card = {'Wheat Field': [[1], 1, 1, 'Bank', 'Once', np.nan], 'Livestock Farm': [[2], 1, 1, 'Bank', 'Once', np.nan], 'Bakery': [[2, 3], 1, 2, 'Bank', 'Once', np.nan], 'Cafe': [[3], 2, 2, 'Dice Roller', 'Once', np.nan], 'Convenience Store': [[4], 2, 4, 'Bank', 'Once', np.nan], 'Forest': [[5], 3, 1, 'Bank', 'Once', np.nan], 'Stadium': [[6], 6, 2, 'Each Player', 'Each Player', np.nan], 'TV Station': [[6], 7, 5, 'Chosen Player', 'Once', np.nan], 'Business Complex': [[6], 8, None, 'Exchange', 'Once', np.nan], 'Cheese Factory': [[7], 5, 3, 'Bank', 'Each Card_type', 'Farm'], 'Furniture Factory': [[8], 3, 3, 'Bank', 'Each Card_type', 'Industry'], 'Mine': [[9], 6, 5, 'Bank', 'Once', np.nan], 'Family Restaurant': [[9, 10], 3, 3, 'Dice Roller', 'Once', np.nan], 'Apple Orchard': [[10], 3, 3, 'Bank', 'Once', np.nan], 'Vegetable Market': [[11, 12], 2, 2, 'Bank', 'Each Card_type', 'Field']}
card_vl = card.values()
for card_id in card_vl:
    print(values_card(1, card_id, card_vl.index(card_id), card_vl))
    