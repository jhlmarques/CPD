from sortdata import SortData, List

# File parser
class RadixData(SortData):

    @staticmethod
    def create_input_data(raw_line_data: List[str]):
        removed_words = 0
        for i, word in enumerate(raw_line_data):
            if len(word) < 4 or not word.isalpha():
                #print(f'Removed word: {word}')
                raw_line_data.pop(i - removed_words)
                removed_words += 1


# Lists of words parsed from the files according to instructions
war_and_peace = RadixData('war_and_peace_clean.txt').get_unsorted_input(0)
frankenstein = RadixData('frankestein_clean.txt').get_unsorted_input(0)

'''

Código do RadixSort aqui

'''

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

'''
Descomentar quando radix estiver pronto e tiver ordenado as listas

put_in_file(war_and_peace, 'war_and_peace_ordenado.txt')
put_in_file(frankenstein, 'frankenstein_ordenado.txt')


'''
# Teste da função que põe no arquivo
#test_sorted_input = 'ABACK ABACK ABACK ABACUS ABANDON ABANDON ABANDON ABANDON ABANDON ABANDONED ABANDONING'.split(' ')
#print(test_sorted_input)
#put_in_file(test_sorted_input, 'test.txt')

