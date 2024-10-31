class Deck:
    def __init__(self,players):
        self.cards_data = {
            "belper": [1, 1, 2],
            "derby": [1, 1, 2],
            "leek": [2, 2, 2],
            "stoke-on-trent": [2, 3, 3],
            "stone": [1, 2, 2],
            "uttoxeter": [1, 1, 2],
            "stafford": [2, 2, 2],
            "burton-on-trent": [2, 2, 2],
            "cannock": [1, 1, 1],
            "tamworth": [1, 1, 1],
            "walsall": [1, 1, 1],
            "coalbrookdale": [3, 3, 3],
            "dudley": [2, 3, 3],
            "kidderminster": [2, 2, 2],
            "wolverhampton": [2, 2, 2],
            "worcester": [2, 2, 2],
            "birmingham": [3, 3, 3],
            "coventry": [3, 3, 3],
            "nuneaton": [1, 1, 1],
            "redditch": [1, 1, 1],
            "iron": [4, 4, 4],
            "coal": [4, 4, 4],
            "goods": [5, 5, 5],
            "pottery": [5, 5, 5],
            "beer": [5, 5, 5],
        }
        self.players = players
        self.deck = self.build_deck()
        self.shuffle_deck()

    def build_deck(self):
        deck = []
        for card_name, counts in self.cards_data.items():
            count = counts[self.players - 2]  
            deck.extend([card_name] * count)
        return deck
    
    def shuffle_deck(self):
        import random
        random.shuffle(self.deck)

    def draw_card(self):
        if self.deck:
            return self.deck.pop()
        else:
            return None
        
    def deck_size(self):
        return len(self.deck)
        