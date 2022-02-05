import shellsortinput
from typing import List, Optional
from shellsortinput import ShellSortData, TWO_POWER, KNUTH, CIURA


# Se fores fazer do jeito que sugeri, só mudar gaps: List[int] para gaps: int
def shell_sort(input: List[int], gaps: List[int]) -> None:
    pass

# Get data
data1 = ShellSortData('entrada1.txt')
data2 = ShellSortData('entrada2.txt')

while data1.selected_input:
    file_output = []    # O que será posto no arquivo final

    inputs = data1.get_current_input()  # Pega input atual
    gaps = data1.get_current_gap(TWO_POWER) # Pega sequencia para o input atual

    file_output.append(' '.join(map(str, inputs)))
    file_output.append(' SEQ=SHELL\n')

    # WIP - Como pensei em fazer o sort:
    # Shell sort organiza para um h específico; guarda saída (inputs) na lista que será printada
    # no arquivo
    # Acredito que não tem problema fazer desse jeito; vou falar com o prof
    for h in reversed(gaps):
        shell_sort(inputs, h)
        file_output.append(' '.join(map(str, inputs)))
        file_output.append(f' SEQ={h}\n')

    # Knuth
    inputs = data1.get_current_input()
    gaps = data1.get_current_gap(KNUTH)

    # Ciura
    inputs = data1.get_current_input()
    gaps = data1.get_current_gap(CIURA)

    data1.next_input()  # Próximo input

    #DEBUG SAÍDA ARQUIVO
    print(''.join(file_output))

