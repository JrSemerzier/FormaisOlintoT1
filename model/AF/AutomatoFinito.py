# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from itertools import product
from model.AF.Estado import Estado
from string import ascii_uppercase
from model.exception.AFNDError import AFNDError
from model.Elemento import *

'''
    Classe que representa um autômato finito.
'''
class AutomatoFinito(Elemento):

    '''
        Método construtor.
    '''
    def __init__(self, nome, determinizado = False):
        super(AutomatoFinito, self).__init__(TipoElemento.AF, nome)
        self.__producoes = {} # conjunto de transições
        self.__estado_inicial = None
        self.__estados_finais = set()
        self.__vt = set() # conjunto de símbolos terminais
        self.__determinizado = determinizado
        if determinizado:
            self.__deterministico = True
        else:
            self.__deterministico = None
        self.__completo = None

    '''
        Adiciona uma nova produção para um estado a partir de um simbolo terminal.
        \:param estado é um símbolo não-terminal (ou um conjunto deles).
        \:param caractere é um simbolo terminal.
        \:param destino é um simbolo não-terminal (ou um conjunto deles).s
    '''
    def adiciona_transicao(self, estado, caractere, destino):
        self.__vt.add(caractere)
        self.__producoes.setdefault(estado, {})
        self.__producoes[estado].setdefault(caractere, [])
        self.__producoes[estado][caractere].append(destino)

    '''
        Adiciona uma novo estado.
        \:param estado é um símbolo não-terminal (ou um conjunto deles).
    '''
    def adiciona_estado(self, estado):
        self.__producoes.setdefault(estado, {})

    '''
        Retorna o conjunto de transições do autômato.
        \:return um dicionário onde a chave é um estado e os dados são 
            um dicionário onde a chave é um símbolo não terminal e os dados são um conjunto de símbolos não-terminais (pode ser vazio).
    '''
    def get_producoes(self):
        return self.__producoes

    '''
        Modifica o estado inicial do autômato.
        \:param estado é o novo estado inicial.
    '''
    def set_estado_inicial(self, estado):
        self.__estado_inicial = estado

    '''
        Retorna o estado inicial do autômato.
        \:return o estado inicial.
    '''
    def get_estado_inicial(self):
        return self.__estado_inicial

    '''
        Modifica o conjunto de estados finais do autômato.
        \:param lista é a lista de novos estados finais.
    '''
    def set_estados_finais(self, lista):
        self.__estados_finais = set(lista)

    '''
        Retorna os estados finais do autômato.
        \:return os estados finais.
    '''
    def get_estados_finais(self):
        return self.__estados_finais

    '''
        Modifica o conjunto de símbolos terminais do autômato.
        \:param vt é o novo conjunto de símbolos terminais.
    '''
    def set_vt(self, vt):
        self.__vt = vt

    '''
        Retorna o conjunto de símbolos terminais do autômato.
        \:return o conjunto de símbolos terminais do autômato.
    '''
    def get_vt(self):
        return self.__vt

    '''
        Transforma um autômato finito em uma gramática.
        \:return a gramática que gera a mesma linguagem que o autômato reconhece.
    '''
    def transforma_em_GR(self):
        from model.Gramatica import Gramatica

        gramatica = Gramatica(self.get_nome() + " (convertido para GR)")
        gramatica.set_vt(self.__vt)

        traducao_nomes = {}
        novos_nomes = []
        # Construção das produções de acordo com os itens A e B do algoritmo visto em aula
        for b in self.__producoes.keys():
            producoes_af = self.__producoes[b]
            producoes_g = []
            for a in producoes_af.keys():
                if a != "&":
                    for c in producoes_af[a]:
                        c_string = c.to_string()
                        if c_string != "-":
                            if c_string[0] == "q":
                                if c_string not in traducao_nomes:
                                    novo_nome = self.novo_estado(novos_nomes).to_string()
                                    novos_nomes.append(novo_nome)
                                    traducao_nomes[c_string] = novo_nome
                                    c_string = novo_nome
                                else:
                                    c_string = traducao_nomes[c_string]
                            producoes_g.append((a, c_string))
                            if c in self.__estados_finais:
                                producoes_g.append((a, "&"))
            b = b.to_string()
            if b[0] == "q":
                if b not in traducao_nomes:
                    novo_nome = self.novo_estado(novos_nomes).to_string()
                    novos_nomes.append(novo_nome)
                    traducao_nomes[b] = novo_nome
                    b = novo_nome
                else:
                    b = traducao_nomes[b]
            gramatica.adiciona_producao(b, producoes_g)

        si = self.__estado_inicial.to_string()
        if si[0] == "q":
            gramatica.set_simbolo_inicial(traducao_nomes[si])
        else:
            gramatica.set_simbolo_inicial(si)

        # Item C do algoritmo visto em aula
        # Se & pertence à linguagem
        if self.__estado_inicial in self.__estados_finais:
            simbolo_novo = gramatica.novo_simbolo()

            # Copia produções do estado inicial atual
            producoes_novo_si = [] # lista de tuplas

            if si[0] == "q":
                si = traducao_nomes[si]
            producoes_si = gramatica.get_producoes()[si]
            for p in producoes_si:
                producoes_novo_si.append(p)

            # Adiciona produção de & para o novo símbolo inicial
            producoes_novo_si.append(("&", "&"))

            gramatica.adiciona_producao(simbolo_novo, producoes_novo_si)
            # Atualiza o símbolo inicial
            gramatica.set_simbolo_inicial(simbolo_novo)
        return gramatica

    '''
        Verifica se a sentença dada pertence à linguagem reconhecida pelo AFD.
        \:param sentenca é a sentença a ser verificada.
        \:return True se a sentença é reconhecida pelo autômato e False caso contrário.
    '''
    def reconhece_sentenca(self, sentenca):

        if not self.isAFND():
            index = 0
            estados = self.__producoes[self.__estado_inicial]
            tamanho_sentenca = len(sentenca)

            if tamanho_sentenca == 0 or (tamanho_sentenca == 1 and sentenca[0] == "&"):
                if self.__estado_inicial in self.__estados_finais:
                    return True

            while index < tamanho_sentenca:
                simbolo = sentenca[index]
                transicoes = []
                if "&" in estados:
                    for t in estados["&"]:
                        if t.to_string() != "&":
                            transicoes.append(t)
                if (simbolo in estados):
                    for x in estados[simbolo]:
                        transicoes.append(x)
                    if index == tamanho_sentenca-1:
                        for t in transicoes:
                            if t in self.__estados_finais:
                                return True
                    index = index + 1
                else:
                    if len(transicoes) == 0:
                        return False
                # Copia produções dos próximos estados
                estados = {}
                for t in transicoes:
                    for x in self.__producoes[t]:
                        estados.setdefault(x, [])
                        for y in self.__producoes[t][x]:
                            estados[x].append(y)
            return False
        else:
            raise AFNDError("reconhecimento de sentença.")

    '''
        Retorna todas as sentenças reconhecidas pelo autômato do tamanho indicado pelo parâmetro.
        \:param tamanho é o tamanho das sentenças reconhecidas.
        \:return uma lista de strings com as sentenças reconhecidas pelo autômato. Se nenhuma senteça do tamanho dado for reconhecida, a lista será vazia.
    '''
    def enumera_sentencas(self, tamanho):
        sentencas_reconhecidas = []
        vt = list(self.__vt - set("&"))
        combinacoes = []

        if tamanho != 0:
            combinacoes = product(vt, repeat=tamanho)
        else:
            combinacoes.append("&")

        for s in combinacoes:
            if self.reconhece_sentenca(s):
                sentencas_reconhecidas.append(''.join(s))
        return sentencas_reconhecidas

    '''
        Determiniza este autômato e o retorna como um autômato novo.
        \:return o autômato determinizado.
    '''
    def determiniza(self):
        if self.isAFND():
            af = AutomatoFinito(self.get_nome() + " (determinizado)", True) # Indica que o autômato é determinizado
            af.set_vt(self.__vt)
            novo_inicial = Estado([self.__estado_inicial.to_string()])
            af.set_estado_inicial(novo_inicial)

            estados_finais = set() # Conjuntos de estados finais do novo autômato
            estados_visitados = set()
            estados_criados = set()
            estados_criados.add(novo_inicial)
            estados_a_visitar = set()
            estados_a_visitar.add(novo_inicial)

            while len(estados_a_visitar) != 0: # Se ainda há estados a visitar
                estado = estados_a_visitar.pop()
                estados_visitados.add(estado)
                for simbolo in self.__vt:
                    nova_transicao = []
                    for i in estado.to_list(): # Em um autômato determinizado, um estado do autômato pode ser composto por mais de um estado do autômato anterior
                        e = Estado(i)
                        if e in self.__estados_finais:
                            estados_finais.add(estado)
                        if len(self.__producoes[e]) != 0:
                            if simbolo in self.__producoes[e]: # Se á produções desse estado a partir do símbolo não terminal sendo analisado
                                transicoes = self.__producoes[e][simbolo]
                                for t in transicoes:
                                    nova_transicao.append(t.to_string())
                    if len(nova_transicao) != 0: # Se há produções a partir desse estado
                        nova_transicao = Estado(nova_transicao)
                        af.adiciona_transicao(estado, simbolo, nova_transicao) # Adiciona a transição ao novo autômato
                        estados_criados.add(nova_transicao)
                    else:
                        af.adiciona_estado(estado) # Se não há produções a partir desse estado, cria um estado com produções vazias
                estados_a_visitar = estados_criados - estados_visitados
            af.set_estados_finais(list(estados_finais))
            return af
        else:
            raise Exception("O autômato já é um autômato finito determinístico.")

    '''
        Minimiza este autômato.
        \:return o autômato mínimo deste autômato.
    '''
    def minimiza(self):
        af_a_minimizar = AutomatoFinito("")
        af_a_minimizar.popula_automato(self, transicoes=True, inicial=True, terminais=True)
        estados_inuteis = af_a_minimizar.estados_inacessiveis().union(af_a_minimizar.estados_mortos())
        af_a_minimizar.remover_estados(list(estados_inuteis))

        if not af_a_minimizar.is_complete():
            af_a_minimizar = af_a_minimizar.completar()
        if not af_a_minimizar.get_producoes():
            estado_unico = Estado("q0")
            af_a_minimizar.adiciona_estado(estado_unico)
            af_a_minimizar.set_estado_inicial(estado_unico)
            for simbolo in af_a_minimizar.get_vt():
                af_a_minimizar.adiciona_transicao(estado_unico, simbolo, estado_unico)

        conjuntos_por_iteracao = []
        conjuntos_por_iteracao.append([set(af_a_minimizar.get_producoes().keys()) - af_a_minimizar.get_estados_finais(), af_a_minimizar.get_estados_finais()])

        i = 0
        while i == 0 or len(conjuntos_por_iteracao[i]) != len(conjuntos_por_iteracao[i-1]):
            i += 1
            conjuntos_por_iteracao.append([])

            for conjunto_estados in conjuntos_por_iteracao[i-1]:
                lista_estados = list(conjunto_estados)
                ja_agrupados = []
                for j in range(0, len(lista_estados)):
                    estado_um = lista_estados[j]
                    if estado_um not in ja_agrupados:
                        ja_agrupados.append(estado_um)
                        equivalentes = [estado_um]
                        for k in range(j + 1, len(lista_estados)):
                            estado_dois = lista_estados[k]
                            if estado_dois not in ja_agrupados and self.__estados_equivalentes(af_a_minimizar, estado_um, estado_dois, conjuntos_por_iteracao[i-1]):
                                equivalentes.append(estado_dois)
                                ja_agrupados.append(estado_dois)
                        conjuntos_por_iteracao[i].append(equivalentes)

        af_minimo = AutomatoFinito(self.get_nome() + " (minimizado)")

        i = 0
        lista_conjnutos_finais = list(conjuntos_por_iteracao[-1])
        estados_aceitacao = []
        for conjunto in lista_conjnutos_finais:
            lista_estados = list(conjunto)
            novo_estado = Estado("q" + str(i))
            af_minimo.adiciona_estado(novo_estado)
            if lista_estados[0] in af_a_minimizar.get_estados_finais():
                estados_aceitacao.append(novo_estado)
            for simbolo in af_a_minimizar.get_vt():
                estado_destino_original = af_a_minimizar.get_producoes()[lista_estados[0]][simbolo][0]
                id_conjunto_destino = self.__encontrar_conjunto_do_estado(af_a_minimizar, estado_destino_original, lista_conjnutos_finais)
                estado_destino = Estado("q" + str(id_conjunto_destino))
                af_minimo.adiciona_transicao(novo_estado, simbolo, estado_destino)
            i += 1

        af_minimo.set_estados_finais(estados_aceitacao)
        id_estado_inicial = self.__encontrar_conjunto_do_estado(af_a_minimizar, af_a_minimizar.get_estado_inicial(), lista_conjnutos_finais)
        estado_inicial = Estado("q" + str(id_estado_inicial))
        af_minimo.set_estado_inicial(estado_inicial)

        return af_minimo

    '''
        Verifica se dois estados são equivalentes em uma iteração do algoritmo de minimização.
        \:param automato é o autômato que os estados pertencem.
        \:param estado_um é o primeiro dos dois estados que se quer saber sobre a equivalencia.
        \:param estado_dois é o segundo dos dois estados que se quer saber sobre a equivalencia.
        \:param lista_conjuntos_anterior é a lista com todos os conjuntos de equivalencia da iteração anterior.
        \:return True se os estados são equivalentes de acordo com a lista de conjuntos passada como parametro, False caso contrário.
    '''
    def __estados_equivalentes(self, automato, estado_um, estado_dois, lista_conjuntos_anterior):
        for simbolo in automato.get_vt():
            estado_destino_um = automato.get_producoes()[estado_um][simbolo][0]  # Como o AF é determinístico, podemos obter apenas o estado que esta no indice [0] dos estados destino (pois é o único).
            estado_destino_dois = automato.get_producoes()[estado_dois][simbolo][0]
            for conjunto in lista_conjuntos_anterior:
                if estado_destino_um in conjunto and estado_destino_dois not in conjunto:
                    return False
                elif estado_destino_um not in conjunto and estado_destino_dois in conjunto:
                    return False
        return True

    '''
        Encontra o conjunto que um determinado estado pertence.
        \:param automato é o autômato que o estado pertence.
        \:param estado é o estado que se quer saber a qual conjunto pertence.
        \:param lista_conjuntos é a lista com todos os conjuntos de equivalencia.
        \:return Retorna o índice do conjunto na lista de conjuntos passada como parâmetro.
    '''
    def __encontrar_conjunto_do_estado(self, automato, estado, lista_conjuntos):
        indice = 0
        for conjunto in lista_conjuntos:
            for estado_conj in conjunto:
                if estado == estado_conj:
                    return indice
            indice += 1
        return -1

    '''
        Identifica os estados inacessíveis do autômato, ou seja, estados em que não é possível chegar a partir do estado inicial.
        \:return o conjunto de estados inacessíveis.
    '''
    def estados_inacessiveis(self):
        estados_alcancados = set()
        estados_alcancados.add(self.__estado_inicial)
        estados_a_visitar = estados_alcancados

        while len(estados_a_visitar) != 0:
            estados_com_transicao = set()
            for estado in estados_a_visitar:
                for simbolo in self.__producoes[estado]:
                    transicoes = self.__producoes[estado][simbolo]
                    for t in transicoes:
                        estados_com_transicao.add(t)
            estados_a_visitar = estados_com_transicao - estados_alcancados
            estados_alcancados = estados_alcancados.union(estados_com_transicao)

        return set(self.__producoes.keys() - estados_alcancados)

    '''
        Identifica os estados mortos do autômato, ou seja, estados que não têm caminho que levem a um estado final a partir deles.
        \:return o conjunto de estados mortos.
    '''
    def estados_mortos(self):
        vivos_atuais = set(self.__estados_finais)
        vivos_anteriores = set()

        while vivos_atuais != vivos_anteriores:
            vivos_anteriores = vivos_atuais
            estados_com_transicao = set()
            for estado in self.__producoes.keys() - vivos_atuais:
                for simbolo in self.__producoes[estado]:
                    transicoes = self.__producoes[estado][simbolo]
                    for t in transicoes:
                        if t in vivos_anteriores:
                            estados_com_transicao.add(estado)
            vivos_atuais = vivos_anteriores.union(estados_com_transicao)

        return set(self.__producoes.keys() - vivos_atuais)

    '''
        Remove estados de um autômato.
        \:param lista_de_estados lista de estados à remover
    '''
    def remover_estados(self, lista_de_estados):
        try:
            self.__completo = None
            for estado in lista_de_estados:
                self.__producoes.pop(estado, None)
                if estado in self.__estados_finais:
                    self.__estados_finais.remove(estado)
            for estado_restante in self.__producoes:
                simbolos_a_remover = []
                for simbolo in self.__producoes[estado_restante]:
                    for estado_destino in self.__producoes[estado_restante][simbolo]:
                        if estado_destino in lista_de_estados:
                            self.__producoes[estado_restante][simbolo].remove(estado_destino)
                            if not self.__producoes[estado_restante][simbolo]:
                                simbolos_a_remover.append(simbolo)
                for simbolo_vazio in simbolos_a_remover:
                    self.__producoes[estado_restante].pop(simbolo_vazio, None)
        except:
            import traceback
            traceback.print_exc()

    '''
        Completa o autômato.
        \:return Um novo autômato que representa a mesma linguagem que é completo
    '''
    def completar(self):
        if self.is_complete():
            raise Exception("Autômato ja é completo")
        else:
            af_completo = AutomatoFinito(self.get_nome() + " (completo)")
            af_completo.popula_automato(self, transicoes=True, inicial=True, terminais=True)

            estado_de_erro = self.novo_estado()
            af_completo.adiciona_estado(estado_de_erro)
            for simbolo in self.__vt:
                af_completo.adiciona_transicao(estado_de_erro, simbolo, estado_de_erro)

            for simbolo in self.__vt:
                for estado in af_completo.get_producoes():
                    if simbolo not in af_completo.get_producoes()[estado]:
                        af_completo.get_producoes()[estado][simbolo] = [estado_de_erro]

            return af_completo

    '''
        Obtem o complemento do autômato que chama a função.
        \:return O autômato que representa o complemento deste autômato
    '''
    def complemento(self):
        if not self.is_complete():
            raise Exception("Autômato não é completo")
        if self.isAFND():
            raise AFNDError(" complemento")
        else:
            af_complemento = AutomatoFinito(self.get_nome() + " (complemento)")
            estados_equivalentes = af_complemento.popula_automato(self, transicoes=True, inicial=True)
            finais_complemento = []
            for estado in self.__producoes:
                if estado not in self.__estados_finais:
                    finais_complemento.append(estados_equivalentes[estado])
            af_complemento.set_estados_finais(finais_complemento)
            return af_complemento

    '''
        Obtem a união deste autômato com outro.
        \:param o segundo autômato da união.
        \:return O autômato resultante da união desse autômato com o autômato passado por parâmetro.
    '''
    def uniao(self, segundo_automato):
        af_uniao = AutomatoFinito("{" + self.get_nome() + "} uniao {" + segundo_automato.get_nome() + "}")

        estados_equivalentes_um = af_uniao.popula_automato(self, transicoes=True, terminais=True)
        estados_equivalentes_dois = af_uniao.popula_automato(segundo_automato, transicoes=True, terminais=True)

        novo_inicial = af_uniao.novo_estado()
        af_uniao.adiciona_estado(novo_inicial)
        af_uniao.set_estado_inicial(novo_inicial)

        for simbolo in self.get_producoes()[self.get_estado_inicial()]:
            for estado_destino in self.get_producoes()[self.get_estado_inicial()][simbolo]:
                af_uniao.adiciona_transicao(novo_inicial, simbolo, estados_equivalentes_um[estado_destino])

        for simbolo in segundo_automato.get_producoes()[segundo_automato.get_estado_inicial()]:
            for estado_destino in segundo_automato.get_producoes()[segundo_automato.get_estado_inicial()][simbolo]:
                af_uniao.adiciona_transicao(novo_inicial, simbolo, estados_equivalentes_dois[estado_destino])

        if (self.__estado_inicial in self.__estados_finais) or (segundo_automato.get_estado_inicial() in segundo_automato.get_estados_finais()):
            finais_atuais = af_uniao.get_estados_finais()
            finais_atuais.add(novo_inicial)
            #af_uniao.set_estados_finais(list(finais_atuais))

        return af_uniao

    '''
        Obtem a intersecção deste autômato com outro.
        \:param o segundo autômato da intersecçãp.
        \:return Uma lista de todos os autômatos gerados para se obter a intersecção
    '''
    def interseccao(self, segundo_automato):
        automatos_gerados = []

        if self.is_complete():
            la_barra = self.complemento()
        else:
            la_completo = self.completar()
            automatos_gerados.append(la_completo)
            la_barra = la_completo.complemento()
        automatos_gerados.append(la_barra)

        if segundo_automato.is_complete():
            lb_barra = segundo_automato.complemento()
        else:
            lb_completo = segundo_automato.completar()
            automatos_gerados.append(lb_completo)
            lb_barra = lb_completo.complemento()
        automatos_gerados.append(lb_barra)

        l_uniao = la_barra.uniao(lb_barra)
        automatos_gerados.append(l_uniao)

        l_deterministico = l_uniao
        if l_uniao.isAFND():
            l_deterministico = l_uniao.determiniza()
            automatos_gerados.append(l_deterministico)

        l_uniao_barra = l_deterministico.complemento()
        l_uniao_barra.set_nome("{" + self.get_nome() + "} intersec. {" + segundo_automato.get_nome() + "}")
        automatos_gerados.append(l_uniao_barra)

        return automatos_gerados

    '''
        Obtem a diferença deste autômato com outro.
        \:param o segundo autômato da diferença.
        \:return O autômato resultante da diferença desse autômato com o autômato passado por parâmetro.
    '''
    def diferenca(self, segundo_automato):
        automatos_gerados = []

        if segundo_automato.is_complete():
            lb_barra = segundo_automato.complemento()
        else:
            lb_completo = segundo_automato.completar()
            automatos_gerados.append(lb_completo)
            lb_barra = lb_completo.complemento()
        automatos_gerados.append(lb_barra)

        automatos_intersec = self.interseccao(lb_barra)
        automatos_intersec[-1].set_nome("{" + self.get_nome() + "} dif. {" + segundo_automato.get_nome() + "}")
        automatos_gerados.extend(automatos_intersec)

        return automatos_gerados

    '''
        Obtem o reverso da linguagem do autômato que chama a função.
        \:return O autômato que representa o reverso da linguagem formata por este autômato.
    '''
    def reverso(self):
        estado_equivalente = {}

        af_reverso = AutomatoFinito(self.get_nome() + " (reverso)")
        for estado in self.__producoes:
            if estado not in estado_equivalente:
                estado_equivalente[estado] = Estado(estado.to_string_display())
            novo_estado = estado_equivalente[estado]

            af_reverso.adiciona_estado(novo_estado)
            for simbolo in self.__producoes[estado]:
                for estado_destino in self.__producoes[estado][simbolo]:
                    if estado_destino not in estado_equivalente:
                        estado_equivalente[estado_destino] = Estado(estado_destino.to_string_display())
                    novo_destino = estado_equivalente[estado_destino]
                    af_reverso.adiciona_estado(novo_destino)
                    af_reverso.adiciona_transicao(novo_destino, simbolo, novo_estado)

        novo_inicial = af_reverso.novo_estado()
        af_reverso.adiciona_estado(novo_inicial)
        af_reverso.set_estado_inicial(novo_inicial)

        for estado_final in self.__estados_finais:
            for simbolo in af_reverso.get_producoes()[estado_equivalente[estado_final]]:
                for estado_destino in af_reverso.get_producoes()[estado_equivalente[estado_final]][simbolo]:
                    af_reverso.adiciona_transicao(novo_inicial, simbolo, estado_destino)

        novo_final = estado_equivalente[self.__estado_inicial]
        novos_finais = [novo_final]
        if self.__estado_inicial in self.__estados_finais:
            novos_finais.append(novo_inicial)
        af_reverso.set_estados_finais(novos_finais)
        return af_reverso

    '''
        Adiciona à esse autômato os estados do autômato passado como parâmetro.
            Outras propriedades do segundo autômato também podem ser adicionadas.
            Além disso ele verificad se ja não existe um estado com um nome igual, criando novos estados com nomes diferentes nesses casos.
        \:param segundo_automato é o autômato cujos estados serão inseridos neste autômato.
        \:param transicoes um booleano que indica se as transições também devem ser adicionadas.
        \:param inicial um booleado que indica se o estado inicial desse autômato deve passar a ser o inicial do segundo_automato.
        \:param terminais um booleado que indica se os terminais de segundo_automato devem ser adicionados aos terminais do autômato atual.
        \:return Um dicionário que mapeia os estados do segunto_automato para os novos estados no autômato atual.
    '''
    def popula_automato(self, segundo_automato, transicoes=False, inicial=False, terminais=False):
        estados_equivalentes = {}
        for estado in segundo_automato.get_producoes():
            if estado not in estados_equivalentes:
                estado_equivalente = Estado(estado.to_string_display())
                while estado_equivalente in self.__producoes:
                    estado_equivalente = Estado(estado_equivalente.to_string_display() + "'")
                estados_equivalentes[estado] = estado_equivalente
            self.adiciona_estado(estados_equivalentes[estado])
            if transicoes:
                for simbolo in segundo_automato.get_producoes()[estado]:
                    for estado_destino in segundo_automato.get_producoes()[estado][simbolo]:
                        if estado_destino not in estados_equivalentes:
                            estado_equivalente = Estado(estado_destino.to_string_display())
                            while estado_equivalente in self.__producoes:
                                estado_equivalente = Estado(estado_equivalente.to_string_display() + "'")
                            estados_equivalentes[estado_destino] = estado_equivalente
                        self.adiciona_transicao(estados_equivalentes[estado], simbolo, estados_equivalentes[estado_destino])

        if inicial:
            self.set_estado_inicial(estados_equivalentes[segundo_automato.get_estado_inicial()])

        if terminais:
            novos_terminais = []
            for terminal in segundo_automato.get_estados_finais():
                self.__estados_finais.add(estados_equivalentes[terminal])

        return estados_equivalentes

    '''
        Verifica se o autômato é um autômato finito não determinístico (AFND).
        \:return True se o autômato for um AFND ou False caso contrário.
    '''
    def isAFND(self):

        if self.__deterministico != None:
            return not self.__deterministico

        self.__deterministico = True
        for estado in self.__producoes:
            transicoes = self.__producoes[estado]
            for t in transicoes:
                if len(transicoes[t]) > 1: # Se tem mais de uma transição para um símbolo
                    self.__deterministico = False
                    return not self.__deterministico
                if t == "&" and len(transicoes.keys()) > 1 and estado != self.__estado_inicial: # Se tem &-transição e mais outras transições através de outros símbolos
                    self.__deterministico = False
                    return not self.__deterministico
        return not self.__deterministico

    '''
        Verifica se o autômato é completo, ou seja, contém transições para todos os símbolos em cada estado.
        \:return True se o autômato for completo ou False caso contrário.
    '''
    def is_complete(self):
        if self.__completo != None:
            return self.__completo

        self.__completo = True
        for estado in self.__producoes:
            transicoes = self.__producoes[estado]
            for simbolo in self.__vt:
                if simbolo not in transicoes:
                    self.__completo = False
                    return self.__completo
        return self.__completo

    '''
        Gera um novo estado que não pertence ao automato.
        \:return um estado que não pertence ao automato.
    '''
    def novo_estado(self, lista=[]):
        simbolo_novo = None
        for letra in ascii_uppercase:
            if Estado(letra) not in self.__producoes and letra not in lista:
                simbolo_novo = letra
                break
        # Se todas as letras do alfabeto já fazem parte do conjunto de símbolos terminais,
        # então o símbolo novo recebe a concatenação de duas letras (que não exista no conjunto)
        if simbolo_novo == None:
            found = False
            for l1 in ascii_uppercase:
                for l2 in ascii_uppercase:
                    letras = l1 + l2
                    if Estado(letras) not in self.__producoes and letra not in lista:
                        simbolo_novo = letras
                        found = True
                        break
                if found:
                    break
        return Estado(simbolo_novo)

    '''
        Transforma o autômato em uma matriz de strings.
        A primeira linha é composta pelos símbolos terminais do autômato e as linhas seguintes representam as transições para cada símbolo não terminal.
        \:return uma matriz de strings.
    '''
    def to_matrix(self):
        matriz =[]
        primeira_prod = []

        vt = list(self.__vt)
        vt = sorted(vt, key=str.lower)
        vt.insert(0, "")
        matriz.append(vt)
        vt = list(self.__vt)
        vt = sorted(vt, key=str.lower)
        for p in self.__producoes:
            linha = []
            simbolo = p.to_list()
            simb_inicial = self.__estado_inicial == Estado(simbolo)
            simb_final = p in self.__estados_finais

            if self.__determinizado:
                simbolo = ','.join(simbolo)
                simbolo = "[" + simbolo + "]"
            else:
                simbolo = ''.join(simbolo)

            if simb_inicial:
                simbolo = "->" + simbolo
            if simb_final:
                simbolo = "*" + simbolo
            linha.append(simbolo)

            prod = self.__producoes[p]
            for x in vt:
                if x in prod:
                    lista_estados = []
                    for estado in prod[x]:
                        if not self.__determinizado:
                            lista_estados.append(estado.to_string())
                        else:
                            lista_estados.append(estado.to_string_com_virgula())
                    estado = ", ".join(lista_estados)
                    if self.__determinizado:
                        estado = "[" + estado + "]"
                    linha.append(estado)
                else:
                    estado = "-"
                    linha.append(estado)
            if simb_inicial:
                primeira_prod = linha
            else:
                matriz.append(linha)

        matriz.insert(1, primeira_prod)
        return matriz

    def to_string(self):
        matriz = self.to_matrix()
        string = []

        maior_estado = self.__maior_estado_na_coluna(matriz, 0)
        for i in range(0, len(matriz)):
            estado = matriz[i][0]
            nome_estado = (" "*(maior_estado-len(estado))) + estado
            string.append(nome_estado)
        if self.__determinizado:
            string[0] += " "

        for i in range(1, len(matriz[0])):
            maior_estado_coluna = self.__maior_estado_na_coluna(matriz, i)
            s = matriz[0][i]
            if self.__determinizado:
                s = " " + s + " "
            string[0] += "   " + (" "*(maior_estado_coluna-len(s))) + s
            for j in range(1, len(matriz)):
                estado = matriz[j][i]
                string[j] += " | " + (" "*(maior_estado_coluna-len(estado))) + estado

        string_final = ""
        for linha in string:
            string_final += linha + "\n"
        return string_final

    def __maior_estado_na_coluna(self, matriz_de_strings, coluna):
        maior_estado = 0
        for i in range(0, len(matriz_de_strings)):
            estado = matriz_de_strings[i][coluna]
            if len(estado) > maior_estado:
                maior_estado = len(estado)
        return maior_estado

    '''
        Exibe as estruturas do autômato no console.
    '''
    def printa(self):
        print("VT:")
        for x in self.__vt:
            print(x)

        print("-------")
        print("Produções:")
        for k in self.__producoes.keys():
            print(k.to_string())
            prod = ""
            for x in self.__producoes[k]:
                est = ""
                for y in self.__producoes[k][x]:
                    y = y.to_string()
                    est += y + " , "
                prod += x + ": " + est
            print("{ " + prod + " }")

        print("-------")
        print("Estados finais:")
        for y in self.__estados_finais:
            print(y.to_string())

        print("xxxxxxx")
        print()