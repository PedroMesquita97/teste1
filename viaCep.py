import customtkinter as ctk
import requests

# 1. Configuração da janela principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Buscador de CEP")
app.geometry("400x400")
app.resizable(False, False)

# 2. Função que conecta a Interface com a API
def buscar_cep():
    # Pega o CEP digitado no campo de texto e remove espaços ou traços
    cep = entrada_cep.get().replace("-", "").replace(" ", "")
    
    # Validação simples para garantir que o usuário digitou 8 números
    if len(cep) != 8 or not cep.isdigit():
        label_resultado.configure(text="Por favor, digite um CEP válido (8 números).", text_color="red")
        return

    # Avisa o usuário que a busca começou
    label_resultado.configure(text="Buscando...", text_color="white")
    app.update() # Força a interface a atualizar a mensagem imediatamente

    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            
            if "erro" in dados:
                label_resultado.configure(text="CEP não encontrado.", text_color="red")
            else:
                # Formata o texto final com as informações da API
                texto_endereco = (
                    f"Rua: {dados.get('logradouro', 'N/A')}\n\n"
                    f"Bairro: {dados.get('bairro', 'N/A')}\n\n"
                    f"Cidade: {dados.get('localidade', 'N/A')} - {dados.get('uf', 'N/A')}\n\n"
                    f"DDD: {dados.get('ddd', 'N/A')}"
                )
                # Atualiza o texto da tela com o endereço e muda a cor para verde
                label_resultado.configure(text=texto_endereco, text_color="#2FA572")
        else:
            label_resultado.configure(text="Erro ao consultar a base de dados.", text_color="red")
            
    except requests.exceptions.RequestException:
        label_resultado.configure(text="Erro de conexão com a internet.", text_color="red")

# 3. Construção dos Elementos da Interface ("Widgets")

titulo = ctk.CTkLabel(app, text="Consulta de Endereço", font=("Arial", 20, "bold"))
titulo.pack(pady=20)

# Campo de texto (Entry) onde o usuário digita
entrada_cep = ctk.CTkEntry(app, placeholder_text="Digite o CEP (Ex: 01001000)", width=200)
entrada_cep.pack(pady=10)

# Botão que, quando clicado, executa a função "buscar_cep"
botao_buscar = ctk.CTkButton(app, text="Buscar Endereço", command=buscar_cep)
botao_buscar.pack(pady=10)

# Um quadro (Frame) para organizar e destacar o resultado na tela
frame_resultado = ctk.CTkFrame(app, width=350, height=180)
frame_resultado.pack(pady=20, padx=20, fill="both", expand=True)
frame_resultado.pack_propagate(False) # Impede que o quadro encolha

# O texto (Label) que vai mostrar o resultado final dentro do quadro
label_resultado = ctk.CTkLabel(frame_resultado, text="O resultado aparecerá aqui.", font=("Arial", 14), justify="left")
label_resultado.pack(pady=20, padx=10)

# 4. Mantém o aplicativo rodando
app.mainloop()