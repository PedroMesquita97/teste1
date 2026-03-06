import customtkinter as ctk

# Janela principal CTK
app = ctk.CTk()
app.title("Contador")
app.geometry("300x200")

contador = 0

#função de "ação" do botão
def clique_contador():
    global contador
    # aumenta o contador em 1
    contador += 1

    # atualizar o elemento visual na tela
    label_numero.configure(text=str(contador))

# elementos visuais
# Texto começando em 0
label_numero = ctk.CTkLabel(app, text="0", font=("Arial", 60, "bold"))
label_numero.pack(pady=20)

# Cria botão
botao_clicar = ctk.CTkButton(app, text="Clique", font=("Arial", 30), command=clique_contador)
botao_clicar.pack(pady=20)

# mantem a janela aberta
app.mainloop()
