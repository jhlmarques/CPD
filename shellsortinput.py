from typing import List, Tuple, NamedTuple, Optional

# Constants
TWO_POWER = 'SHELL'
KNUTH = 'KNUTH'
CIURA = 'CIURA'

# Gap sequence caches
gaps_twopower: List[List[int]] = [[1]]
gaps_knuth: List[List[int]] = [[1]]
gaps_ciura: List[List[int]] = [[1], [1, 4], [1, 4, 10], [1, 4, 10, 23],
                               [1, 4, 10, 23, 57], [1, 4, 10, 23, 57, 132],
                               [1, 4, 10, 23, 57, 132, 301], [1, 4, 10, 23, 57, 132, 301, 701]]

# Used to compare an input's size with preexisting gap sequences
twopower_largest_sequence: List[int] = [1]
knuth_largest_sequence = [1]
ciura_largest_sequence = [1, 4, 10, 23, 57, 132, 301, 701]


# Given an input size, tries to find a suitable gap sequence in the cache. Otherwise, generates
# a new one and returns it's index in the cache
def get_gap_indexes(input_size: int) -> Tuple[int, int, int]:

    global twopower_largest_sequence
    global knuth_largest_sequence
    global ciura_largest_sequence

    # Powers of two

    tp_index: int
    tp_last = twopower_largest_sequence[-1]
    # No gap sequence that suits this input size exists yet; generate it
    if input_size > tp_last:
        while tp_last < input_size:
            tp_last = tp_last * 2
            new_sequence = twopower_largest_sequence.copy()
            new_sequence.append(tp_last)
            gaps_twopower.append(new_sequence)
            twopower_largest_sequence = new_sequence
        tp_index = len(gaps_twopower) - 2
    else:
        # Gap sequence exists, so we search for it: It's not very efficient to give the maximum
        # sequence for any input size, so we search for the best fitting sequence
        tp_index = len(gaps_twopower) - 1
        for i in reversed(twopower_largest_sequence):
            if i < input_size:
                break
            else:
                tp_index -= 1

    # Knuth

    kn_index: int
    kn_last = knuth_largest_sequence[-1]
    # No gap sequence that suits this input size exists yet; generate it
    if input_size > kn_last:
        while kn_last < input_size:
            kn_last = kn_last * 3 + 1
            new_sequence = knuth_largest_sequence.copy()
            new_sequence.append(kn_last)
            gaps_knuth.append(new_sequence)
            knuth_largest_sequence = new_sequence
        kn_index = len(gaps_knuth) - 2
    else:
        # Gap sequence exists, so we search for it: It's not very efficient to give the maximum
        # sequence for any input size, so we search for the best fitting sequence
        kn_index = len(gaps_knuth) - 1
        for i in reversed(knuth_largest_sequence):
            if i < input_size:
                break
            else:
                kn_index -= 1

    # Ciura

    cr_index: int
    cr_last = ciura_largest_sequence[-1]
    # No gap sequence that suits this input size exists yet; generate it
    if input_size > cr_last:
        while cr_last < input_size:
            cr_last = int(cr_last * 2.25)
            new_sequence = ciura_largest_sequence.copy()
            new_sequence.append(cr_last)
            gaps_ciura.append(new_sequence)
            ciura_largest_sequence = new_sequence
        cr_index = len(gaps_ciura) - 2
    else:
        # Gap sequence exists, so we search for it: It's not very efficient to give the maximum
        # sequence for any input size, so we search for the best fitting sequence
        cr_index = len(gaps_ciura) - 1
        for i in reversed(ciura_largest_sequence):
            if i < input_size:
                break
            else:
                cr_index -= 1

    return tp_index, kn_index, cr_index


# Data class that holds unsorted values to be fed to shell sort and indexes
# for accessing the gap sequence caches
class ShellSortInput(NamedTuple):
    gap_indexes: Tuple[int, int, int]
    unsorted_values: List[int]


# Holds data from an input file and manages the inputs fed to shell sort
class ShellSortData:

    def __init__(self, input_file: str):

        self.inputs: List[ShellSortInput] = []
        self.iter_inputs = iter(self.inputs)
        self.selected_input: Optional[ShellSortInput] = None

        self.read_input_file(input_file)

    def next_input(self):
        try:
            self.selected_input = next(self.iter_inputs)
        except StopIteration:
            self.selected_input = None

    def read_input_file(self, input_file: str):
        with open(input_file, "r") as file:
            for line in file:
                line_data = line.split(' ')
                self.inputs.append(ShellSortInput(gap_indexes=get_gap_indexes(int(line_data[0])),
                                                  unsorted_values=list(map(int, line_data[0:-1]))))
        self.next_input()

    def get_current_gap(self, sequence_type: str) -> Optional[List[int]]:
        if not self.selected_input:
            return None
        if sequence_type == TWO_POWER:
            return gaps_twopower[self.selected_input.gap_indexes[0]]
        if sequence_type == KNUTH:
            return gaps_knuth[self.selected_input.gap_indexes[1]]
        if sequence_type == CIURA:
            return gaps_ciura[self.selected_input.gap_indexes[2]]

        raise ValueError("Sequence type must be either TWO_POWER, KNUTH or CIURA")

    def get_current_input(self) -> Optional[List[int]]:
        if not self.selected_input:
            return None
        return self.selected_input.unsorted_values.copy()
