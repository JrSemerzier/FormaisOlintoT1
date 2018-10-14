# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from model.ER.Arvore.Nodo import Nodo
from model.ER.Constants import *


class NodoOpcional(Nodo):

    def __init__(self):
        super(NodoOpcional, self).__init__(Operacao.OPCIONAL.value, prioridade=prioridade(Operacao.OPCIONAL))

    def descer(self, composicao):
        composicao = self.get_filho_esquerdo().descer(composicao)
        composicao = self.get_costura().subir(composicao)
        return composicao

    def subir(self, composicao):
        composicao = self.get_costura().subir(composicao)
        return composicao
