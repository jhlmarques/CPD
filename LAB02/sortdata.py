from typing import List, NamedTuple


# Base data class for holding input data (not all sorts rely only on a list of numbers, e.g. shell sort)
class SortInput(NamedTuple):
    unsorted_values: List[int]


# Generates relevant data for a sorting algorithm when given a text file
# create_input_data should be overridden to change what data is parsed and/or generated from the input file
# getter methods should be used to access input data (like get_unsorted_input)
class SortData:

    def __init__(self, input_file: str):

        self.inputs: List[SortInput] = []
        self.size = 0
        self.read_input_file(input_file)

    @staticmethod
    def create_input_data(raw_line_data: list[str]):
        return SortInput(unsorted_values=list(map(int, raw_line_data[1:])))

    def read_input_file(self, input_file: str):
        with open(input_file, "r") as file:
            for line in file:
                line_data = line.split(' ')
                if line_data[-1] == '\n':
                    line_data.pop(-1)

                self.inputs.append(self.create_input_data(line_data))
                #print(len(line_data))
                #print(len(self.inputs[-1].unsorted_values))
        self.size = len(self.inputs)

    def get_unsorted_input(self, pos: int) -> List[int]:
        return self.inputs[pos].unsorted_values
