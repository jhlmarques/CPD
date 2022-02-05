from isort import file
import shellsortinput
from typing import List, Optional
from shellsortinput import ShellSortData, TWO_POWER, KNUTH, CIURA
from time import time

# Se fores fazer do jeito que sugeri, só mudar gaps: List[int] para gaps: int
def shell_sort(input: List[int], gap: int, size: int) -> None:
    for i in range(gap, size):
        curr = input[i]
        j = i - gap
        while j >= 0 and input[j] > curr:
            input[j + gap] = input[j]
            j -= gap
        input[j + gap] = curr

# Get data
data1 = ShellSortData('entrada1.txt')
data2 = ShellSortData('entrada2.txt')

while data1.selected_input:
    file_output = []    # O que será posto no arquivo final

    inputs = data1.get_current_input()  # Pega input atual
    arr_size = inputs[0]
    arr = inputs[1:]

    sorts = [TWO_POWER, KNUTH, CIURA]

    for sort in sorts:
        gaps = data1.get_current_gap(sort)
        file_output.append(' '.join(map(str, arr)))
        file_output.append(f' SEQ={str(sort)}\n')
        for h in reversed(gaps):
            shell_sort(arr, h, arr_size)
            file_output.append(' '.join(map(str, arr)))
            file_output.append(f' SEQ={h}\n')

    data1.next_input()  # Próximo input

    #DEBUG SAÍDA ARQUIVO
    output_string = ''.join(file_output)
    print(output_string)
    # with open("saida1.txt", "a") as file1:
    #     file1.write(output_string)

while data2.selected_input:
    file_output = []

    inputs = data2.get_current_input()  # Pega input atual
    arr_size = inputs[0]
    arr = inputs[1:]

    sorts = [TWO_POWER, KNUTH, CIURA]

    for sort in sorts:
        gaps = data2.get_current_gap(sort)
        file_output.append(f'{sort}, {arr_size}, ')
        start = time()
        for h in reversed(gaps):
            shell_sort(arr, h, arr_size)
        total_time = time() - start
        file_output.append(f'{total_time}\n')

    data2.next_input()

    output_string = ''.join(file_output)
    print(output_string)
    # with open("saida2.txt", "a") as file2:
    #     file2.write(output_string)

