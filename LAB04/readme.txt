A função de hash usada foi a de Horner, implementada usando a propriedade de aritmetica
modular mostradas nos slides (slide 92).
O método de resolução de conflitos utilizados foi o de encadeamento. Para isso, a hash table
usa uma lista de listas para armazenar os valores, de modo que para armazenar um valor em um
índice calculado, chamamos o método append() da lista. Assim, se houver um conflito, este
será posto no fim da lista.