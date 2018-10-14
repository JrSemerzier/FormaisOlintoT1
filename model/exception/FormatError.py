# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

'''
    Classe que representa um erro na formatação da gramática escrita pelo usuário.
'''
class FormatError(Exception):
    FORMAT_ERROR = "A gramática não segue o formato padrão de produções regulares na linha "

    '''
        Método construtor.
    '''
    def __init__(self, message):
        self.__message = "ERRO: " + message

    '''
        Retorna a mensagem de erro.
        \:return a string da mensagem de erro.
    '''
    def get_message(self):
        return self.__message