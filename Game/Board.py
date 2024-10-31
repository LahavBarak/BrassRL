import pandas as pd
import numpy as np
import networkx as nx
import random
import ast

class Board:

    def __init__(self,players = 4,network = "canals"):
        self.cities = self.import_map("cities")
        self.markets = self.import_map("markets")
        self.map = self.create_graph(network)
        self.randomize_markets(players)

    def import_map(self, node):
        csv_file = f'../Resources/{node}.csv'
        df = pd.read_csv(csv_file, sep=';')
        def parse_list_column(column):
            return column.apply(lambda x: ast.literal_eval(x))
        for col in df.columns[1:]:  # Skip the first column as it contains names
            df[col] = parse_list_column(df[col])
        # Create instances of City and store them in a list
        if node == "cities":
            cities = []
            for _, row in df.iterrows():
                city = City(
                    name=row['name'],
                    canals=row['canals'],
                    rails=row['rails'],
                    locations=(row['loc1'],row['loc2'],row['loc3'],row['loc4'])
                )
                cities.append(city)
            return cities
        elif node == "markets":
            markets = []
            for _, row in df.iterrows():
                market = Market(
                    name=row['name'],
                    canals=row['canals'],
                    rails=row['rails']
                )
                markets.append(market)
            return markets
    
    def get_city(self,city_name):
        for city in self.cities:
            if city.name.lower() == city_name.lower():  # Case insensitive comparison
                return city
        return None
    
    def get_market(self,market_name):
        for market in self.markets:
            if market.name.lower() == market_name.lower():  # Case insensitive comparison
                return market
        return None
    
    def randomize_markets(self, players):
        tokens = ["empty","empty","cotton","goods","all","empty","pottery","cotton","goods"]
        markets = ["gloucester", "oxford", "shrewsbury", "warrington", "nottingham"]  # Example markets

        if (players < 4): 
            tokens.remove("cotton")
            tokens.remove("goods")
            markets.remove("nottingham")
        if (players < 3): 
            tokens.remove("empty")
            tokens.remove("pottery")
            markets.remove("warrington")
        for name in markets:
            market = self.get_market(name)
            if name == "shrewsbury":
                token = random.sample(tokens,1)
                market.products = token
                tokens.remove(token[0])
            else:
                token_sel = random.sample(tokens,2)
                market.products = token_sel
                for token in token_sel: 
                    tokens.remove(token)      
        return tokens
    
    def create_graph(self,edge_type):
        gameMap = nx.Graph()
        for market in self.markets:
            gameMap.add_node(market.name)
        for city in self.cities:
            gameMap.add_node(city.name)
            edges = getattr(city, edge_type)
            for edge in edges:
                gameMap.add_edge(city.name,edge, occupied = 0)
        return gameMap
    
    def occupy_edge(self,city1,city2,player):
        if self.map.has_edge(city1,city2) and self.map[city1][city2]['occupied'] == 0:
            self.map[city1][city2]['occupied'] = player
            return player
        return False
    
    def is_edge_occupied(self, city1, city2):
        return self.map[city1][city2]['occupied'] if self.map.has_edge(city1, city2) else None

    def in_network(self, player, city1, city2 = None):
        if city2 is None: # city or market
            # Rule 1: Check if the city is occupied by the player
            if player in self.get_city(city1).taken:  # Check if any location in the city is occupied by the player
                return True
            # Rule 2: Check connected edges
            connected_edges = self.map.edges(city1)
            for edge in connected_edges:
                if self.is_edge_occupied(edge[0], edge[1]) == player:
                    return True
        else:       
            # Check if either node of the edge is in the player's network
            if self.is_in_network(player, city1) or self.is_in_network(player, city2):
                return True
        return False
    
    def is_connected(self, city1, city2):
        """Check if there is an occupied path between two cities."""
        visited = set()  # Track visited cities to avoid cycles
        queue = [city1]  # BFS queue starting from city1
        while queue:
            current_city = queue.pop(0)  # Dequeue the first city
            if current_city == city2:  # If we reached the target city, return True
                return True
            visited.add(current_city)  # Mark the city as visited
            # Iterate over all neighbors of the current city
            for neighbor in self.map.neighbors(current_city):
                # Check if the edge between current city and neighbor is occupied
                if self.is_edge_occupied(current_city, neighbor) and neighbor not in visited:
                    queue.append(neighbor)  # Add the neighbor to the queue
        return False  # No occupied path found
    
    def closest_coal(self, city):
        """Find all the nearest connected cities with coal, taken, and with resources."""
        visited = set()  # To avoid revisiting cities
        queue = [(city, 0)]  # (city, distance) pairs for BFS
        results = []  # Store all valid coal locations at the closest distance
        min_distance = None  # Track the first valid distance found
        while queue:
            current_city, distance = queue.pop(0)  # Dequeue the first city
            # If we found a valid coal location at a distance, store it
            if min_distance is None or distance == min_distance:
                coals = self._get_available_industry_locations(current_city,"coal")
                if coals:  # If the city has any valid coal locations
                    results.extend([(current_city, loc) for loc in coals])
                    min_distance = distance  # Set the minimum distance if not set
            # Stop if we've already processed all cities at the closest distance
            if min_distance is not None and distance > min_distance:
                break
            visited.add(current_city)  # Mark as visited
            # Explore neighbors connected by occupied edges
            for neighbor in self.map.neighbors(current_city):
                if self.is_edge_occupied(current_city, neighbor) and neighbor not in visited:
                    queue.append((neighbor, distance + 1))  # Add neighbor to queue
        return results if results else None
    
    def _get_available_industry_locations(self, city_name, industry):
        """Return the location numbers of valid coal locations in a city."""
        city = self.get_city(city_name)
        if not city:
            return []
        coal_locations = []
        for i, location in enumerate(city.locations):
            if industry in location and city.taken[i] != 0 and city.resources[i] > 0:
                coal_locations.append(i + 1)  # Return human-readable location numbers (1-indexed)
        return coal_locations

    def industry_available(self, industry):
        results = []
        for city in self.cities:
            for i, location in enumerate(city.locations):
                if industry in location and city.taken[i] != 0 and city.resources[i] > 0:
                    results.append([city.name,i+1])
        return results if results else None


