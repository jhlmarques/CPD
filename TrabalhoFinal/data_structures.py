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
        self.player_ratings = []  # 20 best rated

    # Try to insert a new (rating, player_ID) pair
    def insert_rating(self, rating, player_ID):
        if len(self.player_ratings) < 20 or \
                (rating > self.player_ratings[-1][0] and
                 (self.player_ratings.pop(-1) or True)):  # Taking advantage of lazy 'or' and lazy 'and'
            # Basically: insert at the correct position; if there are > 20 it must be greater than the last
            # element, which is then removed
            insertion_idx = 0
            for p_rating, _ in self.player_ratings:
                if p_rating > rating:
                    insertion_idx += 1
                    continue
                break
            self.player_ratings.insert(insertion_idx, (rating, player_ID))  # Insert at the correct position


# Fast prefix-based finding
class Trie:

    # Add a string to the Trie
    def insert(self, string: str):
        pass


# Hash table that stores ID -> Data class pairs
class HashID:

    def __init__(self, size):
        self.size = size
        self.table = [[]] * size

    # Adds a key - value pair.
    def insert(self, key: int, value):
        pos = key % self.size
        key_list = self.table[pos]


        # Insertion sort - add new element to collision list
        insertion_idx = 0
        for i, _ in key_list:
            if i < key:
                insertion_idx += 1
            break
        key_list.insert(insertion_idx, (key, value))

    # Finds the data associated to the key
    def find(self, key):
        pos = key % self.size
        key_list = self.table[pos]
        return


# Hash table that stores String -> Data class pairs
class HashString:

    # Adds a key - value pair
    def insert(self, key: int, value):
        pass

    # Finds the data associated to the key
    def find(self, key):
        pass
