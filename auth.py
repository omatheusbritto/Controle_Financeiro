import tkinter as tk
from tkinter import messagebox

class Login(tk.Tk):
    def __init__(self, cursor, conn, AppClass):
        super().__init__()
        self.cursor = cursor
        self.conn = conn
        self.AppClass = AppClass
        self.title("Login - Controle Financeiro")
        self.geometry("300x200")

        tk.Label(self, text="Usuário").pack()
        self.usuario = tk.Entry(self)
        self.usuario.pack()

        tk.Label(self, text="Senha").pack()
        self.senha = tk.Entry(self, show="*")
        self.senha.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=5)
        tk.Button(self, text="Cadastrar", command=self.cadastrar).pack()

    def login(self):
        u = self.usuario.get()
        s = self.senha.get()
        self.cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (u, s))
        if self.cursor.fetchone():
            self.destroy()
            self.AppClass(u, self.cursor, self.conn)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def cadastrar(self):
        u = self.usuario.get()
        s = self.senha.get()
        if not u or not s:
            messagebox.showerror("Erro", "Preencha usuário e senha!")
            return
        try:
            self.cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (u, s))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado!")
        except:
            messagebox.showerror("Erro", "Usuário já existe!")
