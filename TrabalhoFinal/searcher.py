from re import M
from data_structures import *
import random
import csv
import time
import os

HASHPLAYERS_SIZE = 1000000
HASHUSERS_SIZE = 1000000
HASHPOSITIONS_SIZE = 100
HASHTAGS_SIZE = 1000

PLAYERS_FILE = 'players.csv'
RATINGS_FILE = 'rating.csv'
TAGS_FILE = 'tags.csv'


class Searcher:

    def __init__(self):

        self.n_of_players = 0

        self.TriePlayers = Trie()
        self.HashPlayers = HashID(HASHPLAYERS_SIZE)      # player_id -> player_data
        self.HashUsers = HashID(HASHUSERS_SIZE)          # user_id -> user_data
        self.HashPositions = HashString(HASHPOSITIONS_SIZE)    # position -> list of players
        self.HashTags = HashString(HASHTAGS_SIZE)         # tag -> list of players

        print('Building data structures...')
        self.t_players = self.build_players()
        self.t_users = self.build_users()
        self.t_tags = self.build_tags()
        self.t_sorts = self.build_sorts()
        print(f'Build time: {self.t_players + self.t_users + self.t_tags + self.t_sorts}')

    def build_players(self):
        timer = time.perf_counter()
        with open(os.path.join(os.path.dirname(__file__), PLAYERS_FILE), encoding='utf-8') as file:
            csvreader = csv.reader(file)
            next(csvreader)

            for line in csvreader:
                self.n_of_players += 1
                new_data = PlayerData(id=line[0], name=line[1], positions=line[2].split(', '), tags=HashString(1))
                self.TriePlayers.insert(line[1], new_data)
                self.HashPlayers.insert(int(line[0]), new_data)
                for position in line[2].split(', '):
                    self.HashPositions.insert(position, new_data)
        return time.perf_counter() - timer

    def build_users(self):
        replacements = 0
        timer = time.perf_counter()

        # Cacheing the player and user can reduce the number of table acesses
        cache_player = None
        cache_player_id = -1
        cache_user = None
        cache_user_id = -1
        cache_user_n_of_ratings = -1    
        cache_user_lowest_rating = -1
        cache_user_reached_limit = False

        with open(os.path.join(os.path.dirname(__file__), RATINGS_FILE), encoding='utf-8') as file:
            csvreader = csv.reader(file)
            next(csvreader)

            for line in csvreader:
                user_id = int(line[0])
                player_id = int(line[1])
                rating = float(line[2])

                # Try to update cache
                if user_id != cache_user_id:
                    cache_user = self.HashUsers.find(user_id)
                    # Create user data if it doesn't exist yet
                    if cache_user is None:
                        cache_user = UserData(id=user_id)
                        self.HashUsers.insert(user_id, cache_user)
                        cache_user_n_of_ratings = 0
                        cache_user_reached_limit = False
                    else:
                        cache_user_lowest_rating = cache_user.player_ratings[-1][0]
                        cache_user_n_of_ratings = len(cache_user.player_ratings)
                        cache_user_reached_limit = (cache_user_n_of_ratings == 20)

                    cache_user_id = user_id

                if player_id != cache_player_id:
                    cache_player = self.HashPlayers.find(player_id)
                    cache_player_id = player_id

                # Update the player's ratings sum and count
                cache_player.sum_of_ratings += rating
                cache_player.n_of_ratings += 1
                cache_player.average = cache_player.sum_of_ratings / cache_player.n_of_ratings

                # Try to add this player to the user's top 20 list
                if cache_user_reached_limit:
                    if cache_user_lowest_rating < rating:
                        cache_user.insert_rating(rating, cache_player, True) # Remove last element and insert
                        cache_user_lowest_rating = cache_user.player_ratings[-1][0]  # Update lowest rating
                else:
                    cache_user.insert_rating(rating, cache_player)  # Insert without removing any elements
                    cache_user_lowest_rating = cache_user.player_ratings[-1][0]  # Update lowest rating
                    cache_user_n_of_ratings += 1
                    cache_user_reached_limit = (cache_user_n_of_ratings < 20)

        return time.perf_counter() - timer

    def build_tags(self):
        timer = time.perf_counter()
        with open(os.path.join(os.path.dirname(__file__), TAGS_FILE), encoding='utf-8') as file:
            csvreader = csv.reader(file)
            next(csvreader)

            for line in csvreader:
                player_id = int(line[1])
                player_tag = line[2]
                player_data = self.HashPlayers.find(player_id)
                
                if player_data.tags.find(player_tag) is None:
                    player_data.tags.insert(player_tag, 0)
                    self.HashTags.insert(player_tag, player_data)
                    
        return time.perf_counter() - timer

    def build_sorts(self):
        timer = time.perf_counter()
        
        # Sort the positions array
        for col_list in self.HashPositions.array:
            for values in col_list:
                randomPartitioner(values[1])
                quickSortHoare(values[1], 0, len(values[1]) - 1)

        return time.perf_counter() - timer


    def find_by_name(self, name):
        name = self.TriePlayers.search(name)
        return name

    def find_by_user(self, user_id):
        user = self.HashUsers.find(user_id)
        if user is None:
            return None
        return user.player_ratings

    def find_top(self, N, position):
        r_list = []
        found = 0
        players_ordered = self.HashPositions.find(position)
        if players_ordered is None:
            return []

        for player in reversed(players_ordered):
            if player.n_of_ratings < 1000:
                continue
            
            r_list.append(player)
            found += 1

            if found == N:
                break

        return r_list

    def find_by_tags(self, tags):
        tag = tags[0]
        possible_players = self.HashTags.find(tag)

        if possible_players is None:
            return []

        if len(tags) == 1:
            found_players = possible_players
        else:
            found_players = []
            for player in possible_players:
                readable = True
                for tag in tags[1:]:
                    if player.tags.find(tag) is None:
                        readable = False
                        break
                if readable:
                    found_players.append(player)
        return found_players


# chooses a random element as partitioner and moves it to start of array
def randomPartitioner(array):
    partitioner = random.choice(array)
    array[array.index(partitioner)], array[0] = array[0], array[array.index(partitioner)]

# quicksort to use with Hoare's partition
def quickSortHoare(array, start, end):
    if (start < end):
        q = partitionHoare(array, start, end)
        quickSortHoare(array, start, q)
        quickSortHoare(array, q + 1, end)


# Hoare's partition strategy
def partitionHoare(array, start, end):
    pivot = array[start]
    i = start - 1  # left index
    j = end + 1  # right index

    while (True):
        # find element on the left that's greater than or equal to pivot
        i += 1
        while (array[i] < pivot):
            i += 1
        # find element on the right that's smaller than or equal to pivot
        j -= 1
        while (array[j] > pivot):
            j -= 1
        # return if indexes meet
        if (i >= j):
            return j

        # swaps elements on right and left
        array[i], array[j] = array[j], array[i]
