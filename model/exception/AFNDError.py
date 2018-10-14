# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

'''
    Classe que representa um erro ao usar um método para AFD em um AFND.
'''
class AFNDError(Exception):
    IS_AFND = "ERRO: Determinize o autômato antes de fazer a operação de "

    '''
        Método construtor.
        \:param message é a operação que causou o erro.
    '''
    def __init__(self, message):
        self.__message = self.IS_AFND + message

    '''
        Retorna a mensagem de erro.
        \:return a string da mensagem de erro.
    '''
    def get_message(self):
        return self.__message