import json
import os
from datetime import datetime, timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

# plyer opcional
try:
    from plyer import notification
except:
    notification = None


class AppTarefas(MDApp):

    ARQUIVO = "tarefas.json"

    # -------- CAMINHO SEGURO ANDROID
    def get_data_path(self):
        if platform == "android":
            from android.storage import app_storage_path
            path = app_storage_path()
        else:
            path = os.getcwd()

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def get_file_path(self):
        return os.path.join(self.get_data_path(), self.ARQUIVO)

    # -------- BUILD
    def build(self):
        self.theme_cls.primary_palette = "Indigo"

        self.tarefas = []
        self.concluidas = []

        self.carregar_dados()

        root = MDBoxLayout(orientation="vertical", padding=15, spacing=10)

        self.input_nome = MDTextField(hint_text="Nome da tarefa")
        self.input_hora = MDTextField(hint_text="Hora (HH:MM)")

        btn_add = MDRaisedButton(
            text="Adicionar",
            on_release=self.adicionar
        )

        root.add_widget(self.input_nome)
        root.add_widget(self.input_hora)
        root.add_widget(btn_add)

        # -------- LISTA
        self.lista = MDBoxLayout(orientation="vertical", size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.lista)

        root.add_widget(scroll)

        # -------- BOTÃO FLUTUANTE
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "y": 0.02},
            on_release=lambda x: self.limpar_inputs()
        )

        layout_final = MDBoxLayout()
        layout_final.add_widget(root)
        layout_final.add_widget(fab)

        self.atualizar()

        Clock.schedule_interval(self.verificar_alertas, 20)

        return layout_final

    # -------- CARREGAR JSON
    def carregar_dados(self):
        try:
            caminho = self.get_file_path()

            if not os.path.exists(caminho):
                with open(caminho, "w") as f:
                    json.dump({"tarefas": [], "concluidas": []}, f)

            with open(caminho, "r") as f:
                dados = json.load(f)

            self.tarefas = dados.get("tarefas", [])
            self.concluidas = dados.get("concluidas", [])

        except Exception as e:
            print("Erro carregar:", e)
            self.tarefas = []
            self.concluidas = []

    # -------- SALVAR JSON
    def salvar_dados(self):
        try:
            caminho = self.get_file_path()

            with open(caminho, "w") as f:
                json.dump({
                    "tarefas": self.tarefas,
                    "concluidas": self.concluidas
                }, f)

        except Exception as e:
            print("Erro salvar:", e)

    # -------- ADICIONAR
    def adicionar(self, obj):
        if not self.input_nome.text:
            return

        self.tarefas.append({
            "nome": self.input_nome.text,
            "hora": self.input_hora.text or "00:00",
            "data": datetime.now().strftime("%Y-%m-%d")
        })

        self.salvar_dados()
        self.atualizar()
        self.limpar_inputs()

    # -------- ATUALIZAR LISTA
    def atualizar(self):
        self.lista.clear_widgets()

        for i, t in enumerate(self.tarefas):
            item = TwoLineAvatarIconListItem(
                text=t["nome"],
                secondary_text=f"{t['data']} {t['hora']}"
            )

            check = MDCheckbox()
            check.bind(active=lambda x, v, idx=i: self.executar(idx) if v else None)

            item.add_widget(check)
            self.lista.add_widget(item)

    # -------- EXECUTAR TAREFA
    def executar(self, idx):
        try:
            t = self.tarefas.pop(idx)

            self.concluidas.append({
                "nome": t["nome"],
                "executado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            self.salvar_dados()
            self.atualizar()

        except Exception as e:
            print("Erro executar:", e)

    # -------- LIMPAR INPUTS
    def limpar_inputs(self):
        self.input_nome.text = ""
        self.input_hora.text = ""

    # -------- ALERTAS
    def verificar_alertas(self, dt):
        agora = datetime.now()

        for t in self.tarefas:
            try:
                dt_tarefa = datetime.strptime(
                    f"{t['data']} {t['hora']}",
                    "%Y-%m-%d %H:%M"
                )

                if dt_tarefa - timedelta(minutes=10) <= agora < dt_tarefa:
                    self.alerta(f"⏰ {t['nome']}")

            except:
                pass

    def alerta(self, msg):
        if notification:
            try:
                notification.notify(
                    title="Lembrete",
                    message=msg
                )
            except:
                pass


if __name__ == "__main__":
    AppTarefas().run()