class City:
    def __init__(self,name,canals,rails,locations):
        self.name = name
        self.canals = canals
        self.rails = rails
        self.locations = list(locations)
        self.taken = [0,0,0,0] # player_num if taken, 0 if free
        self.rank = [0,0,0,0] # rank of tile
        self.flipped = [0,0,0,0] 
        self.resources = [0,0,0,0] # amount of resources on tile, if any

    def build(self,industry, rank, location, player, resources = 0): # simplified, no double vs single location check
        location = location-1 # translate from human count to python count
        # check if not taken by others
        if self.taken[location] == 0 or self.taken[location] == player: untaken = True
        else: untaken = False
        # check if tile contains industry and build
        if industry in self.locations[location] and untaken: 
            self.locations[location] = [industry]
            self.taken[location] = player
            self.rank[location] = rank
            self.resources[location] = resources
            noIndustry = True
        else: noIndustry = False
        return untaken, noIndustry

class Market:
    def __init__(self,name,canals,rails):
        self.name = name
        self.canals = canals
        self.rails = rails
        self.products = []
        self.beer = np.array((1,1))

    def reset_beers(self):
        self.beer = np.array((1,1))
    
    def use_beer(self,product,spot):
        spot -= 1
        if self.products[spot] == product:
            self.beer[spot] = 0
            return 0
        return -1

def test():
    board = Board(3)
    # tile1 = board.get_city("cannock").build("coal",1,2,1,2)
    # tile2 = board.get_city("cannock").build("coal",1,1,2,1)
    # tile3 = board.get_city("dudley").build("iron",1,1,1,2)
    # tile4 = board.get_city("wolverhampton").build("coal",1,2,1,2)
    # print(f"tiles success {tile1},{tile2},{tile3},{tile4}")
    print(board.closest_coal("cannock")) # expect cannock (x2) and wolverhampton
    print(board.industry_available("iron")) # expect dudley

if __name__ == "__main__":
    test()


        