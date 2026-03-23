import customtkinter as ctk
import requests
import random
import threading
import io
from PIL import Image

# Configuração da Janela Principal
app = ctk.CTk()
app.geometry("650x500")
app.title("Pokédex - Busca Aleatória")
ctk.set_appearance_mode("dark")  # Deixa o visual moderno

# --- Layout: Frames ---
# Frame da Esquerda (Imagem e Botão)
left_frame = ctk.CTkFrame(app, fg_color="transparent")
left_frame.pack(side="left", fill="y", padx=20, pady=20)

# Frame da Direita (Informações e Status)
right_frame = ctk.CTkFrame(app, fg_color="transparent")
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# --- Elementos da Esquerda ---
img_label = ctk.CTkLabel(left_frame, text="Buscando\nPokémon...", width=250, height=250, font=("Arial", 16))
img_label.pack(pady=10)

btn_random = ctk.CTkButton(left_frame, text="Sortear Pokémon", font=("Arial", 16, "bold"), 
                           command=lambda: fetch_pokemon_thread(), height=40)
btn_random.pack(pady=20)

# --- Elementos da Direita ---
name_label = ctk.CTkLabel(right_frame, text="Nome do Pokémon", font=("Arial", 28, "bold"))
name_label.pack(anchor="w", pady=(0, 5))

type_label = ctk.CTkLabel(right_frame, text="Tipo: ", font=("Arial", 16))
type_label.pack(anchor="w", pady=(0, 10))

info_label = ctk.CTkLabel(right_frame, text="Altura: -- m | Peso: -- kg", font=("Arial", 14))
info_label.pack(anchor="w", pady=(0, 20))

# Frame para as Barras de Status
stats_frame = ctk.CTkFrame(right_frame)
stats_frame.pack(fill="x", pady=10)

ctk.CTkLabel(stats_frame, text="Status Base", font=("Arial", 16, "bold")).pack(pady=5)

# Dicionário para guardar as barras de progresso e atualizá-las depois
stat_bars = {}
stats_names = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
display_names = ["HP", "Ataque", "Defesa", "Atq. Esp", "Def. Esp", "Velocidade"]

for idx, stat in enumerate(stats_names):
    row = ctk.CTkFrame(stats_frame, fg_color="transparent")
    row.pack(fill="x", padx=10, pady=2)

    lbl = ctk.CTkLabel(row, text=display_names[idx], width=80, anchor="w")
    lbl.pack(side="left")

    pb = ctk.CTkProgressBar(row, width=150)
    pb.set(0)
    pb.pack(side="left", padx=10)

    val_lbl = ctk.CTkLabel(row, text="0", width=30, anchor="e")
    val_lbl.pack(side="right")

    stat_bars[stat] = (pb, val_lbl)

# --- Lógica do Aplicativo ---
def fetch_pokemon_thread():
    """Roda a busca em segundo plano para não travar a interface"""
    btn_random.configure(state="disabled", text="Buscando...")
    threading.Thread(target=fetch_pokemon, daemon=True).start()

def fetch_pokemon():
    try:
        # Sorteia um ID (1 a 1025 pega todas as gerações atuais)
        poke_id = random.randint(1, 1025)
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Processando os textos
        name = data['name'].capitalize()
        types = " / ".join([t['type']['name'].capitalize() for t in data['types']])
        height = data['height'] / 10  # Converte decímetros para metros
        weight = data['weight'] / 10  # Converte hectogramas para kg
        
        # Processando os status
        stats_data = {s['stat']['name']: s['base_stat'] for s in data['stats']}

        # Pegando a imagem de alta qualidade (official-artwork)
        img_url = data['sprites']['other']['official-artwork']['front_default']
        img_ctk = None
        if img_url:
            img_response = requests.get(img_url)
            img_data = Image.open(io.BytesIO(img_response.content))
            # Redimensiona para ficar grande e bonita na tela
            img_ctk = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(250, 250))

        # Atualiza a interface gráfica (precisa ser agendado no CustomTkinter)
        app.after(0, update_ui, name, poke_id, types, height, weight, stats_data, img_ctk)

    except Exception as e:
        print(f"Erro ao buscar: {e}")
        app.after(0, lambda: btn_random.configure(state="normal", text="Sortear Pokémon"))

def update_ui(name, poke_id, types, height, weight, stats_data, img_ctk):
    """Atualiza os textos e barras na tela"""
    name_label.configure(text=f"#{poke_id:04d} - {name}")
    type_label.configure(text=f"Tipo: {types}")
    info_label.configure(text=f"Altura: {height}m  |  Peso: {weight}kg")

    if img_ctk:
        img_label.configure(image=img_ctk, text="")
    else:
        img_label.configure(image="", text="Imagem indisponível")

    # Atualiza as barras de status
    for stat_name, (pb, val_lbl) in stat_bars.items():
        base_stat = stats_data.get(stat_name, 0)
        val_lbl.configure(text=str(base_stat))
        # Divide por 255 (status base máximo no jogo) para calcular a porcentagem da barra
        pb.set(base_stat / 255.0) 

    # Reativa o botão
    btn_random.configure(state="normal", text="Sortear Pokémon")

# Inicia buscando o primeiro Pokémon automaticamente
fetch_pokemon_thread()

# Roda o aplicativo
app.mainloop()