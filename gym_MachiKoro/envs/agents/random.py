from ..base.player import Player
import random
import math
import json
import numpy as np
from colorama import Fore, Style

# Các loại thẻ:
#     - F&B Service: dịch vụ ăn uống, tương ứng với 2 thẻ hỗ trợ màu đỏ, có biểu tượng là cái ly
#     - Big Construction: công trình lớn, tương ứng với 3 thẻ hỗ trợ màu tím và 4 vùng đất quan trọng, có biểu tượng là 1 tượng đài
#     - Field: cánh đồng, tương ứng với các thẻ 'vườn táo' và 'cánh đồng lúa mì', biểu tượng là cây lúa
#     - Store: cửa hàng, tương ứng với các thẻ 'tiệm bánh' và 'cửa hàng tiện lợi', biểu tượng giống mặt tiền của 1 gian hàng
#     - Farm: nông trại, ứng với thẻ 'nông trại', biểu tượng là con trâu
#     - Industry: công nghiệp, tương ứng với các thẻ 'rừng' và 'khu mỏ quặng', biểu tượng là bánh răng
#     - Factory: nhà máy, tương ứng với các thẻ 'nhà máy pho mát' và 'nhà máy nội thất', biểu tượng là lưỡi cưa
#     - Market: chợ, ứng với thẻ 'chợ trái cây và rau củ', biểu tượng là quả cam có 2 lá

#thẻ
# Bakery: tiệm bánh
# Wheat Field: Cánh đồng lúa mỳ
# Vegetable Market: chợ trái cây và rau củ
# Livestock Farm : Nông trại 
# Convenience Store: Cửa hàng tiện lợi
# Family Restaurant : quán ăn gia đình

#Công trình:
#Train Station: Nhà ga
#

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  dict_input):
        state = dict_input
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        action = random.choice(a)
        # self.check_vtr(dict_input)
        return action
    
    def check_vtr(self, dict_input):
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(self.name, 'Thắng')
            pass
        elif victory == 0:
            print(self.name, 'Thua')
            pass