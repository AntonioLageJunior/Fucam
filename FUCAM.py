import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

def criar_banco_de_dados():
    if not os.path.exists('beneficiarios.db'):
        conn = sqlite3.connect('beneficiarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS beneficiarios (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                estado_civil TEXT,
                escolaridade TEXT,
                cpf TEXT,
                idade INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        print('Banco de dados criado com sucesso!')
    else:
        print('O banco de dados já existe.')

# Chama a função para criar o banco de dados
criar_banco_de_dados()

def cadastrar_beneficiario():
    nome = entry_nome.get()
    estado_civil = entry_estado_civil.get()
    escolaridade = entry_escolaridade.get()
    cpf = entry_cpf.get()
    idade = entry_idade.get()

    conn = sqlite3.connect('beneficiarios.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO beneficiarios (nome, estado_civil, escolaridade, cpf, idade) VALUES (?, ?, ?, ?, ?)',
                   (nome, estado_civil, escolaridade, cpf, idade))
    conn.commit()
    conn.close()

    messagebox.showinfo('Cadastro', 'Beneficiário cadastrado com sucesso!')

def buscar_beneficiario():
    cpf = entry_busca_cpf.get()
    conn = sqlite3.connect('beneficiarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM beneficiarios WHERE cpf = ?', (cpf,))
    beneficiario = cursor.fetchone()
    conn.close()

    if beneficiario:
        abrir_janela_atualizacao(beneficiario)
    else:
        messagebox.showwarning('Busca', 'Beneficiário não encontrado.')

def atualizar_beneficiario(id, nome, estado_civil, escolaridade, cpf, idade, janela):
    conn = sqlite3.connect('beneficiarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE beneficiarios 
        SET nome = ?, estado_civil = ?, escolaridade = ?, cpf = ?, idade = ? 
        WHERE id = ?
    ''', (nome, estado_civil, escolaridade, cpf, idade, id))
    conn.commit()
    conn.close()

    messagebox.showinfo('Atualização', 'Beneficiário atualizado com sucesso!')
    janela.destroy()

def abrir_janela_atualizacao(beneficiario):
    janela_atualizacao = tk.Toplevel(root)
    janela_atualizacao.title('Atualizar Beneficiário')

    # Labels e Entry fields
    label_nome = tk.Label(janela_atualizacao, text='Nome completo:')
    entry_nome = tk.Entry(janela_atualizacao)
    entry_nome.insert(0, beneficiario[1])

    label_estado_civil = tk.Label(janela_atualizacao, text='Estado civil:')
    entry_estado_civil = tk.Entry(janela_atualizacao)
    entry_estado_civil.insert(0, beneficiario[2])

    label_escolaridade = tk.Label(janela_atualizacao, text='Escolaridade:')
    entry_escolaridade = tk.Entry(janela_atualizacao)
    entry_escolaridade.insert(0, beneficiario[3])

    label_cpf = tk.Label(janela_atualizacao, text='CPF:')
    entry_cpf = tk.Entry(janela_atualizacao)
    entry_cpf.insert(0, beneficiario[4])

    label_idade = tk.Label(janela_atualizacao, text='Idade:')
    entry_idade = tk.Entry(janela_atualizacao)
    entry_idade.insert(0, beneficiario[5])

    # Button para atualizar
    button_atualizar = tk.Button(janela_atualizacao, text='Atualizar',
                                 command=lambda: atualizar_beneficiario(
                                     beneficiario[0], entry_nome.get(), entry_estado_civil.get(), entry_escolaridade.get(), entry_cpf.get(), entry_idade.get(), janela_atualizacao))

    # Grid layout
    label_nome.grid(row=0, column=0)
    entry_nome.grid(row=0, column=1)
    label_estado_civil.grid(row=1, column=0)
    entry_estado_civil.grid(row=1, column=1)
    label_escolaridade.grid(row=2, column=0)
    entry_escolaridade.grid(row=2, column=1)
    label_cpf.grid(row=3, column=0)
    entry_cpf.grid(row=3, column=1)
    label_idade.grid(row=4, column=0)
    entry_idade.grid(row=4, column=1)
    button_atualizar.grid(row=5, columnspan=2)

root = tk.Tk()
root.geometry("400x300")
root.title('Cadastro de Beneficiários')

# Labels
label_nome = tk.Label(root, text='Nome completo:')
label_estado_civil = tk.Label(root, text='Estado civil:')
label_escolaridade = tk.Label(root, text='Escolaridade:')
label_cpf = tk.Label(root, text='CPF:')
label_idade = tk.Label(root, text='Idade:')

# Entry fields
entry_nome = tk.Entry(root)
entry_estado_civil = tk.Entry(root)
entry_escolaridade = tk.Entry(root)
entry_cpf = tk.Entry(root)
entry_idade = tk.Entry(root)

# Buttons
button_cadastrar = tk.Button(root, text='Cadastrar', command=cadastrar_beneficiario)

# Grid layout
label_nome.grid(row=0, column=0)
entry_nome.grid(row=0, column=1)
label_estado_civil.grid(row=1, column=0)
entry_estado_civil.grid(row=1, column=1)
label_escolaridade.grid(row=2, column=0)
entry_escolaridade.grid(row=2, column=1)
label_cpf.grid(row=3, column=0)
entry_cpf.grid(row=3, column=1)
label_idade.grid(row=4, column=0)
entry_idade.grid(row=4, column=1)
button_cadastrar.grid(row=5, columnspan=2)

# Busca por CPF
label_busca_cpf = tk.Label(root, text='Buscar por CPF:')
entry_busca_cpf = tk.Entry(root)
button_buscar = tk.Button(root, text='Buscar', command=buscar_beneficiario)

label_busca_cpf.grid(row=6, column=0)
entry_busca_cpf.grid(row=6, column=1)
button_buscar.grid(row=7, columnspan=2)

root.mainloop()
