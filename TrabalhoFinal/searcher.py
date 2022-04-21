from data_structures import *
import csv
import time

HASHPLAYERS_SIZE = 1000000
HASHUSERS_SIZE = 1000000
#HASHPOSITIONS_SIZE =
#HASHTAGS_SIZE =


class Searcher:

    def __init__(self):

        self.TriePlayers = Trie()
        self.HashPlayers = HashID(HASHPLAYERS_SIZE)      # player_id -> player_data
        self.HashUsers = HashID(HASHUSERS_SIZE)          # user_id -> user_data
        self.HashPositions = HashString()    # position -> list of players
        self.HashTags = HashString()         # tag -> list of players

        self.t_players = self.build_players()
        self.t_users = self.build_users()
        self.t_tags = self.build_tags()
        print(f'Build time: {self.t_players + self.t_users + self.t_tags}')

    def build_players(self):
        timer = time.perf_counter()
        with open('players.csv', encoding='utf-8') as file:
            csvreader = csv.reader(file)
            next(csvreader)

            for line in csvreader:
                new_data = PlayerData(id=line[0], name=line[1], positions=line[2], ratings=HashString())
                self.TriePlayers.insert(line[1], new_data)
                self.HashPlayers.insert(int(line[0]), new_data)
                # for position in line[2]:
                #     players_in_position = HashPositions.find(position)
                #     if players_in_position is None:
                #         HashPositions.insert(position, new_data)
                #     else:
                #         players_in_position.append(new_data)
        return time.perf_counter() - timer

    def build_users(self):
        replacements = 0
        timer = time.perf_counter()
        with open('rating.csv', encoding='utf-8') as file:
            csvreader = csv.reader(file)
            next(csvreader)

            for line in csvreader:
                user_id = int(line[0])
                rating = float(line[2])

                player = self.HashPlayers.find(int(line[1]))
                player.sum_of_ratings += rating
                player.n_of_ratings += 1

                user = self.HashUsers.find(user_id)
                if user is None:
                    user = UserData(id=user_id)
                    self.HashUsers.insert(user_id, user)

                if user.insert_rating(rating, player):
                    replacements += 1
        print(f'BUILD: Ratings - {replacements} replacements')
        return time.perf_counter() - timer

    def build_tags(self):
        return 0.0

    def find_by_name(self, name):
        pass

    def find_by_user(self, user_id):
        user = self.HashUsers.find(user_id)
        if user is None:
            return None
        return user.player_ratings

    def find_top(self, N, tag):
        pass

    def find_by_tags(self, tags):
        pass