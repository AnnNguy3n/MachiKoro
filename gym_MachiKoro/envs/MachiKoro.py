from colorama import Fore, Style
import gym
import random
import json
from gym_MachiKoro.envs.base.board import Board
from gym_MachiKoro.envs.agents import agent_interface

def p_rint_horizontal_lines():
    print('----------------------------------------------------------------------------------------------------')
    pass

def p_rint_array_card(_arr):
    print(Fore.LIGHTBLUE_EX + str(_arr[0]), _arr[1], Fore.LIGHTGREEN_EX + str(_arr[2]), Fore.LIGHTRED_EX + str(_arr[3]), Fore.LIGHTGREEN_EX + str(_arr[4]), Fore.LIGHTBLUE_EX + str(_arr[5]), Fore.LIGHTMAGENTA_EX + str(_arr[6]), _arr[7], _arr[8], Fore.LIGHTGREEN_EX + str(_arr[9]), _arr[10], Fore.LIGHTBLUE_EX + str(_arr[11]), Fore.LIGHTRED_EX + str(_arr[12]), Fore.LIGHTBLUE_EX + str(_arr[13]), Fore.LIGHTGREEN_EX + str(_arr[14]), Style.RESET_ALL, end='')

    pass

class MachiKoro_Env(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.__full_action = list(json.load(open('gym_MachiKoro/envs/action_space.json')).values())
        self.board = Board()
        self.reset()

    def reset(self):
        self.board.reset()
        temp = random.sample([i for i in range(agent_interface.lst.__len__())], k=min(agent_interface.lst.__len__(), 4))
        self.players = [agent_interface.lst[i].Agent(agent_interface.lst_name[i]) for i in temp]

        self.turn = random.choice(self.players)
        self.bonus_turn = False
        self.phase = ''
        self.phases = []
        self.is_reroll = False
        self.value_of_dice = None
        self.p_name_victory = 'None'

        self.dict_input = {
            'Board': self.board,
            'Player': [self.turn],
            'Phase': self.phase,
            'Value_of_dice': -1,
            'Cards_bought': [],
            'Remaining_exchange_times': 0,
            'Remaining_robbery_times': 0
        }

        turn_id = self.players.index(self.turn)
        for i in range(1, self.players.__len__()):
            self.dict_input['Player'].append(self.players[(turn_id+i) % self.players.__len__()])
        
    def render(self, mode='human', close=False):
        p_rint_horizontal_lines()
        k = 0
        for player in self.players:
            print(player.name, list(player.important_land_cards.values()), player.coins, end=' ')
            p_rint_array_card(list(player.support_cards.values()))
            k += 1
            if k % 2 == 0:
                print()
                pass
        
        print('Board:', end=' ')
        p_rint_array_card(list(self.board.support_cards.values()))
        print()
        pass
    
    def close(self):
        for player in self.players:
            if sum(player.important_land_cards.values()) == 4:
                return True
        
        return False

    def step(self, action_player):
        if self.close():
            self.end_turn()
            return self, None, True, None
        
        else:
            if self.phase == 'Choose number of dice':
                if action_player in [1,2]:
                    pass
                else:
                    action_player = self.__full_action[action_player]

                if action_player not in [1,2]:
                    print(Fore.LIGHTRED_EX, self.turn.name, f'tr??? action sai: {action_player}')
                    self.end_turn()
                else:
                    self.roll_the_dice(action_player)
                    if type(self.value_of_dice) == tuple and self.value_of_dice[0] == self.value_of_dice[1]\
                        and self.turn.important_land_cards['Amusement Park'] == 1:
                        self.bonus_turn = True
                        print(self.turn.name, 's??? ???????c th??m l?????t n???u ch???p nh???n k???t qu??? ????? x??c x???c')
                    else:
                        self.bonus_turn = False
                    
                    if self.is_reroll or self.turn.important_land_cards['Radio Tower'] == 0:
                        self.process()
                        self.change_phase()
                    else:
                        self.set_phase('Re-roll?')
                
            elif self.phase == 'Re-roll?':
                if type(action_player) == int:
                    action_player = self.__full_action[action_player]

                self.is_reroll = True
                if action_player.upper() == 'NO':
                    print('Kh??ng re-roll')
                    self.process()
                    self.change_phase()
                elif action_player.upper() == 'YES':
                    print('C?? re-roll')
                    if self.turn.important_land_cards['Train Station'] == 1:
                        self.set_phase('Choose number of dice')
                    else:
                        self.roll_the_dice(1)
                        self.process()
                        self.change_phase()
                else:
                    print(Fore.LIGHTRED_EX, self.turn.name, f'tr??? action sai: {action_player}')
                    self.end_turn()
            
            elif self.phase == 'Exchange':
                if type(action_player) == int:
                    action_player = self.__full_action[action_player]

                self.exchange_card(action_player[0], action_player[1], action_player[2])
            elif self.phase == 'Coin_robbery':
                if action_player in [1,2,3]:
                    pass
                else:
                    action_player = self.__full_action[action_player]

                self.coin_robbery(action_player)
            elif self.phase == 'Card_shopping':
                if type(action_player) == int:
                    action_player = self.__full_action[action_player]

                self.card_shopping(action_player)
            else:
                print(Fore.LIGHTRED_EX, f'T??n phase ??ang b??? sai: {self.phase}'.upper(), Style.RESET_ALL)
                input()

            done = self.close()
            if done:
                for player in self.players:
                    if sum(list(player.important_land_cards.values())) == 4:
                        self.p_name_victory = player.name
                        break
                
                self.set_phase('End game')
                self.end_turn()
                    
            return self, None, done, None
    
    def run_game(self):
        self.render()
        print('?????n l?????t c???a:', self.turn.name)
        if self.turn.important_land_cards['Train Station'] == 1:
            self.set_phase('Choose number of dice')
        else:
            self.roll_the_dice(1)
            if self.turn.important_land_cards['Radio Tower'] == 1:
                self.set_phase('Re-roll?')
            else:
                self.process()
                self.change_phase()

    def card_shopping(self, name: str):
        if name in self.dict_input['Cards_bought']:
            print(Fore.LIGHTRED_EX, self.turn.name, f"kh??ng th??? mua th??? '{name}' n???a do ???? mua r???i".upper(), Style.RESET_ALL)
            self.end_turn()

        elif name in ['Business Complex', 'TV Station', 'Stadium'] and self.turn.support_cards[name] != 0:
            print(Fore.LIGHTRED_EX, self.turn.name, f"kh??ng th??? mua th??? '{name}' n???a do th??? n??y ch??? ???????c mua 1 l???n".upper(), Style.RESET_ALL)
            self.end_turn()

        elif name in self.board.support_cards_object.keys():
            if self.turn.coins < self.board.support_cards_object[name].price:
                print(Fore.LIGHTRED_EX, self.turn.name, f"l???i kh??ng ????? ti???n mua th??? '{name}'".upper(), Style.RESET_ALL)
                self.end_turn()
            elif self.board.support_cards[name] == 0:
                print(Fore.LIGHTRED_EX, self.turn.name, f"th??? '{name}' ???? h???t".upper(), Style.RESET_ALL)
                self.end_turn()
            else:
                self.turn._Player__coins -= self.board.support_cards_object[name].price
                self.turn._Player__support_cards[name] += 1
                self.board._Board__support_cards[name] -= 1
                print(self.turn.name, f"???? mua th??? '{name}'")
                self.dict_input['Cards_bought'].append(name)
        
        elif name in self.turn.important_land_cards.keys():
            if self.turn.coins < self.turn.important_land_cards_object[name].price:
                print(Fore.LIGHTRED_EX, self.turn.name, f"l???i kh??ng ????? ti???n mua th??? '{name}'".upper(), Style.RESET_ALL)
                self.end_turn()
            elif self.turn.important_land_cards[name] == 1:
                print(Fore.LIGHTRED_EX, self.turn.name, f"???? m??? c??ng tr??nh '{name}' t??? tr?????c ????".upper(), Style.RESET_ALL)
                self.end_turn()
            else:
                self.turn._Player__coins -= self.turn.important_land_cards_object[name].price
                self.turn._Player__important_land_cards[name] = 1
                print(self.turn.name, f"???? m??? c??ng tr??nh '{name}'")
                self.dict_input['Cards_bought'].append(name)
                if name == 'Shopping Mall':
                    for key in self.turn.support_cards.keys():
                        if self.turn.support_cards_object[key].card_type in ['F&B Service', 'Store']:
                            self.turn._Player__support_cards_object[key]._Support_Card__income += 1

                    print("C??c th??? lo???i 'F&B Service' v?? 'Store' c???a", self.turn.name, "???? ???????c t??ng 1 ?????ng ph???n th?????ng")

                # Xem ng?????i ch??i c?? ????? ti???n mua th??? r??? nh???t tr??n b??n kh??ng, n???u kh??ng th?? skip turn lu??n cho nhanh
                temp = ['Wheat Field', 'Livestock Farm', 'Bakery', 'Cafe', 'Convenience Store', 'Forest', 'Stadium', 'TV Station', 'Business Complex',
                'Cheese Factory', 'Furniture Factory', 'Mine', 'Family Restaurant', 'Apple Orchard', 'Vegetable Market']
                
                min_ = 0
                sp_chua_mua = [name for name in temp if name not in self.dict_input['Cards_bought'] and self.board.support_cards[name] != 0]
                im_land_chua_mua = [name for name in self.turn.important_land_cards.keys() if self.turn.important_land_cards[name] == 0]
                price_sp = [self.board.support_cards_object[name].price for name in sp_chua_mua]
                price_im_land = [self.turn.important_land_cards_object[name].price for name in im_land_chua_mua]
                try:
                    min_ = min(price_im_land + price_sp)
                except:
                    min_ = 0

                if self.turn.coins < min_:
                    self.end_turn()
        
        elif name == '' or name == None:
            self.end_turn()

        else:
            print(Fore.LIGHTRED_EX, self.turn.name, f"th??? kh??ng t???n t???i: {name}".upper(), Style.RESET_ALL)
            self.end_turn()

    def end_turn(self):
        self.dict_input['Cards_bought'] = []
        self.is_reroll = False
        self.value_of_dice = None
        if self.bonus_turn:
            self.bonus_turn = False
            self.run_game()
        else:
            indexx = self.players.index(self.turn)
            turn_id = (indexx + 1) % self.players.__len__()
            self.turn = self.players[turn_id]
            self.dict_input['Player'] = [self.turn]
            for i in range(1, self.players.__len__()):
                self.dict_input['Player'].append(self.players[(turn_id+i) % self.players.__len__()])
            self.run_game()

    def coin_robbery(self, _id: int):
        id_player = (self.players.index(self.turn) + _id) % self.players.__len__()
        number = min(5, self.players[id_player].coins)
        self.turn._Player__coins += number
        self.players[id_player]._Player__coins -= number
        print(self.turn.name, f'l???y {number} ?????ng c???a', self.players[id_player].name)

        self.dict_input['Remaining_robbery_times'] -= 1
        self.change_phase()
    
    def exchange_card(self, card_give: str, card_receive: str, _id: int):
        id_player = (self.players.index(self.turn) + _id) % self.players.__len__()
        if card_give == '' or card_receive == '':
            print(Fore.LIGHTYELLOW_EX, self.turn.name, 'kh??ng th???c hi???n trao ?????i'.upper(), Style.RESET_ALL)
            input()
            pass
        elif card_give in ['Stadium', 'TV Station', 'Business Complex'] or card_receive in ['Stadium', 'TV Station', 'Business Complex']:
            print(Fore.LIGHTRED_EX, self.turn.name, "l???i trao ?????i th??? 'Big Construction'".upper(), Style.RESET_ALL)
            pass
        else:
            if self.turn.support_cards[card_give] == 0 or self.players[id_player].support_cards[card_receive] == 0:
                print(Fore.LIGHTRED_EX, self.turn.name, 'l???i kh??ng c?? th??? ????? trao ?????i'.upper(), Style.RESET_ALL)
                pass
            else:
                self.turn._Player__support_cards[card_give] -= 1
                self.turn._Player__support_cards[card_receive] += 1
                self.players[id_player]._Player__support_cards[card_give] += 1
                self.players[id_player]._Player__support_cards[card_receive] -= 1
                print(self.turn.name, f"?????i th??? '{card_give}' l???y th??? '{card_receive}' c???a", self.players[id_player].name)
        
        self.dict_input['Remaining_exchange_times'] -= 1
        self.change_phase()

    def change_phase(self):
        self.phase = self.phases.pop(0)
        self.dict_input['Phase'] = self.phase

        if self.phase == 'Card_shopping':
            # Xem ng?????i ch??i c?? ????? ti???n mua th??? r??? nh???t tr??n b??n kh??ng, n???u kh??ng th?? skip turn lu??n cho nhanh
            temp = ['Wheat Field', 'Livestock Farm', 'Bakery', 'Cafe', 'Convenience Store', 'Forest', 'Stadium', 'TV Station', 'Business Complex',
                'Cheese Factory', 'Furniture Factory', 'Mine', 'Family Restaurant', 'Apple Orchard', 'Vegetable Market']
                
            min_ = 0
            sp_chua_mua = [name for name in temp if name not in self.dict_input['Cards_bought'] and self.board.support_cards[name] != 0]
            im_land_chua_mua = [name for name in self.turn.important_land_cards.keys() if self.turn.important_land_cards[name] == 0]
            price_sp = [self.board.support_cards_object[name].price for name in sp_chua_mua]
            price_im_land = [self.turn.important_land_cards_object[name].price for name in im_land_chua_mua]
            try:
                min_ = min(price_im_land + price_sp)
            except:
                min_ = 0

            if self.turn.coins < min_:
                self.end_turn()

    def process(self):
        try:
            value_of_dice = sum(self.value_of_dice)
        except:
            value_of_dice = self.value_of_dice
        
        # Duy???t nh???ng ng?????i ch??i kh??c theo chi???u ng?????c v??ng tr?????c: Activated from ['Dice Roller', 'Anyone]
        indexx = self.players.index(self.turn)
        for i in range(indexx-1, indexx-self.players.__len__(), -1):
            active_cards = dict({item for item in self.players[i].support_cards.items()
                if value_of_dice in self.players[i].support_cards_object[item[0]].value_to_activate
                and self.players[i].support_cards_object[item[0]].activated_from in ['Anyone', 'Dice Roller']
                and item[1] != 0
            })

            income_from_bank = 0
            income_from_dice_roller = 0
            for key in active_cards.keys():
                if self.players[i].support_cards_object[key].activated_from == 'Anyone':
                    income_from_bank += self.players[i].support_cards_object[key].income * active_cards[key]
                else:
                    income_from_dice_roller += min(self.turn.coins, self.players[i].support_cards_object[key].income * active_cards[key])
            
            if income_from_bank != 0:
                self.players[i]._Player__coins += income_from_bank
                print(self.players[i].name, f'nh???n {income_from_bank} ?????ng t??? ng??n h??ng')
            
            if income_from_dice_roller != 0:
                self.turn._Player__coins -= income_from_dice_roller
                self.players[i]._Player__coins += income_from_dice_roller
                print(self.players[i].name, f'nh???n {income_from_dice_roller} ?????ng t???', self.turn.name)
        
        # Duy???t ?????n c??c th??? c???a m??nh: Activated from ['You', 'Anyone]
        my_active_cards = dict({item for item in self.turn.support_cards.items()
            if value_of_dice in self.turn.support_cards_object[item[0]].value_to_activate
            and self.turn.support_cards_object[item[0]].activated_from in ['Anyone', 'You']
            and item[1] != 0
        })
        my_active_cards = dict(sorted(my_active_cards.items()))

        income_from_bank = 0
        income_from_all_player = 0
        phases = []

        for key in my_active_cards.keys():
            if self.turn.support_cards_object[key].income_from == 'Bank':
                if self.turn.support_cards_object[key].income_times == 'Once':
                    income_from_bank += self.turn.support_cards_object[key].income * my_active_cards[key]
                else:
                    card_type_in_effect = self.turn.support_cards_object[key].card_type_in_effect
                    amount = 0
                    for key_2 in self.turn.support_cards.keys():
                        if self.turn.support_cards_object[key_2].card_type == card_type_in_effect:
                            amount += self.turn.support_cards[key_2]

                    income_from_bank += self.turn.support_cards_object[key].income * amount
            
            else:
                if self.turn.support_cards_object[key].income_from == 'Each Player':
                    for i in range(indexx-1, indexx-self.players.__len__(), -1):
                        temp = min(self.players[i].coins, 2 * my_active_cards[key])
                        if temp != 0:
                            print(self.turn.name, f'nh???n {temp} ?????ng t???', self.players[i].name)
                            income_from_all_player += temp
                            self.players[i]._Player__coins -= temp
                
                elif self.turn.support_cards_object[key].income_from == 'Chosen Player':
                    print(self.turn.name, f'c?? {my_active_cards[key]} l???n ch???n l???y t???i ??a {5} ?????ng t??? m???t ng?????i kh??c')
                    self.dict_input['Remaining_robbery_times'] = my_active_cards[key]
                    for i in range(my_active_cards[key]):
                        phases.append('Coin_robbery')
                
                else:
                    print(self.turn.name, f'c?? {my_active_cards[key]} l???n trao ?????i th??? v???i m???t ng?????i kh??c')
                    self.dict_input['Remaining_exchange_times'] = my_active_cards[key]
                    for i in range(my_active_cards[key]):
                        phases.append('Exchange')

        self.turn._Player__coins += income_from_all_player
        if income_from_bank != 0:
            print(self.turn.name, f'nh???n {income_from_bank} ?????ng t??? ng??n h??ng')
            self.turn._Player__coins += income_from_bank

        phases.append('Card_shopping')
        self.phases = phases.copy()

    def roll_the_dice(self, number_of_dice: int):
        if number_of_dice == 1:
            self.value_of_dice = random.randint(1,6)
        elif number_of_dice == 2:
            self.value_of_dice = random.randint(1,6), random.randint(1,6)
        else:
            self.value_of_dice = None
        try:
            self.dict_input['Value_of_dice'] = sum(self.value_of_dice)
        except:
            self.dict_input['Value_of_dice'] = self.value_of_dice
            
        print('Gi?? tr??? x??c x???c:', self.value_of_dice)

    def set_phase(self, phase: str):
        self.phase = phase
        self.dict_input['Phase'] = phase