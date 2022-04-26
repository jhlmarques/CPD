from dataclasses import dataclass


@dataclass
class PlayerData:
    name: str
    id: int
    positions: list
    ratings: 'HashString'
    sum_of_ratings: int = 0
    n_of_ratings: int = 0


class UserData:

    def __init__(self, id):
        self.id = id
        self.player_ratings = []  # 20 best ratings (sorted)
        self.insertion_index = 0

    # Try to insert a new (rating, player_data) pair, keeping the elements in descending order with regards to their rating
    # The following behaviours are present in order to increase efficiency:
    # - Has no control over how many ratings can be added
    # - Assumes that the current insertion has greater rating than the last element
    def insert_rating(self, rating, player_data, reached_capacity=False):

        # Remove the element with the lowest rating
        if reached_capacity:
            self.player_ratings.pop(-1)

        idx = self.insertion_index  # Skip elements with the highest possible rating
        
        for i in range(self.insertion_index, len(self.player_ratings)):
            if self.player_ratings[i][0] < rating:
                break
            idx += 1
        self.player_ratings.insert(idx, (rating, player_data))  # Insert while keeping descending order
        
        if rating == 5.0:
            self.insertion_index += 1

# Fast prefix-based finding
class Trie:

    # Add a string to the Trie, with the last node containing the data
    def insert(self, string: str, data):
        pass


# Hash table that stores ID -> Data class pairs
class HashID:

    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    # Adds a key - value pair.
    def insert(self, key: int, value):
        pos = key % self.size
        self.table[pos].append((key, value))

    # Finds the data associated to the key
    def find(self, key):
        pos = key % self.size
        key_list = self.table[pos]
        for item in key_list:
            if item[0] == key:
                return item[1]
        return None


# Hash table that stores String -> Data class pairs
class HashString:

    # Adds a key - value pair
    def insert(self, key: int, value):
        pass

    # Finds the data associated to the key
    def find(self, key):
        pass
