import customtkinter as ctk # pip install customtkinter  
import subprocess
import os

class PainelAutomacao(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Scripts")
        self.geometry("450x350")

        # Criando o sistema de abas
        self.abas = ctk.CTkTabview(self)
        self.abas.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.abas.add("Principal")
        self.abas.add("Configurações")

        # Aba Principal - Botões para os EXEs
        tab_p = self.abas.tab("Principal")

        self.label = ctk.CTkLabel(tab_p, text="Selecione a Automação", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        # Botão para o Script 1
        self.btn_script1 = ctk.CTkButton(tab_p, text="Abrir Script de Vendas", 
                                         command=lambda: self.executar_exe("vendas.exe"))
        self.btn_script1.pack(pady=10)

        # Botão para o Script 2
        self.btn_script2 = ctk.CTkButton(tab_p, text="Abrir Script de Backup", 
                                         command=lambda: self.executar_exe("backup.exe"))
        self.btn_script2.pack(pady=10)

    def executar_exe(self, nome_arquivo):
        # Pega o caminho da pasta onde este script da interface está
        caminho_pasta = os.path.dirname(__file__)
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

        try:
            # Popen inicia o processo e deixa ele rodar "solto"
            subprocess.Popen([caminho_completo])
            print(f"Sucesso: {nome_arquivo} iniciado.")
        except Exception as e:
            print(f"Erro ao abrir {nome_arquivo}: {e}")

if __name__ == "__main__":
    app = PainelAutomacao()
    app.mainloop()
