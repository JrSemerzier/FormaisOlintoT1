# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from model.ER.Arvore.Nodo import Nodo


class NodoFolha(Nodo):

    __numero = None

    def __init__(self, valor):
        super(NodoFolha, self).__init__(valor, folha=True)

    def numera_folha(self, lista):
        self.__numero = len(lista)
        lista.append(self)

    def descer(self, composicao):
        if self.get_valor() not in composicao:
            composicao[self.get_valor()] = set()
        composicao[self.get_valor()].add(self.__numero)
        return composicao

    def subir(self, composicao):
        if self.get_valor() == "$":
            composicao["$"] = set()
            composicao["$"].add(-1)
            return composicao

        composicao = self.get_costura().subir(composicao)
        return composicao
