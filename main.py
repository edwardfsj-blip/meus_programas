import json
from datetime import datetime, timedelta

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker

from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView


class Tab(MDScreen, MDTabsBase):
    pass


class AppTarefas(MDApp):

    ARQUIVO = "tarefas.json"

    def build(self):
        # 🎨 TEMA PREMIUM
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "400"

        self.tarefas = []
        self.concluidas = []
        self.selecionada = None
        self.selecionada_concluida = None
        self.data_selecionada = None

        self.carregar_dados()

        root = MDBoxLayout(orientation="vertical")
        root.md_bg_color = (1, 1, 1, 1)

        self.tabs = MDTabs()
        root.add_widget(self.tabs)

        # ---------------- ABA ADICIONAR
        self.tab_add = Tab(title="Adicionar")
        box_add = MDBoxLayout(orientation="vertical", padding=15, spacing=15)

        self.input_nome = MDTextField(hint_text="Nome da tarefa")
        self.input_hora = MDTextField(hint_text="Horário (HH:MM)")

        self.btn_data = MDRaisedButton(
            text="Selecionar data",
            on_release=self.abrir_calendario
        )

        self.prioridade = "Normal"
        self.btn_prioridade = MDRaisedButton(text="Prioridade: Normal")

        menu_items = [
            {"text": "Alta", "on_release": lambda x="Alta": self.set_prioridade(x)},
            {"text": "Normal", "on_release": lambda x="Normal": self.set_prioridade(x)},
            {"text": "Baixa", "on_release": lambda x="Baixa": self.set_prioridade(x)},
        ]

        self.menu = MDDropdownMenu(caller=self.btn_prioridade, items=menu_items)
        self.btn_prioridade.bind(on_release=lambda x: self.menu.open())

        btn_salvar = MDRaisedButton(text="Salvar tarefa", on_release=self.adicionar)

        box_add.add_widget(self.input_nome)
        box_add.add_widget(self.input_hora)
        box_add.add_widget(self.btn_data)
        box_add.add_widget(self.btn_prioridade)
        box_add.add_widget(btn_salvar)

        self.tab_add.add_widget(box_add)

        # ---------------- PENDENTES
        self.tab_pend = Tab(title="Pendentes")

        self.lista = MDBoxLayout(orientation="vertical", spacing=5, size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.lista)

        self.box_acoes = MDBoxLayout(size_hint_y=None, height=50)
        self.box_acoes.opacity = 0

        btn_exec = MDRaisedButton(text="Executar", on_release=self.executar)
        btn_del = MDRaisedButton(text="Excluir", on_release=self.excluir)

        self.box_acoes.add_widget(btn_exec)
        self.box_acoes.add_widget(btn_del)

        box_pend = MDBoxLayout(orientation="vertical")
        box_pend.add_widget(scroll)
        box_pend.add_widget(self.box_acoes)

        self.tab_pend.add_widget(box_pend)

        # ---------------- CONCLUÍDAS
        self.tab_done = Tab(title="Concluídas")

        self.lista_concluidas = MDBoxLayout(
            orientation="vertical", spacing=5, size_hint_y=None
        )
        self.lista_concluidas.bind(minimum_height=self.lista_concluidas.setter('height'))

        scroll2 = ScrollView()
        scroll2.add_widget(self.lista_concluidas)

        self.box_acoes_done = MDBoxLayout(size_hint_y=None, height=50)
        self.box_acoes_done.opacity = 0

        btn_del_done = MDRaisedButton(
            text="Excluir concluída",
            on_release=self.excluir_concluida
        )

        self.box_acoes_done.add_widget(btn_del_done)

        container_done = MDBoxLayout(orientation="vertical")
        container_done.add_widget(scroll2)
        container_done.add_widget(self.box_acoes_done)

        self.tab_done.add_widget(container_done)

        # ADD TABS
        self.tabs.add_widget(self.tab_add)
        self.tabs.add_widget(self.tab_pend)
        self.tabs.add_widget(self.tab_done)

        self.atualizar()

        Clock.schedule_interval(self.verificar_alertas, 30)
        Clock.schedule_interval(self.limpar_concluidas_antigas, 60)

        return root

    # ---------------- SALVAR / CARREGAR
    def salvar_dados(self):
        with open(self.ARQUIVO, "w") as f:
            json.dump({
                "tarefas": self.tarefas,
                "concluidas": self.concluidas
            }, f)

    def carregar_dados(self):
        try:
            with open(self.ARQUIVO, "r") as f:
                dados = json.load(f)
                self.tarefas = dados.get("tarefas", [])
                self.concluidas = dados.get("concluidas", [])
        except:
            pass

    # ---------------- CALENDÁRIO
    def abrir_calendario(self, obj):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.definir_data)
        date_dialog.open()

    def definir_data(self, instance, value, date_range):
        self.data_selecionada = value.strftime("%Y-%m-%d")
        self.btn_data.text = value.strftime("%d/%m/%Y")

    # ---------------- PRIORIDADE
    def set_prioridade(self, valor):
        self.prioridade = valor
        self.btn_prioridade.text = f"Prioridade: {valor}"
        self.menu.dismiss()

    # ---------------- ADICIONAR
    def adicionar(self, obj):
        if not self.input_nome.text or not self.input_hora.text or not self.data_selecionada:
            self.mostrar_alerta("Preencha tudo!")
            return

        self.tarefas.append({
            "nome": self.input_nome.text,
            "hora": self.input_hora.text,
            "data": self.data_selecionada,
            "prioridade": self.prioridade
        })

        self.salvar_dados()
        self.input_nome.text = ""
        self.input_hora.text = ""
        self.atualizar()

    # ---------------- ATUALIZAR
    def atualizar(self):
        self.lista.clear_widgets()
        self.lista_concluidas.clear_widgets()

        for i, t in enumerate(self.tarefas):
            cor = {
                "Alta": (1, 0.3, 0.3, 1),
                "Normal": (0.2, 0.6, 1, 1),
                "Baixa": (0.5, 0.5, 0.5, 1)
            }[t["prioridade"]]

            item = OneLineListItem(
                text=f"{t['nome']} - {t['data']} {t['hora']}",
                text_color=cor
            )
            item.bind(on_release=lambda x, idx=i: self.selecionar(idx))
            self.lista.add_widget(item)

        for i, t in enumerate(self.concluidas):
            item = OneLineListItem(
                text=f"{t['nome']} ✔ {t['executado_em']}"
            )
            item.bind(on_release=lambda x, idx=i: self.selecionar_concluida(idx))
            self.lista_concluidas.add_widget(item)

    # ---------------- SELECIONAR
    def selecionar(self, i):
        self.selecionada = i
        self.box_acoes.opacity = 1

    def selecionar_concluida(self, i):
        self.selecionada_concluida = i
        self.box_acoes_done.opacity = 1

    # ---------------- EXECUTAR
    def executar(self, obj):
        tarefa = self.tarefas.pop(self.selecionada)

        self.concluidas.append({
            "nome": tarefa["nome"],
            "executado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.selecionada = None
        self.box_acoes.opacity = 0
        self.salvar_dados()
        self.atualizar()

    # ---------------- EXCLUIR
    def excluir(self, obj):
        self.tarefas.pop(self.selecionada)
        self.selecionada = None
        self.box_acoes.opacity = 0
        self.salvar_dados()
        self.atualizar()

    def excluir_concluida(self, obj):
        if self.selecionada_concluida is None:
            return

        self.concluidas.pop(self.selecionada_concluida)
        self.selecionada_concluida = None
        self.box_acoes_done.opacity = 0

        self.salvar_dados()
        self.atualizar()

    # ---------------- LIMPEZA AUTOMÁTICA
    def limpar_concluidas_antigas(self, dt):
        limite = datetime.now() - timedelta(days=30)

        novas = []
        for t in self.concluidas:
            data_exec = datetime.strptime(t["executado_em"], "%Y-%m-%d %H:%M:%S")
            if data_exec > limite:
                novas.append(t)

        self.concluidas = novas
        self.salvar_dados()

    # ---------------- ALERTAS
    def verificar_alertas(self, dt):
        agora_data = datetime.now().strftime("%Y-%m-%d")
        agora_hora = datetime.now().strftime("%H:%M")

        for t in self.tarefas:
            if t["data"] == agora_data and t["hora"] == agora_hora:
                self.mostrar_alerta(f"Tarefa: {t['nome']}")

    def mostrar_alerta(self, texto):
        MDDialog(title="Aviso", text=texto).open()


AppTarefas().run()