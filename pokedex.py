import customtkinter as ctk
import requests
from io import BytesIO
from PIL import Image

# 1. Configurações da Janela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pokédex Básica")
app.geometry("400x550")
app.resizable(False, False)

# 2. Funções

# Função para buscar os dados na PokeAPI
def buscar_dados_pokemon():
    # Pega o input do usuário e deixa tudo em minúsculo (necessário para a API)
    entrada = entrada_id_nome.get().lower().strip()

    if not entrada:
        return

    label_erro.configure(text="Buscando...")
    # Limpa a imagem anterior, se houver
    label_imagem.configure(image=None) 
    app.update()

    url = f"https://pokeapi.co/api/v2/pokemon/{entrada}"

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados_json = resposta.json()
            label_erro.configure(text="") # Limpa erro
            exibir_dados(dados_json)
        elif resposta.status_code == 404:
            label_erro.configure(text="Pokémon não encontrado.", text_color="red")
        else:
            label_erro.configure(text="Erro ao contatar a API.", text_color="red")
    except requests.exceptions.RequestException:
        label_erro.configure(text="Erro de conexão com a internet.", text_color="red")

# Função para exibir os textos e a imagem no frame de resultado
def exibir_dados(dados):
    # --- Dados de Texto ---
    nome = dados['name'].title() # Capitaliza o nome
    idx = dados['id']
    tipos = [t['type']['name'].title() for t in dados['types']]
    string_tipos = " / ".join(tipos) # Junta os tipos em uma string
    altura = dados['height'] / 10 # A API dá em decímetros, convertemos para metros
    peso = dados['weight'] / 10 # A API dá em hectogramas, convertemos para KG

    # Atualiza as labels
    label_nome_id.configure(text=f"[{idx}] {nome}")
    label_tipos.configure(text=f"Tipo(s): {string_tipos}")
    label_informacoes.configure(text=f"Altura: {altura}m\nPeso: {peso}kg")

    # --- Dados de Imagem ---
    # Pegamos a URL da imagem oficial (official-artwork). O PokeAPI tem muitas imagens!
    # Se você quiser GIFs, o caminho é: dados['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
    url_imagem = dados['sprites']['other']['official-artwork']['front_default']

    if url_imagem:
        baixar_exibir_imagem(url_imagem)

# Função para baixar a imagem e colocar no CTkImage
def baixar_exibir_imagem(url_url):
    try:
        # Baixa os bytes da imagem
        print(f"Baixando imagem de: {url_url}...")
        resposta_img = requests.get(url_url)
        
        # Transforma os bytes em um objeto de imagem PIL
        img_pil = Image.open(BytesIO(resposta_img.content))
        
        # Converte a imagem PIL para um CTkImage (compatível com CustomTkinter)
        # Definimos o tamanho (ex: 200x200)
        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(200, 200))
        
        # Aplica a imagem na Label de imagem
        label_imagem.configure(image=img_ctk)
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")

# 3. Widgets da Interface

titulo = ctk.CTkLabel(app, text="Minha Pokédex", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Entrada do usuário
entrada_id_nome = ctk.CTkEntry(app, placeholder_text="Digite ID ou Nome (Ex: 25 ou pikachu)")
entrada_id_nome.pack(pady=10, padx=20, fill="x")

# Botão de Busca
# Note que a função é chamada sem os (), pois é uma referência que o botão executará
botao_buscar = ctk.CTkButton(app, text="Buscar Pokémon", command=buscar_dados_pokemon)
botao_buscar.pack(pady=10)

# Mensagens de Erro/Status
label_erro = ctk.CTkLabel(app, text="")
label_erro.pack()

# --- Quadro de Resultado ---
frame_resultado = ctk.CTkFrame(app, width=350, height=350)
frame_resultado.pack(pady=20, padx=20, fill="both", expand=True)

# Imagem (Label vazia esperando ser preenchida)
label_imagem = ctk.CTkLabel(frame_resultado, text="") 
label_imagem.pack(pady=20)

# Nome e ID
label_nome_id = ctk.CTkLabel(frame_resultado, text="", font=("Arial", 20, "bold"))
label_nome_id.pack(pady=5)

# Tipos
label_tipos = ctk.CTkLabel(frame_resultado, text="", font=("Arial", 16, "italic"), text_color="#A0A0A0")
label_tipos.pack()

# Outras informações (Altura/Peso)
label_informacoes = ctk.CTkLabel(frame_resultado, text="", font=("Arial", 14), justify="left")
label_informacoes.pack(pady=15, padx=20, anchor="w")

# 4. Inicia o Loop Principal
app.mainloop()