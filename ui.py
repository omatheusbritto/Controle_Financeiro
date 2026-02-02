import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from registro import inserir_registro, excluir_registro, listar_registros, format_valor
from relatorio import calcular_saldo

class App(tk.Tk):
    def __init__(self, usuario, cursor, conn):
        super().__init__()
        self.usuario = usuario
        self.cursor = cursor
        self.conn = conn
        self.title(f"Controle Financeiro - {usuario}")
        self.geometry("400x250")

        # Campos de entrada
        self.tipo = tk.StringVar(value="Entrada")
        self.categoria = tk.StringVar()
        self.valor = tk.Entry(self)
        self.comentario = tk.Entry(self)

        tk.Radiobutton(self, text="Entrada", variable=self.tipo, value="Entrada", command=self.update_categorias).pack(anchor="w")
        tk.Radiobutton(self, text="Saída", variable=self.tipo, value="Saída", command=self.update_categorias).pack(anchor="w")

        self.frame_cat = tk.Frame(self)
        self.frame_cat.pack()
        self.update_categorias()

        tk.Label(self, text="Valor (R$)").pack()
        self.valor.pack()

        tk.Label(self, text="Comentário").pack()
        self.comentario.pack()

        tk.Button(self, text="Registrar", command=self.registrar).pack(pady=5)

        # Botão para abrir relatório
        tk.Button(self, text="Relatório", command=self.abrir_relatorio).pack(pady=5)

        # Saldo
        self.saldo_label = tk.Label(self, text="Saldo: R$ 0,00", font=("Arial", 14, "bold"))
        self.saldo_label.pack(pady=10)

        self.atualizar_saldo()

    def update_categorias(self):
        for widget in self.frame_cat.winfo_children():
            widget.destroy()
        categorias = ["UBER", "99POP", "INDRIVER", "OUTROS"] if self.tipo.get() == "Entrada" else ["COMBUSTÍVEL", "ALIMENTAÇÃO", "INVESTIMENTOS", "DÍVIDAS", "OUTROS"]
        for cat in categorias:
            tk.Radiobutton(self.frame_cat, text=cat, variable=self.categoria, value=cat).pack(anchor="w")

    def registrar(self):
        if not self.categoria.get() or not self.valor.get():
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        try:
            valor_str = self.valor.get().replace(",", ".")
            valor = float(valor_str)
            if valor < 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Valor inválido!")
            return

        if not messagebox.askyesno("Confirmação", "Deseja registrar este lançamento?"):
            return

        inserir_registro(self.cursor, self.conn, self.usuario, self.tipo.get(), self.categoria.get(), valor, self.comentario.get())
        self.atualizar_saldo()

    def atualizar_saldo(self):
        registros = listar_registros(self.cursor, self.usuario)
        saldo = calcular_saldo(registros)
        cor = "green" if saldo >= 0 else "red"
        self.saldo_label.config(text=f"Saldo: R$ {format_valor(saldo)}", fg=cor)

    def abrir_relatorio(self):
        Relatorio(self.usuario, self.cursor, self.conn)


class Relatorio(tk.Toplevel):
    def __init__(self, usuario, cursor, conn):
        super().__init__()
        self.usuario = usuario
        self.cursor = cursor
        self.conn = conn
        self.title("Relatório Financeiro")
        self.geometry("700x400")

        self.tree = ttk.Treeview(self, columns=("Tipo", "Categoria", "Valor", "Data", "Hora", "Comentário"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")

        tk.Button(self, text="Editar", command=self.editar).pack(side="left", padx=5)
        tk.Button(self, text="Excluir", command=self.excluir).pack(side="left", padx=5)

        self.carregar_registros()

    def carregar_registros(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        registros = listar_registros(self.cursor, self.usuario)
        for r in registros:
            self.tree.insert("", "end", values=(r[2], r[3], f"R$ {format_valor(r[4])}", r[6], r[7], r[5]))

    def editar(self):
        item = self.tree.selection()
        if not item:
            return
        valores = self.tree.item(item)["values"]
        categoria, valor, data, hora, comentario = valores[1], valores[2].replace("R$ ", "").replace(",", "."), valores[3], valores[4], valores[5]

        if not messagebox.askyesno("Confirmação", "Deseja editar este registro?"):
            return

        novo_valor = simpledialog.askstring("Editar Valor", "Digite o novo valor (use vírgula):", initialvalue=valores[2].replace("R$ ", ""))
        if not novo_valor:
            return
        try:
            novo_valor = float(novo_valor.replace(",", "."))
        except:
            messagebox.showerror("Erro", "Valor inválido!")
            return

        novo_comentario = simpledialog.askstring("Editar Comentário", "Digite o novo comentário:", initialvalue=comentario)

        if not messagebox.askyesno("Confirmação Final", "Confirmar edição?"):
            return

        # Exclui registro antigo e insere novo
        excluir_registro(self.cursor, self.conn, self.usuario, categoria, float(valor), data, hora)
        inserir_registro(self.cursor, self.conn, self.usuario, valores[0], categoria, novo_valor, novo_comentario)
        self.carregar_registros()

    def excluir(self):
        item = self.tree.selection()
        if not item:
            return
        valores = self.tree.item(item)["values"]
        categoria, valor, data, hora = valores[1], valores[2].replace("R$ ", "").replace(",", "."), valores[3], valores[4]

        if not messagebox.askyesno("Confirmação", "Deseja excluir este registro?"):
            return
        if not messagebox.askyesno("Confirmação Final", "Tem certeza que deseja excluir?"):
            return

        excluir_registro(self.cursor, self.conn, self.usuario, categoria, float(valor), data, hora)
        self.carregar_registros()
