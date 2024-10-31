from Board import Board
from Player import Player
from Deck import Deck
import numpy as np
import random

class Game:
    def __init__(self, player_num):
        self.board = Board(player_num,"canals")
        self.deck = Deck(player_num)
        self.players = []
        for i in range(player_num):
            player = Player()
            # draw initial hand
            for j in range(8):  # draw initial hand
                player.get_card(self.deck.draw_card())
            self.deck.draw_card() # discard one per player
            self.players.append(player)
        
        self.coal_cubes = 13
        self.iron_cubes = 8

        self.turn_order = [1,2,3,4]
        random.shuffle(self.turn_order)
        self.spendings = [0,0,0,0]
    
    def build(self,player,card,city,location):
        ## PLACEHOLDER for build action
        pass

    def canal(self,player,card,city1,city2):
        # check network rules
        if self.players[player].placed_tile and self.board.in_network(player,city1,city2) is False:
            return -4 # not in network
        if card == "empty": return -1
        if self.players[player].coins >= 3:
            self.players[player].coins -= 3
        else: return -2 # not enough money
        if self.players[player].discard(card) : # discard. if ok...
            if self.board.occupy_edge(city1,city2,player) == player: # place network.
                self.players[player].placed_tile = True
                return True
            else: # if network is occupied
                self.players[player].get_card(card)
                self.players[player].coins += 3
                return -3 # network occupied
        else: # if card is bad
            self.players[player].coins -= 3
            return -1 # bad card
        
    def rail(self,player,card,city1,city2):
        ## PLACEHOLDER for rail network action
        pass

    def develop(self,player,card,industry1,industry2 = None):
        # iron_available = self.board.industry_available("iron")
        # if iron_available is None:
        #     iron_source = "market"
        
        # if iron_source = "market" and iron_available is None
        pass
    
    def sell(self,player,card):
        ## PLACEHOLDER for sell action
        pass
    
    def loan(self,player,card):
        if self.players[player].discard(card): # discard. if ok...
            if self.players[player].regress_income(3): # lose 3 income. if ok...
                self.players[player].coins += 30
                return True
            else: return -2 # not enough income
        else: return -1 # bad card

    def scout(self,player,card1,card2,card3):
        card1flag = False
        card2flag = False
        card3flag = False
        if self.players[player].discard(card1): card1flag = True
        else: return -1 # card1 bad
        if self.players[player].discard(card2): card2flag = True
        else: return -2 # card2 bad
        if self.players[player].discard(card3): card3flag = True
        else: return -3 # card3 bad
        if card1flag is True and card2flag is True and card3flag is True:
            self.players[player].get_card("joker_industry")
            self.players[player].get_card("joker_location")
            return True
        return False
    
    def iron_price(self):
        if self.iron_cubes <= 0: return 6
        else: return (12-self.iron_cubes)/2 
    
    def coal_price(self):
        if self.coal_cubes <= 0: return 8
        else: return (16-self.coal_cubes)/2 

import code

def test():
    game = Game(3)
    
    # Start an interactive console with the game object in its namespace
    console = code.InteractiveConsole(locals={'game': game})
    console.interact("Interactive Game Console. Type your commands below:")

if __name__ == "__main__":
    test()

        
