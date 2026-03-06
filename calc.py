import customtkinter as ctk

# 1. Configuração inicial da janela
ctk.set_appearance_mode("dark")  # Tema escuro
ctk.set_default_color_theme("blue")  # Cor de destaque

app = ctk.CTk()
app.title("Calculadora")
app.geometry("300x400")
app.resizable(False, False)

# 2. Funções de lógica da calculadora
def adicionar_ao_visor(valor):
    """Adiciona o número ou operador digitado ao visor."""
    visor.insert(ctk.END, valor)

def limpar_visor():
    """Apaga tudo que está no visor."""
    visor.delete(0, ctk.END)

def calcular_resultado():
    """Pega a expressão matemática do visor e calcula."""
    expressao = visor.get()
    try:
        # A função eval() avalia a string como uma expressão matemática Python
        resultado = eval(expressao)
        limpar_visor()
        visor.insert(ctk.END, str(resultado))
    except ZeroDivisionError:
        limpar_visor()
        visor.insert(ctk.END, "Erro: Divisão por zero")
    except Exception:
        limpar_visor()
        visor.insert(ctk.END, "Erro na formatação")

# 3. Criação do Visor (Entry)
visor = ctk.CTkEntry(app, height=50, font=("Arial", 24), justify="right")
visor.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="ew")

# 4. Configuração dos Botões
# Lista com os textos dos botões na ordem em que aparecerão na grade
botoes = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

linha = 1
coluna = 0

for texto_botao in botoes:
    # Escolhendo a função do botão com base no texto dele
    if texto_botao == '=':
        comando = calcular_resultado
    elif texto_botao == 'C':
        comando = limpar_visor
    else:
        # Usamos uma função lambda para passar o valor específico do botão
        comando = lambda t=texto_botao: adicionar_ao_visor(t)
    
    # Criando o botão
    botao = ctk.CTkButton(app, text=texto_botao, width=60, height=60, font=("Arial", 20), command=comando)
    botao.grid(row=linha, column=coluna, padx=5, pady=5)
    
    # Lógica para pular para a próxima linha na grade (grid) de 4 colunas
    coluna += 1
    if coluna > 3:
        coluna = 0
        linha += 1

# Mantém a janela aberta
app.mainloop()