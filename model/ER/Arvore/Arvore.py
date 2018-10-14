# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]


from model.ER.Arvore.Nodos.NodoFolha import NodoFolha


class Arvore:

    __nodo_raiz = None
    __folhas = []

    def __init__(self):
        pass

    def set_nodo_raiz(self, novo_nodo_raiz):
        self.__nodo_raiz = novo_nodo_raiz

    def get_nodo_raiz(self):
        return self.__nodo_raiz

    def get_em_ordem(self):
        return self.__nodo_raiz.em_ordem("")

    def costura_arvore(self):
        stack = [NodoFolha("$")]
        self.__nodo_raiz.costura_nodo(stack)
        
    def numera_folhas(self):
        self.__folhas = []
        self.__nodo_raiz.numera_folhas(self.__folhas)
        return self.__folhas

    def composicao_da_raiz(self):
        composicao = {}
        self.__nodo_raiz.descer(composicao)
        return composicao
