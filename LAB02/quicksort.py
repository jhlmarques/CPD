import random
import statistics
import time

array1 = [16, 16, 14, 12, 1, 8, 4, 9, 6, 15, 13, 11, 2, 7, 3, 10, 5]
array2 = [16, 3, 10, 5, 16, 14, 12, 1, 8, 4, 9, 6, 15, 13, 11, 2, 7]
swaps = 0
recursions = 0

# chooses a random element as partitioner and moves it to start of array
def randomPartitioner(array):
    newArray = array.copy()
    partitioner =  random.choice(newArray);
    newArray[newArray.index(partitioner)], newArray[0] = newArray[0], newArray[newArray.index(partitioner)]
    return newArray;

# chooses the partitioner based on the median of first, last and middle elements    
def medianPartitioner(array):
    newArray = array.copy()
    first = newArray[0];
    middle = newArray[int(len(newArray)/2)];
    last = newArray[-1];
    partitioner = statistics.median([first, middle, last]);
    newArray[newArray.index(partitioner)], newArray[0] = newArray[0], newArray[newArray.index(partitioner)]
    return newArray;

# quicksort to use with Lomuto's partition
def quickSortLomuto(array, start, end):
    global recursions
    recursions += 1;
    if(start < end):
        # finds pivot position and sorts elements before and after partition
        q = partitionLomuto(array, start, end);
        quickSortLomuto(array, start, q-1);
        quickSortLomuto(array, q+1, end);

# Lomuto's partition strategy
def partitionLomuto(array, start, end):
    global swaps
    pivot = array[end];
    i = start - 1;

    for j in range(start, end):
        if array[j] <= pivot:
            i += 1;
            array[i], array[j] = array[j], array[i]
            swaps += 1;

    array[i+1], array[end] = array[end], array[i+1]
    return (i+1)

# quicksort to use with Hoare's partition
def quickSortHoare(array, start, end):
    global recursions
    recursions += 1;
    if(start < end):
        q = partitionHoare(array, start, end);
        quickSortHoare(array, start, q);
        quickSortHoare(array, q+1, end);

# Hoare's partition strategy
def partitionHoare(array, start, end):
    global swaps;
    pivot = array[start];
    i = start - 1 # left index
    j = end + 1 # right index
    
    while(True):
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
        swaps += 1;

array1.pop(0); # remove array size
arrayWithRandom = randomPartitioner(array1) # creates array with random partitioner at start position
arrayWithMedian = medianPartitioner(array1) # creates array with median partitioner at start position

print('LOMUTO RANDOM: ')
t0 = time.perf_counter()
quickSortLomuto(arrayWithRandom, 0, len(arrayWithRandom)-1)
tf = time.perf_counter() - t0
print(f'time: {tf}, swaps: {swaps}, recursions: {recursions}')

swaps = 0
recursions = 0
print('LOMUTO MEDIAN: ')
t0 = time.perf_counter()
quickSortLomuto(arrayWithMedian, 0, len(arrayWithMedian)-1)
tf = time.perf_counter() - t0
print(f'time: {tf}, swaps: {swaps}, recursions: {recursions}')

arrayWithRandom = randomPartitioner(array1)
arrayWithMedian = medianPartitioner(array1)

swaps = 0
recursions = 0
print('HOARE RANDOM: ')
t0 = time.perf_counter()
quickSortHoare(arrayWithRandom, 0, len(arrayWithRandom)-1)
tf = time.perf_counter() - t0
print(f'time: {tf}, swaps: {swaps}, recursions: {recursions}')

swaps = 0
recursions = 0
print('HOARE MEDIAN: ')
t0 = time.perf_counter()
quickSortHoare(arrayWithMedian, 0, len(arrayWithMedian)-1)
tf = time.perf_counter() - t0
print(f'time: {tf}, swaps: {swaps}, recursions: {recursions}')