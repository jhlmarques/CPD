from sortdata import SortData, NamedTuple, List


# Radix input data
class RadixInput(NamedTuple):
    unsorted_values: List[str]
    greatest_word_length: int


# File parser
class RadixData(SortData):

    @staticmethod
    def create_input_data(raw_line_data: List[str]):
        greatest_word_length = 0
        newlist = []
        for word in raw_line_data:
            length = len(word)
            if length >= 4 and word.isalpha():
                newlist.append(word)
                if length > greatest_word_length:
                    greatest_word_length = length

        return RadixInput(unsorted_values=newlist, greatest_word_length=greatest_word_length)

    def get_greatest_word_length(self):
        return self.inputs[0].greatest_word_length


# Lists of words parsed from the files according to instructions
wap_data = RadixData('war_and_peace_clean.txt')
frank_data = RadixData('frankestein_clean.txt')

war_and_peace = wap_data.get_unsorted_input(0)
radix_max_size1 = wap_data.get_greatest_word_length()
frankenstein = frank_data.get_unsorted_input(0)
radix_max_size2 = frank_data.get_greatest_word_length()


# aux function to get the index of a letter on a range of 0 - 25
def get_index(letter):
    return ord(letter) - 65

def radix(arr, d):
    sorted_list = []

    if(arr):
        aux = [[] for i in range(26)]
        for word in arr:
            if d >= len(word):
                sorted_list.append(word)
            else:
                index = get_index(word[d])
                aux[index].append(word)

        aux = [radix(position, d + 1) for position in aux]

        for position in aux:
            for word in position:
                sorted_list.append(word)

    return sorted_list

# Counts how many times each word appears in the sorted list and output it to a file
def put_in_file(sorted_list: List[str], output_file):
    with open(output_file, 'w') as file:
        length = len(sorted_list)
        i = 0
        while i < length:
            word_count = 1
            word = sorted_list[i]
            # If there are duplicates of this word, they must come after it
            for j in range(i + 1, length):
                if sorted_list[j] == word:
                    i += 1
                    word_count += 1
                else:
                    break
            file.write(f'{word} {word_count}\n')
            i += 1

sorted_wap = radix(war_and_peace, 0)
sorted_frank = radix(frankenstein, 0)

put_in_file(sorted_wap, 'war_and_peace_ordenado.txt')
put_in_file(sorted_frank, 'frankenstein_ordenado.txt')

# Teste da função que põe no arquivo
# test_sorted_input = 'ABACK ABACK ABACK ABACUS ABANDON ABANDON ABANDON ABANDON ABANDON ABANDONED ABANDONING'.split(' ')
# print(test_sorted_input)
# put_in_file(test_sorted_input, 'test.txt')