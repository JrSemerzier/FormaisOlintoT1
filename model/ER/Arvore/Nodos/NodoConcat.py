# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from model.ER.Arvore.Nodo import Nodo
from model.ER.Constants import *


class NodoConcat(Nodo):

    def __init__(self):
        super(NodoConcat, self).__init__(Operacao.CONCAT.value, prioridade=prioridade(Operacao.CONCAT))

    def descer(self, composicao):
        composicao = self.get_filho_esquerdo().descer(composicao)
        return composicao

    def subir(self, composicao):
        composicao = self.get_filho_direito().descer(composicao)
        return composicao
