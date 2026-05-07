import os

# 🔥 CORREÇÕES ANDROID / XIAOMI
os.environ["KIVY_GL_BACKEND"] = "sdl2"
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_WINDOW"] = "sdl2"
os.environ["KIVY_CLOCK"] = "interrupt"

import json
from datetime import datetime, timedelta

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import (
    MDRaisedButton,
    MDFloatingActionButton,
    MDFlatButton
)
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog

# 🔥 Corrige tela branca/preta
Window.clearcolor = (1, 1, 1, 1)


class AppTarefas(MDApp):

    ARQUIVO = "tarefas.json"

    def build(self):

        self.theme_cls.primary_palette = "Indigo"

        self.tarefas = []
        self.concluidas = []
        self.dialog = None

        self.carregar_dados()

        # ROOT
        root = MDBoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10,
            size_hint=(1, 1)
        )

        # INPUTS
        self.input_nome = MDTextField(
            hint_text="Nome da tarefa"
        )

        self.input_hora = MDTextField(
            hint_text="Hora (HH:MM)"
        )

        btn_add = MDRaisedButton(
            text="Adicionar",
            pos_hint={"center_x": 0.5}
        )

        btn_add.bind(on_release=self.adicionar)

        root.add_widget(self.input_nome)
        root.add_widget(self.input_hora)
        root.add_widget(btn_add)

        # LISTA
        self.lista = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=5
        )

        self.lista.bind(
            minimum_height=self.lista.setter("height")
        )

        scroll = ScrollView(
            size_hint=(1, 1)
        )

        scroll.add_widget(self.lista)

        root.add_widget(scroll)

        # FLOAT LAYOUT (corrige FAB Android)
        layout_final = FloatLayout()

        layout_final.add_widget(root)

        # FAB
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "y": 0.03}
        )

        fab.bind(
            on_release=lambda x: self.limpar_inputs()
        )

        layout_final.add_widget(fab)

        self.atualizar()

        # 🔥 Verifica alertas
        Clock.schedule_interval(
            self.verificar_alertas,
            20
        )

        return layout_final

    # ----------------------------
    # ARQUIVO
    # ----------------------------

    def caminho_arquivo(self):
        return os.path.join(
            self.user_data_dir,
            self.ARQUIVO
        )

    def carregar_dados(self):

        try:

            caminho = self.caminho_arquivo()

            if not os.path.exists(caminho):

                with open(caminho, "w") as f:

                    json.dump(
                        {
                            "tarefas": [],
                            "concluidas": []
                        },
                        f
                    )

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

            caminho = self.caminho_arquivo()

            with open(caminho, "w") as f:

                json.dump(
                    {
                        "tarefas": self.tarefas,
                        "concluidas": self.concluidas
                    },
                    f
                )

        except Exception as e:
            print("Erro salvar:", e)

    # ----------------------------
    # FUNÇÕES
    # ----------------------------

    def adicionar(self, obj):

        nome = self.input_nome.text.strip()
        hora = self.input_hora.text.strip()

        if not nome:
            return

        if not hora:
            hora = "00:00"

        self.tarefas.append(
            {
                "nome": nome,
                "hora": hora,
                "data": datetime.now().strftime("%Y-%m-%d")
            }
        )

        self.salvar_dados()

        self.atualizar()

        self.limpar_inputs()

    def atualizar(self):

        self.lista.clear_widgets()

        for i, tarefa in enumerate(self.tarefas):

            item = TwoLineListItem(
                text=tarefa["nome"],
                secondary_text=f"{tarefa['data']} {tarefa['hora']}"
            )

            checkbox = MDCheckbox()

            checkbox.bind(
                active=lambda x, v, idx=i:
                self.executar(idx) if v else None
            )

            item.add_widget(checkbox)

            self.lista.add_widget(item)

    def executar(self, idx):

        try:

            tarefa = self.tarefas.pop(idx)

            self.concluidas.append(
                {
                    "nome": tarefa["nome"],
                    "executado_em": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                }
            )

            self.salvar_dados()

            self.atualizar()

        except Exception as e:
            print("Erro executar:", e)

    def limpar_inputs(self):

        self.input_nome.text = ""
        self.input_hora.text = ""

    # ----------------------------
    # ALERTA
    # ----------------------------

    def alerta(self, mensagem):

        try:

            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                title="⏰ Lembrete",
                text=mensagem,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x:
                        self.dialog.dismiss()
                    )
                ]
            )

            self.dialog.open()

        except Exception as e:
            print("Erro alerta:", e)

    def verificar_alertas(self, dt):

        agora = datetime.now()

        for tarefa in self.tarefas:

            try:

                data_hora = datetime.strptime(
                    f"{tarefa['data']} {tarefa['hora']}",
                    "%Y-%m-%d %H:%M"
                )

                if (
                    data_hora - timedelta(minutes=10)
                    <= agora
                    < data_hora
                ):

                    self.alerta(
                        f"Tarefa: {tarefa['nome']}"
                    )

            except Exception as e:
                print("Erro alerta tempo:", e)


AppTarefas().run()
