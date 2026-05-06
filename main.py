import json
import os
from datetime import datetime, timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatIconButton, MDFloatingActionButton
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker

# plyer opcional
try:
    from plyer import notification
except:
    notification = None


# 🔥 CORREÇÃO CRÍTICA (não usar MDScreen)
class Tab(MDBoxLayout, MDTabsBase):
    pass


class CalendarioPT(MDDatePicker):
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
        self.tab_add = Tab(title="Adicionar", orientation="vertical")

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

        self.menu = MDDropdownMenu(
            caller=self.btn_prioridade,
            items=menu_items,
            width_mult=4,
            max_height=200
        )

        self.btn_prioridade.bind(on_release=lambda x: self.menu.open())

        btn_salvar = MDRectangleFlatIconButton(
            text="Salvar",
            icon="check",
            on_release=self.adicionar
        )

        box.add_widget(self.input_nome)
        box.add_widget(self.input_hora)
        box.add_widget(self.btn_data)
        box.add_widget(self.btn_prioridade)
        box.add_widget(btn_salvar)

        self.tab_add.add_widget(box)

        # -------- ABA PENDENTES
        self.tab_pend = Tab(title="Pendentes", orientation="vertical")

        self.lista = MDBoxLayout(orientation="vertical", size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.lista)

        self.box_acoes = MDBoxLayout(size_hint_y=None, height=50)
        self.box_acoes.opacity = 0

        btn_exec = MDRectangleFlatIconButton(text="Executar", on_release=self.executar)
        btn_del = MDRectangleFlatIconButton(text="Excluir", on_release=self.excluir)

        self.box_acoes.add_widget(btn_exec)
        self.box_acoes.add_widget(btn_del)

        layout_pend = MDBoxLayout(orientation="vertical")
        layout_pend.add_widget(scroll)
        layout_pend.add_widget(self.box_acoes)

        self.tab_pend.add_widget(layout_pend)

        # -------- ABA CONCLUÍDAS
        self.tab_done = Tab(title="Concluídas", orientation="vertical")

        self.lista_concluidas = MDBoxLayout(orientation="vertical", size_hint_y=None)
        self.lista_concluidas.bind(minimum_height=self.lista_concluidas.setter('height'))

        scroll_done = ScrollView()
        scroll_done.add_widget(self.lista_concluidas)

        self.tab_done.add_widget(scroll_done)

        # -------- ADICIONAR TABS
        self.tabs.add_widget(self.tab_add)
        self.tabs.add_widget(self.tab_pend)
        self.tabs.add_widget(self.tab_done)

        # -------- FAB (corrigido)
        layout_final = MDBoxLayout(orientation="vertical")
        layout_final.add_widget(root)

        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "y": 0.02},
            on_release=lambda x: self.tabs.switch_tab(self.tab_add)
        )

        layout_final.add_widget(fab)

        self.atualizar()
        Clock.schedule_interval(self.verificar_alertas, 20)

        return layout_final

    # -------- JSON ANDROID SAFE
    def carregar_dados(self):
        try:
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
            print("Erro carregar:", e)
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
            print("Erro salvar:", e)

    # -------- FUNÇÕES
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
            check.bind(active=lambda x, v, idx=i: self.marcar_execucao(idx) if v else None)

            item.add_widget(check)
            self.lista.add_widget(item)

        for i, t in enumerate(self.concluidas):
            item = TwoLineAvatarIconListItem(
                text=t["nome"],
                secondary_text=t["executado_em"]
            )
            self.lista_concluidas.add_widget(item)

    def marcar_execucao(self, idx):
        self.selecionada = idx
        self.executar(None)

    def selecionar(self, i):
        self.selecionada = i
        self.box_acoes.opacity = 1

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

    def verificar_alertas(self, dt):
        agora = datetime.now()

        for t in self.tarefas:
            try:
                dt_tarefa = datetime.strptime(f"{t['data']} {t['hora']}", "%Y-%m-%d %H:%M")
                if dt_tarefa - timedelta(minutes=10) <= agora < dt_tarefa:
                    self.alerta(f"⏰ {t['nome']}")
            except:
                pass

    def alerta(self, msg):
        if notification:
            notification.notify(title="Lembrete", message=msg)


AppTarefas().run()