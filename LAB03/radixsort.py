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

'''

Código do RadixSort aqui
Não sei se vais usar, mas as variáveis radix_max_size1 e radix_max_size2
podem servir pra saber por quantos caracteres tem que rodar o radix pra cada um
dos arquivos

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
# test_sorted_input = 'ABACK ABACK ABACK ABACUS ABANDON ABANDON ABANDON ABANDON ABANDON ABANDONED ABANDONING'.split(' ')
# print(test_sorted_input)
# put_in_file(test_sorted_input, 'test.txt')