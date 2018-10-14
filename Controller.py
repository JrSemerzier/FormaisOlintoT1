# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from model.Model import Model
from view.View import View

from model.exception.FormatError import FormatError
from model.exception.AFNDError import AFNDError
from model.exception.ExpressionParsingError import ExpressionParsingError
from model.Elemento import TipoElemento

'''
    Controller do padrão MVC.
'''
class Controller:

    __model = None  # Fachada do modelo
    __view = None  # Tela principal da aplicação

    '''
       Método construtor.
    '''
    def __init__(self):
        self.__model = Model()  # Fachada do modelo
        self.__view = View(self)  # Tela principal da aplicação
        self.__view.start()

    def __adicionar_multiplos_elementos(self, lista_de_elementos):
        for elemento in lista_de_elementos:
            self.__adicionar_unico_elemento(elemento)

    def __adicionar_unico_elemento(self, elemento):
        self.__model.adicionar_elemento_na_lista(elemento)
        self.__view.adicionar_elemento_na_lista(elemento.get_nome(), elemento.get_tipo())

    # Callbacks da interface

    '''
        Método que recebe um nome e a entrada de uma gramática e a adiciona no sistema, mostrando erro caso aconteça.
        \:param nome é o nome da gramática que será criada.
        \:param entrada é a representação textual da gramática.
        \:return True se a operação foi bem sucedida, False caso contrário.
    '''
    def cb_nova_gramatica(self, nome, entrada):
        try:
            gr = self.__model.criar_gramatica(nome, entrada)
            self.__adicionar_unico_elemento(gr)
            return True
        except FormatError as e:
            self.__view.mostrar_aviso(e.get_message())
            return False
        except Exception:
            self.__view.mostrar_aviso("Erro ao criar gramática.")
            return False


    '''
        Método que recebe um nome e a entrada de uma expressão e a adiciona no sistema, mostrando erro caso aconteça.
        \:param nome é o nome da expressão que será criada.
        \:param entrada é a representação textual da expressão.
        \:return True se a operação foi bem sucedida, False caso contrário.
    '''
    def cb_nova_expressao(self, nome, entrada):
        try:
            er = self.__model.criar_expressao(nome, entrada)
            self.__adicionar_unico_elemento(er)
            return True
        except ExpressionParsingError as e:
            self.__view.mostrar_aviso(e.get_message())
            return False
        except Exception:
            self.__view.mostrar_aviso("Erro ao criar expressão.")
            return False

    '''
        Método que recebe um índice e remove esse objeto da lista.
        \:param indice é o índice do elemento na lista.
    '''
    def cb_remover_elemento(self, indice):
        self.__model.remover_elemento(indice)
        self.__view.remover_elemento_da_lista(indice)

    '''
        Método que é chamado ao alterar o elemento selecionado na lista.
        \:param indice é o índice do elemento na lista.
    '''
    def cb_alterar_elemento_selecionado(self, indice):
        elemento = None
        if indice is not None:
            elemento = self.__model.obter_elemento_por_indice(indice)
        self.__view.atualiza_elemento_selecionado(indice, elemento)

    '''
        Método que é chamado ao requisitar a conversao e um elemento para uma gramática regular.
        \:param indice é o índice do elemento na lista.
    '''
    def cb_converter_para_gr(self, indice):
        elementos_novos = self.__model.transformar_elemento_em_gr(indice)
        self.__adicionar_multiplos_elementos(elementos_novos)

    '''
        Método que é chamado ao requisitar a conversao e um elemento para uma gramática regular.
        \:param indice é o índice do elemento na lista.
    '''
    def cb_converter_para_af(self, indice):
        elemento_novo = self.__model.transformar_elemento_em_af(indice)
        self.__adicionar_unico_elemento(elemento_novo)

    '''
        Método que é chamado ao requisitar uma operação entre dois elementos.
        \:param indice_um é o índice na lista do primeiro elemento da operação.
        \:param indice_dois é o índice na lista do segundo elemento da operação.
        \:param operacao é o índice da operacao selecionada.
    '''
    def cb_aplica_operacao(self, indice_um, indice_dois, operacao):
        if operacao >= 3 or indice_dois is not None:
            try:
                elementos_novos = self.__model.operacao_elementos(indice_um, indice_dois, operacao)
                self.__adicionar_multiplos_elementos(elementos_novos)
            except AFNDError as e:
                self.__view.mostrar_aviso(e.get_message())
        else:
            self.__view.mostrar_aviso("Você precisa selecionar um segundo\nelemento para aplicar a operação.")

    '''
        Método que é chamado ao requisitar uma operação entre duas gramáticas regulares.
        \:param indice_um é o índice na lista da primeira gramática da operação.
        \:param indice_dois é o índice na lista da segunda gramática da operação.
        \:param operacao é o índice da operacao selecionada.
    '''
    def cb_aplica_operacao_gr(self, indice_um, indice_dois, operacao):
        if operacao == 2 or indice_dois is not None:
            elementos_novos = self.__model.operacao_gr(indice_um, indice_dois, operacao)
            self.__adicionar_unico_elemento(elementos_novos)
        else:
            self.__view.mostrar_aviso("Você precisa selecionar uma segunda\ngramática para aplicar a operação.")

    '''
        Obtem um automato equivalente determinístico.
        \:param indice é o índice do autômato na lista.
    '''
    def cb_determiniza_af(self, indice):
        try:
            novo_elemento = self.__model.determiniza_af(indice)
            self.__adicionar_unico_elemento(novo_elemento)
        except Exception:
            self.__view.mostrar_aviso("O autômato ja é determinístico.")

    '''
        Obtem um automato equivalente minimo.
        \:param indice é o índice do autômato na lista.
    '''
    def cb_minimiza_af(self, indice):
        try:
            novo_elemento = self.__model.minimiza_af(indice)
            self.__adicionar_unico_elemento(novo_elemento)
        except Exception:
            self.__view.mostrar_aviso("É preciso que o autômato seja determinístico.")

    '''
        Informa se dada sentença é reconhecida por um autômato especificado.
        \:param indice é o índice do autômato na lista.
        \:param sentenca é a sentença que será reconhecida.
    '''
    def cb_reconhecimento(self, indice, sentenca):
        try:
            if self.__model.reconhecimento(indice, sentenca):
                self.__view.mostrar_aviso("A sentença \"" + sentenca + "\" é reconhecida pelo autômato.", "Reconhecimento de Sentença")
            else:
                self.__view.mostrar_aviso("A sentença \"" + sentenca + "\" não é reconhecida pelo autômato.", "Reconhecimento de Sentença")
        except AFNDError:
            self.__view.mostrar_aviso("O autômato precisa ser determinístico para reconhecer uma sentença.")
        except Exception:
            self.__view.mostrar_aviso("Erro ao reconhecer sentença.")

    '''
        Obtem as sentenças de um autoômato finito com determinado tamanho.
        \:param indice é o índice do autômato na lista.
        \:param tamanho é o tamanho das sentenças que serão enumeradas.
    '''
    def cb_enumeracao(self, indice, tamanho):
        try:
            sentencas = self.__model.enumeracao(indice, tamanho)
            if sentencas:
                self.__view.mostrar_lista(sentencas, tamanho)
            else:
                self.__view.mostrar_aviso("Nenhuma sentença de tamanho " + tamanho + " é reconhecida.")
        except ValueError:
            self.__view.mostrar_aviso("O tamanho da sentença deve ser um inteiro.")
        except AFNDError:
            self.__view.mostrar_aviso("O autômato precisa ser determinístico para enumerar sentenças.")
        except Exception:
            self.__view.mostrar_aviso("Erro ao enumerar sentenças.")

    '''
        Altera um elemento.
        \:param indice é o índice do autômato na lista.
        \:param tamanho é o tamanho das sentenças que serão enumeradas.
    '''
    def cb_alterar_elemento(self, indice):
        elemento = self.__model.obter_elemento_por_indice(indice)
        try:
            sucesso = self.__view.abrir_janela_edicao_de_elemento(elemento.get_nome(), elemento.to_string(), elemento.get_tipo())
            if sucesso:
                self.__view.reposiciona_elemento_editado(indice)
                self.__model.reposiciona_elemento_editado(indice)
                self.cb_alterar_elemento_selecionado(indice)
        except Exception:
            self.__view.mostrar_aviso("O elemento não foi alterado.")

    def cb_duplica_elemento(self, indice):
        copia = self.__model.duplicar(indice)
        self.__adicionar_unico_elemento(copia)

    def cb_salvar_elemento(self, indice):
        elemento = self.__model.obter_elemento_por_indice(indice)
        if elemento.get_tipo() is not TipoElemento.AF:
            caminho = self.__view.salvar_arquivo(elemento.get_nome())
            resultado = self.__model.salvar_elemento(caminho, indice)
            if resultado:
                self.__view.mostrar_aviso("Elemento salvo com sucesso.", titulo="Sucesso")
            else:
                self.__view.mostrar_aviso("Falha ao salvar arquivo.")
        else:
            self.__view.mostrar_aviso("Não é possível salvar autômatos finitos.")

    def cb_carregar_gr(self, caminho):
        try:
            conteudo = self.__model.carregar_elemento(caminho)
            nome_elemento = self.__model.nome_arquivo(caminho)
            resultado = self.cb_nova_gramatica(nome_elemento, conteudo)
            if resultado:
                self.__view.mostrar_aviso("Gramática carregada com sucesso.", titulo="Sucesso")
        except Exception:
            self.__view.mostrar_aviso("Erro ao carregar arquivo.")

    def cb_carregar_er(self, caminho):
        try:
            conteudo = self.__model.carregar_elemento(caminho)
            nome_elemento = self.__model.nome_arquivo(caminho)
            resultado = self.cb_nova_expressao(nome_elemento, conteudo)
            if resultado:
                self.__view.mostrar_aviso("Expressão carregada com sucesso.", titulo="Sucesso")
        except Exception:
            self.__view.mostrar_aviso("Erro ao carregar arquivo.")
