# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

import string

from model.Elemento import Elemento
from model.Elemento import TipoElemento
from model.ER.Arvore.Nodos.NodoConcat import NodoConcat
from model.ER.Arvore.Nodos.NodoFecho import NodoFecho
from model.ER.Arvore.Nodos.NodoFolha import NodoFolha
from model.ER.Arvore.Nodos.NodoOpcional import NodoOpcional
from model.ER.Arvore.Nodos.NodoUniao import NodoUniao
from model.ER.Arvore.Arvore import Arvore
from model.ER.Constants import Operacao, prioridade
from model.exception.ExpressionParsingError import ExpressionParsingError

'''
    Classe que representa uma expressão regular.
'''
class Expressao(Elemento):

    __arvore = None

    '''
        Construtor do elemento expressão regular.
        \:param nome é o nome do elemento no sistema.
    '''
    def __init__(self, nome):
        super(Expressao, self).__init__(TipoElemento.ER, nome)

    '''
        Método que recebe a expressão em forma de textual e armazena sua estrutura nesse objeto.
        \:param expressao é a representação textual da expressão regular.
    '''
    def parse(self, expressao):
        self.__gerar_arvore(expressao)

    '''
        Retorna a representação textual da expressão regular.
        \:return a representação textual da expressão regular.
    '''
    def to_string(self):
        return self.__arvore.get_em_ordem()

    '''
        Metodo utilizado para gerar a arvore a partir da representação textual da expressão regular.
        \:param expressao é a representação textual da expressão regular.
    '''
    def __gerar_arvore(self, expressao):
        self.__arvore = Arvore()
        expressao = self.__preparar_expressao(expressao)
        if self.__verifica_validade(expressao):
            self.__arvore.set_nodo_raiz(self.__gerar_nodo(expressao))
            self.__arvore.costura_arvore()
            self.__arvore.numera_folhas()
        try:
            self.__verifica_validade(self.to_string())
        except:
            raise ExpressionParsingError(ExpressionParsingError.EXPRESSION_PARSING_ERROR +
                                         "Expressão possui operadores redundantes que resultam em recursão sem fim.")

    '''
        Algorítmo recursivo que gera a arvore/sub-arvore a partir da expressão/sub-expressão regular dada.

        Ele percorre a expressão encontrando o operador de menor prioridade na expressão atual, criando um nodo na
        arvore para este operador, e então chama recursivamente o algoritmo para gerar as sub-arvores passando como
        parametro a sub-expressão do novo ramo.

        \:param expressao é a representação textual da expressão regular.
        \:return o nodo raíz da árvore obtida a partir da expressão dada.
    '''
    def __gerar_nodo(self, expressao):
        subexpressao = self.__remover_parenteses_externos(expressao)

        if len(subexpressao) == 1:
            return NodoFolha(subexpressao)
        else:
            operador_div = None
            prioridade_div = -1
            posicao_div = None

            parenteses_abertos = 0
            for i in range(0, len(subexpressao)):
                char = subexpressao[i]
                if char == "(":
                    parenteses_abertos += 1
                elif char == ")":
                    parenteses_abertos -= 1
                elif parenteses_abertos == 0:
                    if char == "|" and prioridade_div < 2:
                        operador_div = Operacao.UNIAO
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "." and prioridade_div < 1:
                        operador_div = Operacao.CONCAT
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "*" and prioridade_div < 0:
                        operador_div = Operacao.FECHO
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "?" and prioridade_div < 0:
                        operador_div = Operacao.OPCIONAL
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i

            nodo = None
            if operador_div == Operacao.UNIAO:
                nodo = NodoUniao()
                nodo.set_filho_esquerdo(self.__gerar_nodo(subexpressao[0:posicao_div]))
                nodo.set_filho_direito(self.__gerar_nodo(subexpressao[posicao_div + 1:]))

            elif operador_div == Operacao.CONCAT:
                nodo = NodoConcat()
                nodo.set_filho_esquerdo(self.__gerar_nodo(subexpressao[0:posicao_div]))
                nodo.set_filho_direito(self.__gerar_nodo(subexpressao[posicao_div + 1:]))

            elif operador_div == Operacao.FECHO:
                nodo = NodoFecho()
                nodo.set_filho_esquerdo(self.__gerar_nodo(subexpressao[0:posicao_div]))

            else:  # operadorDiv == Operacao.OPCIONAL:
                nodo = NodoOpcional()
                nodo.set_filho_esquerdo(self.__gerar_nodo(subexpressao[0:posicao_div]))

            return nodo

    '''
        Verifica se uma expressão representada em texto possui apenas caracteres válidos em uma posição válida.
        \:param expressao é a representação textual da expressão regular.
        \:return True caso a expressão seja válida
    '''
    def __verifica_validade(self, expressao):
        if not expressao:
            raise ExpressionParsingError("A expressão não pode ser vazia")
        chars_validos = string.ascii_lowercase + string.digits + "|.*?()"
        nivel_parentesis = 0
        char_anterior = " "
        i_real = 0
        for i in range(0, len(expressao)):
            char = expressao[i]
            if char in chars_validos:
                if i > 1:
                    if char_anterior in "|.(" and char in "|.*?)":
                        raise ExpressionParsingError(ExpressionParsingError.EXPRESSION_PARSING_ERROR +
                                                     "Simbolo não esperado na posição: " + str(i_real))
                    elif char_anterior in "*?" and char in "*?":
                        raise ExpressionParsingError(ExpressionParsingError.EXPRESSION_PARSING_ERROR +
                                                     "Simbolo não esperado na posição: " + str(i_real))

                if char == "(":
                    nivel_parentesis += 1
                elif char == ")":
                    nivel_parentesis -= 1
                    if nivel_parentesis < 0:
                        raise ExpressionParsingError(ExpressionParsingError.EXPRESSION_PARSING_ERROR +
                                                     "Parenteses fechado sem correspondente na posição: " + str(i_real))
                elif char == ".":
                    i_real -= 1
            else:
                raise ExpressionParsingError(ExpressionParsingError.EXPRESSION_PARSING_ERROR +
                                             "Simbolo desconhecido na posição: " + str(i_real))
            char_anterior = char
            i_real += 1

        if nivel_parentesis > 0:
            raise ExpressionParsingError(ExpressionParsingError.EXPRESSION_PARSING_ERROR +
                                         "Parenteses aberto sem correspondente")
        return True

    '''
        Prepara a expressão para o alogorítmo de construção da arvore, eliminando espaços e expondo concatenações
        implicitas.
        \:param expressao é a representação textual da expressão regular.
        \:return a expressão preparada para o algoritmo de geração de arvore.
    '''
    def __preparar_expressao(self, expressao):
        # Remove espaços em branco
        expressao = "".join(expressao.split())
        # Adiciona concatenações implicitas
        expressao = self.__expor_concatenacoes_implicitas(expressao)
        return expressao

    '''
        Expõe concatenações implícitas na expressão regular dada.
        \:param expressao é a representação textual da expressão regular.
        \:return a expressão com suas concatenações implicitas reveladas.
    '''
    def __expor_concatenacoes_implicitas(self, expressao):
        nova_expressao = expressao
        char_anterior = " "
        concats_adicionadas = 0
        for i in range(0, len(expressao)):
            char = expressao[i]
            if (char_anterior.isalnum() or (char_anterior in ")*?")) and (char.isalnum() or char == "("):
                nova_expressao = nova_expressao[:i+concats_adicionadas] + '.' + nova_expressao[i+concats_adicionadas:]
                concats_adicionadas += 1
            char_anterior = char

        return nova_expressao

    '''
        Remove parenteses redundantes nas extremidades de uma expressão.
        \:param expressao é a representação textual da expressão regular.
        \:return a expressão sem parenteses reundantes nas extremidades.
    '''
    def __remover_parenteses_externos(self, expressao):
        parenteses_encontrados = 0
        nivel = 0
        inicio = True
        i = 0
        comprimento_expr = len(expressao)
        while i < comprimento_expr - parenteses_encontrados:
            char = expressao[i]
            if char == "(":
                nivel += 1
                if inicio:
                    parenteses_encontrados = nivel
            else:
                inicio = False
                if char == ")":
                    nivel -= 1
                    parenteses_encontrados = min(parenteses_encontrados, nivel)
            i += 1
        return expressao[parenteses_encontrados:comprimento_expr - parenteses_encontrados]

    '''
        Transforma essa expressão regular em um automato finito através do algoritmo de De Simone.
        \:return o automato finito que representa a mesma linguagem que esta expressão regular.
    '''
    def obter_automato_finito_equivalente(self):
        from model.AF.AutomatoFinito import AutomatoFinito
        from model.AF.Estado import Estado

        folhas = self.__arvore.numera_folhas()

        obter_composicao = {}  # mapeia estados para sua composição
        obter_estado = {}  # mapeia composicoes para seu estado

        prefixo_do_estado = "q"
        i = 0

        estado_inicial = Estado(prefixo_do_estado + str(i))

        automato = AutomatoFinito(self.get_nome() + " (convertido para AF)")
        automato.adiciona_estado(estado_inicial)
        automato.set_estado_inicial(estado_inicial)

        composicao_da_raiz = self.__arvore.composicao_da_raiz()
        obter_composicao[estado_inicial] = composicao_da_raiz
        obter_estado[self.__obter_composicao_como_chave(composicao_da_raiz)] = estado_inicial

        estados_incompletos = [estado_inicial]
        estados_de_aceitacao = []

        i += 1
        while len(estados_incompletos) > 0:
            estado_atual = estados_incompletos.pop(0)
            composicao_atual = obter_composicao[estado_atual]
            for simbolo in composicao_atual:
                if simbolo != "$":
                    novo_estado = Estado(prefixo_do_estado + str(i))
                    i += 1
                    nova_composicao = {}
                    for numero_folha in composicao_atual[simbolo]:
                        folhas[numero_folha].subir(nova_composicao)
                    obter_composicao[novo_estado] = nova_composicao

                    nova_composicao_como_chave = self.__obter_composicao_como_chave(nova_composicao)
                    if nova_composicao_como_chave not in obter_estado:
                        obter_estado[nova_composicao_como_chave] = novo_estado
                        automato.adiciona_estado(novo_estado)
                        estados_incompletos.append(novo_estado)
                    else:
                        novo_estado = obter_estado[nova_composicao_como_chave]

                    automato.adiciona_transicao(estado_atual, simbolo, novo_estado)
                else:
                    estados_de_aceitacao.append(estado_atual)
        automato.set_estados_finais(estados_de_aceitacao)
        return automato

    '''
        Recebe a composição de um estado e a transforma em um valor único imutável para a composição com estes valores.
            Utilizado quando se precisa utilizar a composição de um estado como chave de um dicionário.
        \:param composicao a composição de um estado.
        \:return uma tupla imutável que representa a mesma composição passada por parâmetro.
    '''
    def __obter_composicao_como_chave(self, composicao):
        id_nova_composicao = []
        for simb in composicao:
            par = (simb, tuple(sorted(list(composicao[simb]))))
            id_nova_composicao.append(par)
        return tuple(id_nova_composicao)
