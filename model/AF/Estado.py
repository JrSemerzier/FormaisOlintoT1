# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

'''
    Classe que representa um estado de um autômato finito.
'''
class Estado:

    '''
        Método construtor.
        \:param nomes é uma lista com o nome dos estados que representam este estado.
    '''
    def __init__(self, nomes):
        if isinstance(nomes, list):
            self.__lista = sorted(nomes, key=str.lower)
            self.__string = ''.join(self.__lista)
            self.__nome = frozenset(nomes)
            self.__string_com_virgula = ','.join(self.__lista)
            self.__string_display = "[" + ','.join(self.__lista) + "]"
        else:
            self.__lista = []
            self.__lista.append(nomes)
            self.__string = nomes
            self.__nome = frozenset([nomes])
            self.__string_com_virgula = ','.join(self.__lista)
            self.__string_display = nomes

    '''
        Retorna o estado em formato de lista.
        \:return uma lista com a composição do estado.
    '''
    def to_list(self):
        return self.__lista

    '''
        Retorna o estado em formato de texto.
        \:return uma string com a composição do estado.
    '''
    def to_string(self):
        return self.__string

    '''
        Retorna o estado em formato de texto, com os estados que compoem este estado separados por vírgula.
        \:return uma string com a composição do estado.
    '''
    def to_string_com_virgula(self):
        return self.__string_com_virgula

    '''
        Retorna o estado em formato de texto, com os estados que compoem este estado dispostos em forma de uma string pronta para exibição.
        \:return uma string com a composição do estado para exibição.
    '''
    def to_string_display(self):
        return self.__string_display

    '''
        Retorna o estado em formato de conjunto.
        \:return um frozenset com a composição do estado.
    '''
    def get_nome(self):
        return self.__nome

    def __hash__(self):
        return hash(self.__nome)

    def __eq__(self, other):
        return self.__nome.__hash__() == other.get_nome().__hash__()

    def __str__(self):
        return "Estado(\"" + self.to_string_display() + "\")"
