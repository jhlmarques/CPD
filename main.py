from isort import file
from typing import List, Optional
from shellsortinput import ShellSortData, TWO_POWER, KNUTH, CIURA
from time import perf_counter


# Inserção direta com incremento (gap)
def shell_sort(input: List[int], gap: int, size: int) -> None:
    for i in range(gap, size):
        curr = input[i]
        j = i - gap
        while j >= 0 and input[j] > curr:
            input[j + gap] = input[j]
            j -= gap
        input[j + gap] = curr


# Pega dados
data1 = ShellSortData('entrada1.txt')
data2 = ShellSortData('entrada2.txt')

file_output = []    # O que será posto no arquivo final
while data1.selected_input:

    input_size = data1.selected_input_size

    sorts = [TWO_POWER, KNUTH, CIURA]

    for sort in sorts:
        inputs = data1.get_current_input()  # Pega input atual
        gaps = data1.get_current_gap(sort)
        file_output.append(' '.join(map(str, inputs)))
        file_output.append(f' SEQ={str(sort)}\n')
        for h in reversed(gaps):
            shell_sort(inputs, h, input_size)
            file_output.append(' '.join(map(str, inputs)))
            file_output.append(f' SEQ={h}\n')

    data1.next_input()  # Próximo input

with open("saida1.txt", "w") as file1:
    file1.truncate(0)
    file1.write(''.join(file_output))

file_output = []
while data2.selected_input:

    input_size = data2.selected_input_size

    sorts = [TWO_POWER, KNUTH, CIURA]
    print(f"Cronometrando input de {input_size} elementos")
    for sort in sorts:
        print(f"Sequência: {sort} =", end=' ')
        inputs = data2.get_current_input()  # Pega input atual
        gaps = data2.get_current_gap(sort)
        file_output.append(f'{sort}, {input_size}, ')
        start = perf_counter()
        for h in reversed(gaps):
            shell_sort(inputs, h, input_size)
        total_time = perf_counter() - start
        print(f"{total_time} segundos")
        file_output.append(f'{total_time}\n')
    print('\n')

    data2.next_input()

with open("saida2.txt", "w") as file1:
    file1.truncate(0)
    file1.write(''.join(file_output))
