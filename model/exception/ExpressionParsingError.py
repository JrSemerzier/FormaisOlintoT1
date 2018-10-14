# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

'''
    Classe que representa um erro na formatação da expressão regular escrita pelo usuário.
'''
class ExpressionParsingError(Exception):

    EXPRESSION_PARSING_ERROR = "A expressão regular não segue o formato padrão:\n"

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