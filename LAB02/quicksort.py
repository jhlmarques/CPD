import random
import statistics
import time
from sortdata import SortData, SortInput
from typing import List, Tuple, NamedTuple

# array1 = [16, 16, 14, 12, 1, 8, 4, 9, 6, 15, 13, 11, 2, 7, 3, 10, 5]
# array2 = [16, 3, 10, 5, 16, 14, 12, 1, 8, 4, 9, 6, 15, 13, 11, 2, 7]
swaps: int
recursions: int

'''

    PARTITIONERS

'''


# chooses a random element as partitioner and moves it to start of array
def randomPartitioner(array):
    newArray = array.copy()
    partitioner = random.choice(newArray)
    newArray[newArray.index(partitioner)], newArray[0] = newArray[0], newArray[newArray.index(partitioner)]
    return newArray


# chooses the partitioner based on the median of first, last and middle elements    
def medianPartitioner(array):
    newArray = array.copy()
    first = newArray[0]
    middle = newArray[int(len(newArray) / 2)]
    last = newArray[-1]
    partitioner = statistics.median([first, middle, last])
    newArray[newArray.index(partitioner)], newArray[0] = newArray[0], newArray[newArray.index(partitioner)]
    return newArray

'''

    QUICKSORT ALGORITHMS

'''


# quicksort to use with Lomuto's partition
def quickSortLomuto(array, start, end):
    global recursions
    recursions += 1
    if (start < end):
        # finds pivot position and sorts elements before and after partition
        q = partitionLomuto(array, start, end)
        quickSortLomuto(array, start, q - 1)
        quickSortLomuto(array, q + 1, end)


# Lomuto's partition strategy
def partitionLomuto(array, start, end):
    global swaps
    pivot = array[end]
    i = start - 1

    for j in range(start, end):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
            swaps += 1

    array[i + 1], array[end] = array[end], array[i + 1]
    return (i + 1)


# quicksort to use with Hoare's partition
def quickSortHoare(array, start, end):
    global recursions
    recursions += 1
    if (start < end):
        q = partitionHoare(array, start, end)
        quickSortHoare(array, start, q)
        quickSortHoare(array, q + 1, end)


# Hoare's partition strategy
def partitionHoare(array, start, end):
    global swaps
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
        swaps += 1


'''

    QUICKSORT DATA

'''


class QuickSortData(SortData):
    def get_unsorted_input(self, pos: int) -> Tuple[List[int], List[int]]:
        return medianPartitioner(self.inputs[pos].unsorted_values), \
               randomPartitioner(self.inputs[pos].unsorted_values)

'''

    STATS

'''


class SortStats(NamedTuple):
    size: int
    swaps: int
    recursions: int
    time: float



QS_data = QuickSortData('entrada-quicksort.txt')
stats_lomuto_median = []
stats_lomuto_random = []
stats_hoare_median = []
stats_hoare_random = []

for i in range(0, QS_data.size):
    median_unsorted1, random_unsorted1 = QS_data.get_unsorted_input(i)
    median_unsorted2, random_unsorted2 = median_unsorted1.copy(), random_unsorted1.copy()
    input_size = len(median_unsorted1)

    print(f"--------LINE {i}--------")

    # LOMUTO -- RANDOM
    recursions = 0
    swaps = 0
    print('LOMUTO RANDOM: ')
    t0 = time.perf_counter()
    quickSortLomuto(random_unsorted1, 0, len(random_unsorted1) - 1)
    tf = time.perf_counter() - t0
    print(f'\ttime: {tf}, swaps: {swaps}, recursions: {recursions}')
    stats_lomuto_random.append(SortStats(swaps=swaps, recursions=recursions, time=tf, size=input_size))

    # LOMUTO -- MEDIAN
    swaps = 0
    recursions = 0
    print('LOMUTO MEDIAN: ')
    t0 = time.perf_counter()
    quickSortLomuto(median_unsorted1, 0, len(median_unsorted1) - 1)
    tf = time.perf_counter() - t0
    print(f'\ttime: {tf}, swaps: {swaps}, recursions: {recursions}')
    stats_lomuto_median.append(SortStats(swaps=swaps, recursions=recursions, time=tf, size=input_size))

    # HOARE -- RANDOM
    swaps = 0
    recursions = 0
    print('HOARE RANDOM: ')
    t0 = time.perf_counter()
    quickSortHoare(random_unsorted2, 0, len(random_unsorted2) - 1)
    tf = time.perf_counter() - t0
    print(f'\ttime: {tf}, swaps: {swaps}, recursions: {recursions}')
    stats_hoare_random.append(SortStats(swaps=swaps, recursions=recursions, time=tf, size=input_size))

    # HOARE -- MEDIAN
    swaps = 0
    recursions = 0
    print('HOARE MEDIAN: ')
    t0 = time.perf_counter()
    quickSortHoare(median_unsorted2, 0, len(median_unsorted2) - 1)
    tf = time.perf_counter() - t0
    print(f'\ttime: {tf}, swaps: {swaps}, recursions: {recursions}')
    stats_hoare_median.append(SortStats(swaps=swaps, recursions=recursions, time=tf, size=input_size))

with open("stats-mediana-hoare.txt", 'w') as file:
    for stat in stats_hoare_median:
        file.write(f'TAMANHO ENTRADA {stat.size}\nSWAPS {stat.swaps}\nRECURSOES {stat.recursions}\nTEMPO {stat.time}\n')

with open("stats-mediana-lomuto.txt", 'w') as file:
    for stat in stats_lomuto_median:
        file.write(f'TAMANHO ENTRADA {stat.size}\nSWAPS {stat.swaps}\nRECURSOES {stat.recursions}\nTEMPO {stat.time}\n')

with open("stats-aleatorio-hoare.txt", 'w') as file:
    for stat in stats_hoare_random:
        file.write(f'TAMANHO ENTRADA {stat.size}\nSWAPS {stat.swaps}\nRECURSOES {stat.recursions}\nTEMPO {stat.time}\n')

with open("stats-aleatorio-lomuto.txt", 'w') as file:
    for stat in stats_lomuto_random:
        file.write(f'TAMANHO ENTRADA {stat.size}\nSWAPS {stat.swaps}\nRECURSOES {stat.recursions}\nTEMPO {stat.time}\n')

