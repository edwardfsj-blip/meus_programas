import tkinter as tk
import json
import os

ARQUIVO = "tarefas.json"

def carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar(tarefas):
    with open(ARQUIVO, "w") as f:
        json.dump(tarefas, f, indent=4)

tarefas = carregar()

def atualizar():
    lista.delete(0, tk.END)
    for t in tarefas:
        status = "✔" if t["concluida"] else "•"
        lista.insert(tk.END, f"{t['nome']}  {status}")

def adicionar():
    nome = entrada.get()
    if nome:
        tarefas.append({"nome": nome, "concluida": False})
        salvar(tarefas)
        entrada.delete(0, tk.END)
        atualizar()

def concluir():
    try:
        i = lista.curselection()[0]
        tarefas[i]["concluida"] = True
        salvar(tarefas)
        atualizar()
    except:
        pass

def excluir():
    try:
        i = lista.curselection()[0]
        tarefas.pop(i)
        salvar(tarefas)
        atualizar()
    except:
        pass

# janela
app = tk.Tk()
app.title("Task App")
app.geometry("380x500")
app.configure(bg="#121212")

# título
titulo = tk.Label(app, text="Minhas Tarefas", fg="white", bg="#121212", font=("Segoe UI", 18, "bold"))
titulo.pack(pady=15)

# entrada
entrada = tk.Entry(app, font=("Segoe UI", 12), bd=0)
entrada.pack(padx=20, fill="x", ipady=8)

# botões
frame = tk.Frame(app, bg="#121212")
frame.pack(pady=10)

def btn(text, cor, cmd):
    return tk.Button(frame, text=text, bg=cor, fg="white",
                     font=("Segoe UI", 10), bd=0,
                     width=10, command=cmd)

btn("Adicionar", "#00c853", adicionar).grid(row=0, column=0, padx=5)
btn("Concluir", "#2196f3", concluir).grid(row=0, column=1, padx=5)
btn("Excluir", "#f44336", excluir).grid(row=0, column=2, padx=5)

# lista
lista = tk.Listbox(app, font=("Segoe UI", 12), bg="#1e1e1e", fg="white",
                   selectbackground="#333", bd=0)
lista.pack(padx=20, pady=10, fill="both", expand=True)

atualizar()
app.mainloop()