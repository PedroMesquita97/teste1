import customtkinter as ctk
import random

app = ctk.CTk()
app.title("Rolar o dado")
app.geometry("200x200")


def rodar_dado():
    
    dado_num = random.randint(1,6)
    label_numero.configure(text=str(dado_num))
    
label_numero = ctk.CTkLabel(app, text="0", font=("Arial", 70, "bold"))
label_numero.pack(pady=20)


botao_clicar = ctk.CTkButton(app, text="Gire o dado", command=rodar_dado)
botao_clicar.pack(pady=20)

app.mainloop()