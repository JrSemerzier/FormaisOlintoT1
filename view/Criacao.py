# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from tkinter import *
from tkinter import ttk

from model.Elemento import TipoElemento


class Criacao:

    __controller = None

    __root = None
    
    __frame_menu_principal = None

    __entry_nome = None

    __notebook_abas_de_elementos = None

    __text_gramatica = None
    __text_expressao = None

    __parent = None

    def __init__(self, parent, controller):
        self.__controller = controller
        self.__parent = parent

    def __inicializar_root(self, adicao):
        self.__root = Toplevel(self.__parent)
        self.__root.transient(self.__parent)
        if adicao:
            self.__root.title("Criação de Elemento")
        else:
            self.__root.title("Edição de Elemento")
        self.__root.resizable(width=True, height=True)

    def __inicializar_menus(self, nome, sentenca, tipo, adicao):
        padding = 10
        self.__frame_menu_principal = Frame(self.__root, padx=padding, pady=padding)
        self.__frame_menu_principal.pack()

        frame_nome = Frame(self.__frame_menu_principal, pady=padding)
        frame_nome.pack(fill=X)

        Label(frame_nome, text="Nome:").pack(side=LEFT)
        self.__entry_nome = Entry(frame_nome)
        self.__entry_nome.insert(0,nome)
        self.__entry_nome.pack(fill=X)
        self.__entry_nome.focus()

        self.__notebook_abas_de_elementos = ttk.Notebook(self.__frame_menu_principal)
        self.__notebook_abas_de_elementos.pack(expand=True, fill=BOTH)
        self.__inicializar_aba_gramatica(self.__notebook_abas_de_elementos, sentenca, tipo, adicao)
        self.__inicializar_aba_expressao(self.__notebook_abas_de_elementos, sentenca, tipo, adicao)

        if tipo is not None:
            if tipo is TipoElemento.ER:
                self.__notebook_abas_de_elementos.tab(0, state=DISABLED)
            else:
                self.__notebook_abas_de_elementos.tab(1, state=DISABLED)

    def __inicializar_aba_gramatica(self, notebook, sentenca, tipo, adicao):
        if tipo is not TipoElemento.GR:
            sentenca = ""
        self.__text_gramatica = self.__criar_aba_generica(notebook, "Gramática Regular", sentenca, adicao)

    def __inicializar_aba_expressao(self, notebook, sentenca, tipo, adicao):
        if tipo is not TipoElemento.ER:
            sentenca = ""
        self.__text_expressao = self.__criar_aba_generica(notebook, "Expressão Regular", sentenca, adicao)

    def __criar_aba_generica(self, notebook, elemento, sentenca, adicao):
        aba_elemento = ttk.Frame(notebook)
        notebook.add(aba_elemento, text=elemento)

        padding = 5
        frame_elemento = Frame(aba_elemento, padx=padding, pady=padding)
        frame_elemento.pack(expand=True, fill=BOTH)
        frame_text_area = Frame(frame_elemento, padx=padding, pady=padding)
        frame_text_area.pack(expand=True, fill=BOTH)

        text_area = Text(frame_text_area, width=0, height=0)
        text_area.insert(END, sentenca)
        text_area.pack(expand=True, fill=BOTH, side=LEFT)

        scrollbar_elemento = Scrollbar(frame_text_area, command=text_area.yview)
        text_area['yscrollcommand'] = scrollbar_elemento.set
        scrollbar_elemento.pack(fill=Y, side=LEFT)
        if adicao:
            Button(frame_elemento, text="Adicionar Nova " + elemento, command=self.cria_elemento).pack()
        else:
            Button(frame_elemento, text="Confirmar Edição", command=self.cria_elemento).pack()

        return text_area

    def __mostrar_menu(self, mostrar):
        if mostrar:
            self.__frame_menu_principal.pack(expand=True, fill=BOTH)
        else:
            self.__frame_menu_principal.pack_forget()

    def get_root(self):
        return self.__root

    def is_showing(self):
        return self.__root is not None

    def show(self, nome="", sentenca="", tipo=None, adicao=True):
        self.__inicializar_root(adicao)
        self.__inicializar_menus(nome, sentenca, tipo, adicao)
        self.__mostrar_menu(True)
        self.__root.minsize(width=400, height=300)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.centralizar(self.__root)
        self.__root.grab_set()

    def pass_set(self):
        self.__root.grab_set()

    def close(self):
        self.__root.destroy()
        self.__root = None

    def cria_elemento(self):
        nome = self.__entry_nome.get()
        aba = self.__notebook_abas_de_elementos.index(self.__notebook_abas_de_elementos.select())
        if aba == 0:
            text = self.__text_gramatica.get("1.0", 'end-1c')
            success = self.__controller.cb_nova_gramatica(nome, text)
        else:
            text = self.__text_expressao.get("1.0", 'end-1c')
            success = self.__controller.cb_nova_expressao(nome, text)

        if success:
            self.close()

    def centralizar(self, janela):
        janela.update_idletasks()
        width = janela.winfo_width()
        frm_width = janela.winfo_rootx() - janela.winfo_x()
        win_width = width + 2 * frm_width
        height = janela.winfo_height()
        titlebar_height = janela.winfo_rooty() - janela.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = janela.winfo_screenwidth() // 2 - win_width // 2
        y = janela.winfo_screenheight() // 2 - win_height // 2
        janela.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        janela.deiconify()