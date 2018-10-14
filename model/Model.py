# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from model.Elemento import *
from model.ListaElementos import ListaElementos
from model.ER.Expressao import Expressao
from model.Gramatica import Gramatica
from model.FileManager.FileManager import FileManager

from copy import deepcopy


'''
    Fachada do módulo model.
'''
class Model:

    __lista_de_elementos = None
    __file_manager = None

    def __init__(self):
        self.__lista_de_elementos = ListaElementos()
        self.__file_manager = FileManager()

    def adicionar_elemento_na_lista(self, elemento):
        self.__lista_de_elementos.adiciona_elemento(elemento)

    '''
        Método que recebe um nome e a entrada de uma gramática e o retorna.
        \:param nome é o nome da gramática que será criada.
        \:param entrada é a representação textual da gramática.
    '''
    def criar_gramatica(self, nome, entrada):
        gr = Gramatica(nome)
        gr.parse(entrada)
        return gr

    '''
        Método que recebe um nome e a entrada de uma expressão e o retorna.
        \:param nome é o nome da expressão que será criada.
        \:param entrada é a representação textual da expressão.
    '''
    def criar_expressao(self, nome, entrada):
        er = Expressao(nome)
        er.parse(entrada)
        return er

    '''
        Método que recebe um índice e remove esse objeto da lista.
        \:param indice é o índice do elemento na lista.
    '''
    def remover_elemento(self, indice):
        self.__lista_de_elementos.remove_elemento(indice)

    '''
        Obtém uma cópia do elemento indicado.
        \:param indice é o índice do elemento na lista.
        \:return uma cópia do elemento requisitado.
    '''
    def duplicar(self, indice):
        elemento = self.obter_elemento_por_indice(indice)
        copia = deepcopy(elemento)
        copia.set_nome(copia.get_nome() + " (cópia)")
        return copia

    '''
        Transforma um elemento em uma gramática.
        \:param indice é o índice do elemento na lista.
        \:return a gramática regular que reconhece a mesma linguagem que o elemento original gerava.
    '''
    def transformar_elemento_em_gr(self, indice):
        elemento = self.obter_elemento_por_indice(indice)
        tipo = elemento.get_tipo()
        if tipo == TipoElemento.AF:
            gr_resultante = elemento.transforma_em_GR()
            return [gr_resultante]
        elif tipo == TipoElemento.ER:
            af_intermediario = elemento.obter_automato_finito_equivalente()
            gr_resultante = af_intermediario.transforma_em_GR()
            return [af_intermediario, gr_resultante]

    '''
        Transforma um elemento em um autômato finito.
        \:param indice é o índice do elemento na lista.
        \:return o autômato finito que reconhece a mesma linguagem que o elemento original gerava.
    '''
    def transformar_elemento_em_af(self, indice):
        elemento = self.obter_elemento_por_indice(indice)
        tipo = elemento.get_tipo()
        if tipo == TipoElemento.GR:
            af_resultante = elemento.transformar_em_AF()
            return af_resultante
        elif tipo == TipoElemento.ER:
            af_resultante = elemento.obter_automato_finito_equivalente()
            return af_resultante

    def operacao_elementos(self, indice_um, indice_dois, operacao):
        elementos_gerados = []

        elemento_um = self.obter_elemento_por_indice(indice_um)
        elemento_op_um = elemento_um
        if elemento_um.get_tipo() is not TipoElemento.AF:
            elemento_op_um = self.transformar_elemento_em_af(indice_um)
            elementos_gerados.append(elemento_op_um)
            if elemento_op_um.isAFND():
                elemento_op_um = elemento_op_um.determiniza()
                elementos_gerados.append(elemento_op_um)

        elemento_op_dois = None
        if operacao < 3:
            elemento_dois = self.obter_elemento_por_indice(indice_dois)
            elemento_op_dois = elemento_dois
            if elemento_dois.get_tipo() is not TipoElemento.AF:
                elemento_op_dois = self.transformar_elemento_em_af(indice_dois)
                elementos_gerados.append(elemento_op_dois)
                if elemento_op_dois.isAFND():
                    elemento_op_dois = elemento_op_dois.determiniza()
                    elementos_gerados.append(elemento_op_dois)

        if operacao == 0:  # União
            elementos_gerados.append(elemento_op_um.uniao(elemento_op_dois))
        elif operacao == 1:  # Intersecção
            elementos_gerados.extend(elemento_op_um.interseccao(elemento_op_dois))
        elif operacao == 2:  # Diferenca
            elementos_gerados.extend(elemento_op_um.diferenca(elemento_op_dois))
        elif operacao == 3:  # Reverso
            elementos_gerados.append(elemento_op_um.reverso())
        else:  # Complemento
            if elemento_op_um.is_complete():
                elementos_gerados.append(elemento_op_um.complemento())
            else:
                af_completa = elemento_op_um.completar()
                elementos_gerados.append(af_completa)
                elementos_gerados.append(af_completa.complemento())

        return elementos_gerados

    def operacao_gr(self, indice_um, indice_dois, operacao):
        gramatica_um = self.obter_elemento_por_indice(indice_um)
        gramatica_dois = None
        if operacao != 2:
            gramatica_dois = self.obter_elemento_por_indice(indice_dois)

        if operacao == 0:  # União
            gramatica_resultante = gramatica_um.uniao(gramatica_dois)
        elif operacao == 1:  # Concatenação
            gramatica_resultante = gramatica_um.concatenacao(gramatica_dois)
        else:  # Fecho
            gramatica_resultante = gramatica_um.fechamento()

        return gramatica_resultante

    '''
        Obtem um automato equivalente determinístico.
        \:param indice é o índice do autômato na lista.
        \:return o autômato finito determinizado.
    '''
    def determiniza_af(self, indice):
        elemento = self.obter_elemento_por_indice(indice)
        return elemento.determiniza()

    '''
        Obtem um automato equivalente minimo.
        \:param indice é o índice do autômato na lista.
        \:return o autômato finito minimizado.
    '''
    def minimiza_af(self, indice):
        elemento = self.obter_elemento_por_indice(indice)
        if elemento.isAFND():
            raise Exception("É preciso que o autômato seja determinístico.")
        return elemento.minimiza()

    '''
        Informa se dada sentença é reconhecida por um autômato especificado.
        \:param indice é o índice do autômato na lista.
        \:param sentenca é a sentença que será reconhecida.
        \:return True se a sentença for aceita, False caso contrário.
    '''
    def reconhecimento(self, indice, sentenca):
        elemento = self.obter_elemento_por_indice(indice)
        return elemento.reconhece_sentenca(sentenca)

    '''
        Obtem as sentenças de um autoômato finito com determinado tamanho.
        \:param indice é o índice do autômato na lista.
        \:param tamanho é o tamanho das sentenças que serão enumeradas.
        \:return as sentenças geradas.
    '''
    def enumeracao(self, indice, tamanho):
        tamanho = int(tamanho)
        elemento = self.obter_elemento_por_indice(indice)
        sentencas = elemento.enumera_sentencas(tamanho)
        return sentencas

    '''
        Obtem o elemento correspondente ao indice passado.
        \:param indice é o índice do elemento na lista.
        \:return o elemento naquele indice.
    '''
    def obter_elemento_por_indice(self, indice):
        return self.__lista_de_elementos.get_elemento(indice)

    def salvar_elemento(self, caminho, indice):
        if indice is not None:
            elemento = self.obter_elemento_por_indice(indice)
            if elemento.get_tipo() is not TipoElemento.AF:
                try:
                    self.__file_manager.salvar(caminho, elemento.to_string())
                    return True
                except:
                    return False
            else:
                return False
        else:
            return False

    def carregar_elemento(self, caminho):
        return self.__file_manager.abrir(caminho)

    def nome_arquivo(self, caminho):
        return self.__file_manager.nome_do_arquivo(caminho)

    def reposiciona_elemento_editado(self, indice):
        self.__lista_de_elementos.reposiciona_elemento_editado(indice)