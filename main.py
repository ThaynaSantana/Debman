import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess

# Função para instalar pacotes .deb
def instalar_deb():
    arquivo_deb = filedialog.askopenfilename(title="Selecione um arquivo para instalar .deb", filetypes=[("Pacotes .deb", "*.deb")])
    if arquivo_deb:
        try:
            subprocess.run(['sudo', 'dpkg', '-i', arquivo_deb], check=True)
            subprocess.run(['sudo','apt','install', '-f'], check=True)
            messagebox.showinfo('Sucesso', 'Pacote .deb instalado com sucesso.')
        except subprocess.CalledProcessError:
            messagebox.showerror('Erro', 'Erro ao instalar o pacote .deb')
        except Exception as e:
            messagebox.showerror('Erro', f"Erro inesperado aconteceu: {e}")

# Função para remover pacotes .deb
def remover_deb():
    arquivo_deb = filedialog.askopenfilename(title="Selecione o pacote para remover", filetypes=[("Pacotes .deb", "*.deb")])
    if arquivo_deb:
        nome_pacote = arquivo_deb.split('/')[-1].split('.')[0]  # Obtém o nome do pacote sem a extensão
        try:
            subprocess.run(['sudo', 'apt-get', 'remove', '--purge', nome_pacote], check=True)
            messagebox.showinfo("Sucesso", f"Pacote {nome_pacote} removido com sucesso!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erro", "Erro ao remover o pacote.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Função para criar a interface gráfica
def criar_interface():
    janela = tk.Tk()
    janela.title("Debman")
    janela.geometry("500x250")
    janela.configure(bg="#2c3e50")

    # Criando uma barra de título personalizada
    barra_titulo = tk.Frame(janela, bg="#c0392b", height=30)
    barra_titulo.pack(fill="x")

    label_titulo = tk.Label(barra_titulo, text=" Debman - Gerenciador de Pacotes .deb", fg="white", bg="#c0392b", font=("Arial", 12, "bold"))
    label_titulo.pack(pady=5)

    # Frame principal
    frame = tk.Frame(janela, bg="#2c3e50")
    frame.pack(expand=True, fill="both", padx=20, pady=10)

    # Texto explicativo
    label_info = tk.Label(frame, text="Selecione um pacote .deb para instalar ou remover.", fg="white", bg="#2c3e50", font=("Arial", 10))
    label_info.pack(pady=10)

    estilo = ttk.Style()
    estilo.configure("TButton", font=("Arial", 12), padding=10)

    botao_instalar = ttk.Button(frame, text="Selecionar e Instalar Pacote", command=instalar_deb)
    botao_instalar.pack(pady=10, fill="x")

    botao_remover = ttk.Button(frame, text="Remover Pacote", command=remover_deb)
    botao_remover.pack(pady=10, fill="x")

    janela.mainloop()
    
# Inicia o app
if __name__ == "__main__":
    criar_interface()