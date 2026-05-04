import json
from datetime import datetime

ARQUIVO = "tarefas.json"

def carregar():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except:
        return []

def salvar(tarefas):
    with open(ARQUIVO, "w") as f:
        json.dump(tarefas, f, indent=4)

def adicionar(tarefas):
    nome = input("Tarefa: ")
    prioridade = input("Prioridade (alta/media/baixa): ")

    tarefas.append({
        "nome": nome,
        "prioridade": prioridade,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "concluida": False
    })

    salvar(tarefas)
    print("✅ Adicionada!\n")

def listar(tarefas):
    print("\n--- TAREFAS ---")

    if not tarefas:
        print("Nenhuma tarefa\n")
        return

    for i, t in enumerate(tarefas, 1):
        status = "✔️" if t["concluida"] else "❌"
        print(f"{i}. {t['nome']} | {t['prioridade']} | {t['data']} [{status}]")

    print()

def concluir(tarefas):
    listar(tarefas)
    try:
        i = int(input("Número: ")) - 1
        tarefas[i]["concluida"] = True
        salvar(tarefas)
    except:
        print("Erro\n")

def editar(tarefas):
    listar(tarefas)
    try:
        i = int(input("Número: ")) - 1
        tarefas[i]["nome"] = input("Novo nome: ")
        tarefas[i]["prioridade"] = input("Nova prioridade: ")
        salvar(tarefas)
        print("✏️ Editado!\n")
    except:
        print("Erro\n")

def excluir(tarefas):
    listar(tarefas)
    try:
        i = int(input("Número: ")) - 1
        tarefas.pop(i)
        salvar(tarefas)
        print("🗑️ Removido!\n")
    except:
        print("Erro\n")

def menu():
    tarefas = carregar()

    while True:
        print("=== SISTEMA AVANÇADO ===")
        print("1 - Adicionar")
        print("2 - Listar")
        print("3 - Concluir")
        print("4 - Editar")
        print("5 - Excluir")
        print("6 - Sair")

        op = input("Escolha: ")

        if op == "1":
            adicionar(tarefas)
        elif op == "2":
            listar(tarefas)
        elif op == "3":
            concluir(tarefas)
        elif op == "4":
            editar(tarefas)
        elif op == "5":
            excluir(tarefas)
        elif op == "6":
            break
        else:
            print("Opção inválida\n")

menu()