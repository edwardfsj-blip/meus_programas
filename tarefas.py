import json

ARQUIVO = "tarefas.json"

# carregar tarefas
def carregar_tarefas():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except:
        return []

# salvar tarefas
def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w") as f:
        json.dump(tarefas, f, indent=4)

# adicionar tarefa
def adicionar_tarefa(tarefas):
    nome = input("Digite a tarefa: ")

    tarefas.append({
        "nome": nome,
        "concluida": False
    })

    salvar_tarefas(tarefas)
    print("✅ Tarefa adicionada!\n")

# listar tarefas
def listar_tarefas(tarefas):
    print("\n--- TAREFAS ---")

    if not tarefas:
        print("Nenhuma tarefa.\n")
        return

    for i, t in enumerate(tarefas, 1):
        status = "✔️" if t["concluida"] else "❌"
        print(f"{i}. {t['nome']} [{status}]")

    print()

# concluir tarefa
def concluir_tarefa(tarefas):
    listar_tarefas(tarefas)

    if not tarefas:
        return

    try:
        num = int(input("Número da tarefa: ")) - 1
        tarefas[num]["concluida"] = True
        salvar_tarefas(tarefas)
        print("✔️ Tarefa concluída!\n")
    except:
        print("Erro.\n")

# menu principal
def menu():
    tarefas = carregar_tarefas()

    while True:
        print("=== SISTEMA DE TAREFAS ===")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Concluir tarefa")
        print("4 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            concluir_tarefa(tarefas)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida\n")

menu()