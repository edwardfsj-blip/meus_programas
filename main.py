import json
import os
from datetime import datetime, timedelta

from kivy.resources import resource_find
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatIconButton, MDFloatingActionButton
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker

# 🔒 plyer opcional (evita crash)
try:
    from plyer import notification
except:
    notification = None


class CalendarioPT(MDDatePicker):
    pass


class Tab(MDScreen, MDTabsBase):
    pass


class AppTarefas(MDApp):

    ARQUIVO = "tarefas.json"

    def build(self):
        self.theme_cls.primary_palette = "Indigo"

        self.tarefas = []
        self.concluidas = []
        self.selecionada = None
        self.selecionada_concluida = None
        self.data_selecionada = None
        self.prioridade = "Normal"

        self.carregar_dados()

        root = MDBoxLayout(orientation="vertical")

        self.tabs = MDTabs()
        root.add_widget(self.tabs)

        # -------- ABA ADICIONAR
        self.tab_add = Tab(title="Adicionar")

        box = MDBoxLayout(orientation="vertical", padding=15, spacing=10)

        self.input_nome = MDTextField(hint_text="Nome")
        self.input_hora = MDTextField(hint_text="Hora (HH:MM)")

        self.btn_data = MDRectangleFlatIconButton(
            text="Selecionar data",
            icon="calendar",
            on_release=self.abrir_calendario
        )

        self.btn_prioridade = MDRectangleFlatIconButton(
            text="Prioridade: Normal",
            icon="flag"
        )

        menu_items = [
            {"text": "Alta", "on_release": lambda x="Alta": self.set_prioridade(x)},
            {"text": "Normal", "on_release": lambda x="Normal": self.set_prioridade(x)},
            {"text": "Baixa", "on_release": lambda x="Baixa": self.set_prioridade(x)},
        ]

        self.menu = MDDropdownMenu(caller=self.btn_prioridade, items=menu_items)
        self.btn_prioridade.bind(on_release=lambda x: self.menu.open())

        btn_salvar = MDRectangleFlatIconButton(
            text="Salvar",
            icon="check",
            md_bg_color=(0, 0.6, 1, 1),
            text_color=(1, 1, 1, 1),
            on_release=self.adicionar
        )

        box.add_widget(self.input_nome)
        box.add_widget(self.input_hora)
        box.add_widget(self.btn_data)
        box.add_widget(self.btn_prioridade)
        box.add_widget(btn_salvar)

        self.tab_add.add_widget(box)

        # -------- ABA PENDENTES
        self.tab_pend = Tab(title="Pendentes")

        self.lista = MDBoxLayout(orientation="vertical", size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.lista)

        self.box_acoes = MDBoxLayout(size_hint_y=None, height=50)
        self.box_acoes.opacity = 0

        btn_exec = MDRectangleFlatIconButton(text="Executar", icon="check", on_release=self.executar)
        btn_del = MDRectangleFlatIconButton(text="Excluir", icon="close", on_release=self.excluir)
        btn_edit = MDRectangleFlatIconButton(text="Editar", icon="pencil", on_release=self.editar_tarefa)

        self.box_acoes.add_widget(btn_exec)
        self.box_acoes.add_widget(btn_del)
        self.box_acoes.add_widget(btn_edit)

        layout_pend = MDBoxLayout(orientation="vertical")
        layout_pend.add_widget(scroll)
        layout_pend.add_widget(self.box_acoes)

        self.tab_pend.add_widget(layout_pend)

        # -------- ABA CONCLUÍDAS
        self.tab_done = Tab(title="Concluídas")

        self.lista_concluidas = MDBoxLayout(orientation="vertical", size_hint_y=None)
        self.lista_concluidas.bind(minimum_height=self.lista_concluidas.setter('height'))

        scroll_done = ScrollView()
        scroll_done.add_widget(self.lista_concluidas)

        self.box_acoes_done = MDBoxLayout(size_hint_y=None, height=50)
        self.box_acoes_done.opacity = 0

        btn_del_done = MDRectangleFlatIconButton(
            text="Excluir",
            icon="close",
            on_release=self.excluir_concluida
        )

        self.box_acoes_done.add_widget(btn_del_done)

        layout_done = MDBoxLayout(orientation="vertical")
        layout_done.add_widget(scroll_done)
        layout_done.add_widget(self.box_acoes_done)

        self.tab_done.add_widget(layout_done)

        # -------- ADICIONAR TABS
        self.tabs.add_widget(self.tab_add)
        self.tabs.add_widget(self.tab_pend)
        self.tabs.add_widget(self.tab_done)

        # -------- BOTÃO +
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "y": 0.02},
            on_release=lambda x: self.tabs.switch_tab("Adicionar")
        )
        root.add_widget(fab)

        self.atualizar()
        Clock.schedule_interval(self.verificar_alertas, 20)

        return root

    # -------- DADOS (ANDROID SAFE)
    def carregar_dados(self):
        try:
            caminho = resource_find(self.ARQUIVO)

            if not caminho:
                caminho = os.path.join(App.get_running_app().user_data_dir, self.ARQUIVO)

            if not os.path.exists(caminho):
                self.tarefas = []
                self.concluidas = []
                return

            with open(caminho, "r") as f:
                dados = json.load(f)

            self.tarefas = dados.get("tarefas", [])
            self.concluidas = dados.get("concluidas", [])

        except Exception as e:
            print("ERRO carregar:", e)
            self.tarefas = []
            self.concluidas = []

    def salvar_dados(self):
        try:
            caminho = os.path.join(App.get_running_app().user_data_dir, self.ARQUIVO)

            with open(caminho, "w") as f:
                json.dump({
                    "tarefas": self.tarefas,
                    "concluidas": self.concluidas
                }, f)

        except Exception as e:
            print("ERRO salvar:", e)

    # -------- RESTO DO APP (igual)
    def abrir_calendario(self, obj):
        dialog = CalendarioPT()
        dialog.bind(on_save=self.definir_data)
        dialog.open()

    def definir_data(self, instance, value, date_range):
        self.data_selecionada = value.strftime("%Y-%m-%d")
        self.btn_data.text = value.strftime("%d/%m/%Y")

    def set_prioridade(self, valor):
        self.prioridade = valor
        self.btn_prioridade.text = f"Prioridade: {valor}"
        self.menu.dismiss()

    def adicionar(self, obj):
        if not self.input_nome.text:
            return

        self.tarefas.append({
            "nome": self.input_nome.text,
            "hora": self.input_hora.text or "00:00",
            "data": self.data_selecionada or datetime.now().strftime("%Y-%m-%d"),
            "prioridade": self.prioridade
        })

        self.salvar_dados()
        self.atualizar()

    def atualizar(self):
        self.lista.clear_widgets()
        self.lista_concluidas.clear_widgets()

        for i, t in enumerate(self.tarefas):
            item = TwoLineAvatarIconListItem(
                text=t["nome"],
                secondary_text=f"{t['data']} {t['hora']}"
            )

            item.bind(on_release=lambda x, idx=i: self.selecionar(idx))

            check = MDCheckbox()
            check.bind(active=lambda x, v, idx=i: self.executar(None) if v else None)

            item.add_widget(check)
            self.lista.add_widget(item)

        for i, t in enumerate(self.concluidas):
            item = TwoLineAvatarIconListItem(
                text=t["nome"],
                secondary_text=t["executado_em"]
            )
            item.bind(on_release=lambda x, idx=i: self.selecionar_concluida(idx))
            self.lista_concluidas.add_widget(item)

    def selecionar(self, i):
        self.selecionada = i
        self.box_acoes.opacity = 1

    def selecionar_concluida(self, i):
        self.selecionada_concluida = i
        self.box_acoes_done.opacity = 1

    def executar(self, obj):
        if self.selecionada is None:
            return

        t = self.tarefas.pop(self.selecionada)

        self.concluidas.append({
            "nome": t["nome"],
            "executado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        self.selecionada = None
        self.box_acoes.opacity = 0

        self.salvar_dados()
        self.atualizar()

    def excluir(self, obj):
        if self.selecionada is None:
            return

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

    def editar_tarefa(self, obj):
        if self.selecionada is None:
            return

        t = self.tarefas[self.selecionada]

        nome = MDTextField(text=t["nome"])
        hora = MDTextField(text=t["hora"])

        box = MDBoxLayout(orientation="vertical")
        box.add_widget(nome)
        box.add_widget(hora)

        def salvar(x):
            t["nome"] = nome.text
            t["hora"] = hora.text
            self.salvar_dados()
            self.atualizar()
            dialog.dismiss()

        dialog = MDDialog(
            title="Editar",
            type="custom",
            content_cls=box,
            buttons=[
                MDRectangleFlatIconButton(text="Salvar", icon="check", on_release=salvar)
            ]
        )

        dialog.open()

    def verificar_alertas(self, dt):
        agora = datetime.now()

        for t in self.tarefas:
            try:
                dt_tarefa = datetime.strptime(f"{t['data']} {t['hora']}", "%Y-%m-%d %H:%M")
                if dt_tarefa - timedelta(minutes=10) <= agora < dt_tarefa:
                    self.alerta(f"⏰ {t['nome']}")
            except Exception as e:
                print("ERRO alerta:", e)

    def alerta(self, msg):
        if notification:
            notification.notify(title="Lembrete", message=msg)
        else:
            MDDialog(title="Aviso", text=msg).open()


AppTarefas().run()