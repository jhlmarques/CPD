from dataclasses import dataclass
from unidecode import unidecode

@dataclass
class PlayerData:
    name: str
    id: int
    positions: list
    tags: 'HashString'
    average: int = 0
    sum_of_ratings: int = 0
    n_of_ratings: int = 0

    # Greater than
    def __lt__(self, y: 'PlayerData'):
        return self.average > y.average

    # Less than
    def __lt__(self, y: 'PlayerData'):
        return self.average < y.average

    # Check equality
    def __eq__(self, y: 'PlayerData') :
        return self.id == y.id

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
class TrieNode:
     
    # Trie node class
    def __init__(self):
        self.children = [None]*31
        self.is_end_of_word = False
        self.data = None
 
class Trie:
    def __init__(self):
        self.root = self.get_node()
 
    def get_node(self):
        return TrieNode()
 
    def ascii_to_index(self, ch):
        if ch == ' ':
            return 26
        elif ch == '"':
            return 27
        elif ch == '-':
            return 28
        elif ch == '.':
            return 29
        elif ch == "'":
            return 30
        else:
            return ord(ch) - ord('a')
 
 
    def insert(self, player_name, data):
        pointer = self.root
        player_name = unidecode(player_name.lower())
        for ch in player_name:
            index = self.ascii_to_index(ch) 
            # adds node if it doesn't already exists
            if not pointer.children[index]:
                pointer.children[index] = self.get_node()
            pointer = pointer.children[index] 
        pointer.is_end_of_word = True
        pointer.data = data
 
    def search(self, player_name):
        pointer = self.root
        player_name = player_name.lower()
        players = []
        for ch in player_name:
            if not ch in ["'", '.', '-', '"', ' '] and not ch.isalpha():
                return []
            index = self.ascii_to_index(ch)
            if not pointer.children[index]:
                return players
            pointer = pointer.children[index]
        
        def search_rec(param):
            if param.data is not None:
                players.append(param.data)
            for child in param.children:
                if child:
                    search_rec(child)

        search_rec(pointer)
        return players


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
    def __init__(self, size: int):
        self.size = size
        self.array = [[] for i in range(self.size)]

    # Horner
    def hashing_function(self, input: str):
        p = 53  # 53 because there's both upper and lowecase
        m = self.size
        p_pow = 1
        hash = 0

        for i in range(len(input)):
            hash = (hash + (ord(input[i]) - ord('a') + 1) * p_pow) % m
            p_pow = (p_pow * p) % m

        return hash

    # Applies the hashing function to the string to get it's position
    # in the array, then inserts it there
    def insert(self, string: str, data):
        index = self.hashing_function(string)
        for item in self.array[index]:
            if item[0] == string:
                item[1].append(data)
                return 
        self.array[index].append((string, [data]))

    # Applies the hashing function to the string to get it's position
    # in the array, then checks if it's actually there
    def find(self, string: str):
        hash = self.hashing_function(string)
        for item in self.array[hash]:
            if item[0] == string:
                return item[1]
        return None
