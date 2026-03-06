import customtkinter as ctk

# 1. Configuração da janela principal
app = ctk.CTk()
app.title("Contador de Cliques")
app.geometry("300x200")

# 2. Variável de estado (Onde guardamos o número de cliques)
# Ela precisa ficar fora da função para não ser zerada toda vez que o botão for clicado
quantidade_cliques = 0

# 3. A Função (A "Ação" do botão)
def adicionar_clique():
    # A palavra 'global' avisa ao Python que queremos modificar a variável 
    # 'quantidade_cliques' que foi criada lá fora, na linha 10.
    global quantidade_cliques
    
    # Aumentamos o valor em 1
    quantidade_cliques += 1
    
    # Atualizamos o texto do elemento visual (label) na tela
    label_numero.configure(text=str(quantidade_cliques))

# 4. Criação dos Elementos Visuais (Widgets)

# Cria o texto grande que começa com "0"
label_numero = ctk.CTkLabel(app, text="0", font=("Arial", 60, "bold"))
label_numero.pack(pady=20) # 'pady' dá um espaço vertical (em cima e embaixo)

# Cria o botão e conecta ele à função 'adicionar_clique' usando o 'command'
botao_clicar = ctk.CTkButton(app, text="Clique em mim!", command=adicionar_clique)
botao_clicar.pack(pady=10)

# 5. Mantém a janela aberta
app.mainloop()