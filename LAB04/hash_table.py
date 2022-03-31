NAMES_FILE = 'nomes_10000.txt'
SEARCH_FILE = 'consultas.txt'

with open(NAMES_FILE, 'r') as file:
    names = [line[:-1] for line in file]

with open(SEARCH_FILE, 'r') as file:
    to_search = [line[:-1] for line in file]


# Hash table that uses strings as keys
class HashTable:
    def __init__(self, size: int):
        self.size = size
        self.array = [[]] * size

    # Horner
    def hashing_function(self, input: str):
        r_val = 0
        for char in input:
            r_val = (31 * r_val + char) % self.size
        return r_val

    # Applies the hashing function to the string to get it's position
    # in the array, then inserts it there
    def insert(self, string: str):
        pass

    # Applies the hashing function to the string to get it's position
    # in the array, then checks if it's actually there
    def find(self, string: str):
        return 1


Hash_503 = HashTable(503)
Hash_2503 = HashTable(2503)
Hash_5003 = HashTable(5003)
Hash_7507 = HashTable(7507)

# Insertion
for name in names:
    Hash_503.insert(name)
    Hash_2503.insert(name)
    Hash_5003.insert(name)
    Hash_7507.insert(name)

# Searches
accum_searches_503 = 0
accum_searches_2503 = 0
accum_searches_5003 = 0
accum_searches_7507 = 0
max_503 = 0
max_2503 = 0
max_5003 = 0
max_7507 = 0

file_output_503 = []
file_output_2503 = []
file_output_5003 = []
file_output_7507 = []

# Search counting
for name in to_search:
    searches_1 = Hash_503.find(name)
    searches_2 = Hash_2503.find(name)
    searches_3 = Hash_5003.find(name)
    searches_4 = Hash_7507.find(name)

    file_output_503.append(f'{name} {searches_1}')
    file_output_2503.append(f'{name} {searches_2}')
    file_output_5003.append(f'{name} {searches_3}')
    file_output_7507.append(f'{name} {searches_4}')

    accum_searches_503 += searches_1
    accum_searches_2503 += searches_2
    accum_searches_5003 += searches_3
    accum_searches_7507 += searches_4

    max_503 = max(max_503, searches_1)
    max_2503 = max(max_2503, searches_2)
    max_5003 = max(max_5003, searches_3)
    max_7507 = max(max_7507, searches_4)

search_length = len(to_search)
file_output_503.append(f'MEDIA {accum_searches_503 / search_length}\nMAXIMO {max_503}')
file_output_2503.append(f'MEDIA {accum_searches_2503 / search_length}\nMAXIMO {max_2503}')
file_output_5003.append(f'MEDIA {accum_searches_5003 / search_length}\nMAXIMO {max_5003}')
file_output_7507.append(f'MEDIA {accum_searches_7507 / search_length}\nMAXIMO {max_7507}')


# Output to file
with open('experimento503.txt', 'w') as file:
    file.write('\n'.join(file_output_503))

with open('experimento2503.txt', 'w') as file:
    file.write('\n'.join(file_output_2503))

with open('experimento5003.txt', 'w') as file:
    file.write('\n'.join(file_output_5003))

with open('experimento7507.txt', 'w') as file:
    file.write('\n'.join(file_output_7507))


