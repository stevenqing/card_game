import gym
import random

class CardEnv(gym.Env):
    def __init__(self):
        self.CARD_RANK_STR = ['D4','C4','H4','S4','D6','C6','H6','S6','D8','C8','H8','S8','D9','C9','H9','S9','DT','CT','HT','ST','DJ','CJ','HJ','SJ','DQ','CQ','HQ','SQ','DK','CK','HK','SK','DA','CA','HA','SA','D3','C3','H3','S3','D2','C2','H2','S2','D5','C5','H5','S5','SmallJoker','BigJoker''D7','C7','H7','S7',]
        self.ACTION_SPACE = ['p1','p2','p3','p4','p5','pass']
        self.BOUNUS_CARDS_5 = ['D5','C5','H5','S5']
        self.BOUNUS_CARDS_10 =['DT','CT','HT','ST','DK','CK','HK','SK']
        ORIGINAL_CARD_PILE = random.sample(self.CARD_RANK_STR,len(self.CARD_RANK_STR))
        #print(CARD_RANK_STR)
        self.actions = self.ACTION_SPACE
        self.cards = self.CARD_RANK_STR
        #print(self.cards)
        self.original_card_pile = ORIGINAL_CARD_PILE
        #print(self.original_card_pile)
        self.original_hand_card_1 = self.original_card_pile[:5]
        del self.original_card_pile[:5]
        self.original_hand_card_2 = self.original_card_pile[:5]
        del self.original_card_pile[:5]
        self.player_cards_1 = self.original_hand_card_1
        self.player_cards_2 = self.original_hand_card_2
        self.first_player = 0
        self.actions_buffer = []
        self.start_position = 0
        self.player_scores_1 = 0
        self.player_scores_2 = 0
        self.cards_buffer = []
        self.stage_number = 0
        self.winner_number = None
        self.played_card = None
        #print('CardEnv Environment initialized')
    
    def sort_str(self,card_1,card_2):
	    ''' 比较两张牌大小
		card_1大返回1，card_2大返回2'''
	    key_1 = self.CARD_RANK_STR.index(card_1)
	    key_2 = self.CARD_RANK_STR.index(card_2)
	    if  key_1>key_2:
		    return 1
	    if key_1<key_2:
		    return -1
	    return 0

    def sort_list(self,card_list):
        card_list = sorted(card_list,key=self.CARD_RANK_STR.index)
        return card_list
    
    
    def draw_cards(self,player_cards):
        '''抽卡抽至五张'''
        if len(player_cards) == 5:
            return player_cards
        if len(player_cards) < 5:
            diff = 5-len(player_cards)
            try: #添加对于牌堆不够的情况
                player_cards +=(self.original_card_pile[:diff])
                del self.original_card_pile[:diff]
            except:
                player_cards+=self.original_card_pile
        return player_cards
    
    def calculate_score(self,played_cards):
        '''计算一轮下来所得的分数'''
        winner_bounus = 0
        for i in played_cards:
            if i in set(self.BOUNUS_CARDS_5):
                winner_bounus+=5
            if i in set(self.BOUNUS_CARDS_10):
                winner_bounus+=10
        return winner_bounus
    
    def round(self,action_1,action_2):
        '''1. 确定第一个人为第几号玩家并出牌
           2. 各个人各自行动
           3. 两人有一人pass之后结束round
           4. 计算赢家的scores'''
        done = 0
        self.player_cards_1 = self.sort_list(self.player_cards_1) #对手牌排序
        self.player_cards_2 = self.sort_list(self.player_cards_2)
        self.winner_number = None #每一轮开始winner置为none
        self.first_player = self.start_position
        if self.first_player == 0: #第一位玩家先出
            for i in range(len(self.actions)): 
                if action_1 == self.actions[i]: #不可以将两个合并，e.g:action_1为4，action_2为1，则action_2先触发，顺序出错
                    if i == 5: #操作为pass
                        self.player_cards_1 = self.player_cards_1
                        self.start_position = 1
                        self.actions_buffer.append(action_1)
                        break
                    #print(self.player_cards_1)
                    if self.player_cards_1: #判断player_card是否为空，为空则自动pass回合
                        try:
                            #print(self.player_cards_1,i)
                            #print(self.original_card_pile)
                            self.cards_buffer.append(self.player_cards_1[i]) #添加这轮出的牌
                            self.player_cards_1.pop(i) #删除打出的牌
                            self.played_card = self.cards_buffer[-1]
                            #print(self.player_cards_1)
                            self.actions_buffer.append(action_1) #添加这轮作出的动作
                        except:
                            break
                    if self.player_cards_1==None:
                        action_1 = 'pass' #在player_cards不存在的情况下给action赋值为pass,为何进入except
                        self.actions_buffer.append(action_1)
                        break
            for i in range(len(self.actions)): #对第二位玩家进行操作
                if action_2 == self.actions[i]:
                    if i == 5:
                        self.player_cards_2 = self.player_cards_2
                        self.actions_buffer.append(action_2)
                        break
                    try: #考虑第一个动作为pass的情况
                        #print(self.played_card,self.player_cards_2[i])
                        judge = self.sort_str(self.played_card,self.player_cards_2[i])
                    except:
                        break
                    if judge == -1:
                        if self.player_cards_2:
                            try:
                                self.cards_buffer.append(self.player_cards_2[i])
                                self.player_cards_2.pop(i)
                                self.actions_buffer.append(action_2)
                            except:
                                break
                        if self.player_cards_2 == None:
                            action_2 = 'pass'
                            self.actions_buffer.append(action_2)
                    if judge == 1:
                        action_2 = 'pass'
                        self.actions_buffer.append(action_2)
                        break

        if self.first_player == 1: #第二位玩家先出
            for i in range(len(self.actions)):
                if action_2 == self.actions[i]:
                    if i == 5:
                        self.player_cards_2 = self.player_cards_2
                        self.start_position = 0
                        self.actions_buffer.append(action_2)
                        break
                    try:
                        self.cards_buffer.append(self.player_cards_2[i])
                        self.player_cards_2.pop(i)
                        self.played_card = self.cards_buffer[-1]
                        self.actions_buffer.append(action_2)
                    except:
                        action_2 = 'pass'
            for i in range(len(self.actions)):
                if action_1 == self.actions[i]:
                    if i == 5:
                        self.player_cards_1 = self.player_cards_1
                        self.actions_buffer.append(action_1)
                        break
                    #print(self.player_cards_2)
                    try:
                        #print(self.played_card,self.player_cards_1[i])
                        judge = self.sort_str(self.played_card,self.player_cards_1[i])
                    except:
                        break
                    if judge == -1:
                        try:
                            self.cards_buffer.append(self.player_cards_1[i])
                            self.player_cards_1.pop(i)
                            self.actions_buffer.append(action_1)
                        except:
                            action_1 = 'pass'
                    if judge == 1:
                        action_1 = 'pass'
        if action_1 == 'pass' or action_2 == 'pass':
            #print(self.cards_buffer)
            if self.start_position == 0:#player1 wins
                self.player_scores_1+=self.calculate_score(self.cards_buffer)
                self.cards_buffer = []
                

            if self.start_position == 1:#player2 wins
                self.player_scores_2+=self.calculate_score(self.cards_buffer)
                self.cards_buffer = []
                
        #print(self.original_card_pile,self.player_cards_1,self.player_cards_2)
        if self.player_cards_1 == []:
            done = 1
            self.player_scores_2+=100-self.player_scores_1-self.player_scores_2
            if self.player_scores_1 > self.player_scores_2:
                self.winner_number = 1
            if self.player_scores_1 < self.player_scores_2:
                self.winner_number = 2
            if self.player_scores_1 == self.player_scores_2:
                self.winner_number = 0
                
        if self.player_cards_2 == []:
            done = 1
            self.player_scores_1+=100-self.player_scores_1-self.player_scores_2
            if self.player_scores_1 > self.player_scores_2:
                self.winner_number = 1
            if self.player_scores_1 < self.player_scores_2:
                self.winner_number = 2
            if self.player_scores_1 == self.player_scores_2:
                self.winner_number = 0
        #print('CardEnv Step successful!')
        return self.winner_number,done,self.actions_buffer,self.player_scores_1,self.player_scores_2
    
    def reset_round(self):
        self.player_cards_1 = self.draw_cards(self.player_cards_1)
        self.player_cards_2 = self.draw_cards(self.player_cards_2)
        #print(self.player_cards_1)
        #print('CardEnv Environment reset')

        

#using guide
#







