import numpy as np

class Player:
    def __init__(self):
        self.industries = {"coal":0,"iron":1,"beer":2,
                         "cotton":3,"pottery":4,"goods":5}
        self.ranks = np.array((1,2,3,4,5,6,7,8))
        self.tiles = np.array((
            (1,2,2,2,0,0,0,0), # coal
            (1,1,1,1,0,0,0,0), # iron
            (1,2,2,2,0,0,0,0), # beer
            (3,2,3,3,0,0,0,0), # cotton
            (1,1,1,1,1,0,0,0), # pottery
            (1,2,1,1,2,1,1,2)))# goods
        self.placed_tile = False
        self.networks = 14
        self.coins = 17
        self.income = 0
        self.income_pos = 10
        self.score = 0

        self.hand = ["empty","empty","empty","empty",
                     "empty","empty","empty","empty"]
    
    def remove_tile(self,industry):
        industry_num = self.industries[industry]
        for rank in range(8):
            if self.tiles[industry_num,rank] != 0: 
                self.tiles[industry_num,rank] -= 1
                return True
        return False
    
    def add_tile(self,industry,rank):
        industry_num = self.industries[industry]
        self.tiles[industry_num,(rank-1)] += 1
    
    def remove_network(self):
        if self.networks >= 0: self.networks -= 1

    def progress_income(self,steps):
        if self.income_pos+steps < 99:
            self.income_pos += steps
            # update income:
            if 0 <= self.income_pos <= 10:
                self.income = self.income_pos - 10
            elif 11 <= self.income_pos <= 30:
                self.income = (self.income_pos - 11) // 2 + 1
            elif 31 <= self.income_pos <= 60:
                self.income = (self.income_pos - 31) // 3 + 11
            elif 61 <= self.income_pos <= 96:
                self.income = (self.income_pos - 61) // 4 + 21
            return True
        else: return False
    
    def regress_income(self,levels):
        if self.income-levels > -10:
            self.income -= levels
            # update income position
            if -10 <= self.income <= 0:
                self.income_pos = self.income + 10
            elif 1 <= self.income <= 10:
                self.income_pos = (self.income - 1) * 2 + 12
            elif 11 <= self.income <= 20:
                self.income_pos = (self.income - 11) * 3 + 33
            elif 21 <= self.income <= 29:
                self.income_pos = (self.income - 21) * 4 + 64
            return True
        else: return False
    
    def discard(self,card):
        if card in self.hand:
            self.hand.remove(card)
            self.hand.append("empty")
            return True
        else: return False
    
    def get_card(self,card):
        if "empty" in self.hand:
            self.hand.remove("empty")
            self.hand.append(card)
            return True
        else: return False

    

