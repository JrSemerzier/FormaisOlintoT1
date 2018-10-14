# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]


class Nodo:

    __valor = None
    __folha = None
    __prioridade_operador = None
    __filho_esquerdo = None
    __filho_direito = None
    __costura = None

    def __init__(self, valor, prioridade=0, folha=False):
        self.__valor = valor
        self.__prioridade_operador = prioridade
        self.__folha = folha

    def set_valor(self, valor):
        self.__valor = valor

    def get_valor(self):
        return self.__valor

    def eh_folha(self):
        return self.__folha

    def set_filho_esquerdo(self, novo_filho_esquerdo):
        self.__filho_esquerdo = novo_filho_esquerdo

    def get_filho_esquerdo(self):
        return self.__filho_esquerdo

    def set_filho_direito(self, novo_filho_direito):
        self.__filho_direito = novo_filho_direito

    def get_filho_direito(self):
        return self.__filho_direito

    def set_costura(self, nodo_costurado):
        self.__costura = nodo_costurado

    def get_costura(self):
        if self.__costura is not None:
            return self.__costura
        else:
            return self.__filho_direito.get_costura()

    def em_ordem(self, expressao):
        if self.__filho_esquerdo is not None:
            if self.__filho_esquerdo.__prioridade_operador > self.__prioridade_operador:
                expressao += "("
            expressao = self.__filho_esquerdo.em_ordem(expressao)
            if self.__filho_esquerdo.__prioridade_operador > self.__prioridade_operador:
                expressao += ")"
        if self.__valor != ".":
            expressao += self.__valor
        if self.__filho_direito is not None:
            if self.__filho_direito.__prioridade_operador > self.__prioridade_operador:
                expressao += "("
            expressao = self.__filho_direito.em_ordem(expressao)
            if self.__filho_direito.__prioridade_operador > self.__prioridade_operador:
                expressao += ")"
        return expressao

    def costura_nodo(self, stack):
        if self.__filho_esquerdo is not None:
            stack.append(self)
            self.__filho_esquerdo.costura_nodo(stack)
            stack.pop()

        if self.__filho_direito is None:
            self.__costura = stack[-1]
        else:
            self.__filho_direito.costura_nodo(stack)

    def numera_folhas(self, lista):
        if self.__filho_esquerdo is not None:
            self.__filho_esquerdo.numera_folhas(lista)

        self.numera_folha(lista)

        if self.__filho_direito is not None:
            self.__filho_direito.numera_folhas(lista)

    def numera_folha(self, lista):
        pass

    def descer(self, composicao):
        pass

    def subir(self, composicao):
        pass

    def __str__(self):
        return "Nodo(\"" + self.get_valor() + "\")"
