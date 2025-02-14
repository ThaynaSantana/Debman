import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, 
    QFileDialog, QLabel, QInputDialog, QPushButton, QVBoxLayout
)
from PyQt6.QtGui import QPalette, QColor, QFont, QDesktopServices
from PyQt6.QtCore import Qt, QUrl

class DebmanApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Debman - Gerenciador de Pacotes .deb")
        self.setGeometry(100, 100, 500, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Titulo do app
        self.title = QLabel("Debman")
        self.title.setFont(QFont("Arial", 16))
        self.title.setStyleSheet("color: #fafafa; background-color: #d96d62; font-weight: bold; padding: 12px;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)
        
        # Texto explicativo
        self.label = QLabel("Selecione um pacote .deb para instalar ou remover.")
        self.label.setFont(QFont("Arial", 10))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        # Botão para instalar
        self.btn_instalar = QPushButton("Selecionar e Instalar Pacote")
        self.btn_instalar.setStyleSheet(self.button_style())
        self.btn_instalar.clicked.connect(self.instalar_deb)
        layout.addWidget(self.btn_instalar)

        # Botão para remover
        self.btn_remover = QPushButton("Remover Pacote")
        self.btn_remover.setStyleSheet(self.button_style())
        self.btn_remover.clicked.connect(self.remover_deb)
        layout.addWidget(self.btn_remover)

        # Área de logs
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setStyleSheet("background-color: #1e272e; color: white; font-size: 12px;")
        layout.addWidget(self.logs)
        
        # Créditos e link para doação com links clicáveis
        creditos = QLabel("Desenvolvido por: Thayna Santana")
        creditos.setFont(QFont("Arial", 10))
        creditos.setStyleSheet("color: white; font-weight: bold; padding: 5px 0;")
        layout.addWidget(creditos)
    
        # Layout para os botões
        layout_botoes = QVBoxLayout()
        
        # Botão para o GitHub
        botao_github = QPushButton("Acessar meu GitHub")
        botao_github.clicked.connect(self.abrir_github)  # Conecta a função ao clique
        layout_botoes.addWidget(botao_github)
            
        # Doação texto
        texto_doacao = QLabel("Se gostou do app, considere fazer uma doação para apoiar o desenvolvimento!")
        texto_doacao.setFont(QFont("Arial", 9))
        texto_doacao.setStyleSheet("color: white; padding: 5px 0;")
        layout.addWidget(texto_doacao)
        
        # Botão para o Ko-fi
        botao_kofi = QPushButton("Fazer uma Doação")
        botao_kofi.clicked.connect(self.abrir_kofi)  # Conecta a função ao clique
        layout_botoes.addWidget(botao_kofi)
        
        # Adiciona os botões ao layout principal
        layout.addLayout(layout_botoes)

        self.setLayout(layout)
        self.set_dark_theme()

    # Função para abrir o GitHub
    def abrir_github(self):
        QDesktopServices.openUrl(QUrl("https://github.com/ThaynaSantana"))
    
    # Função para abrir o Ko-fi
    def abrir_kofi(self):
        QDesktopServices.openUrl(QUrl("https://ko-fi.com/thaynasantana"))

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2c3e50"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
        self.setPalette(palette)

    def button_style(self):
        return """
        QPushButton {
            background-color: #c0392b;
            color: white;
            font-size: 14px;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #e74c3c;
        }
        """

    def instalar_deb(self):
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar Pacote .deb", "", "Pacotes .deb (*.deb)")
        if not arquivo:
            self.logs.append("Nenhum pacote selecionado.")
            return
    
        self.logs.append(f"Iniciando instalação de: {arquivo}\n")
    
        try:
            process = subprocess.Popen(
                ["sudo", "dpkg", "-i", arquivo],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
    
            for linha in process.stdout:
                self.logs.append(linha.strip())
    
            process.wait()  # Aguarda a instalação terminar
    
            # 🔥 Novo método para verificar se o pacote foi instalado corretamente
            pacote_instalado = self.verificar_instalacao(arquivo)
    
            if pacote_instalado:
                self.logs.append("\n✅ Instalação concluída com sucesso!\n")
            else:
                self.logs.append("\n❌ Erro na instalação. Verifique os logs acima.\n")
    
        except Exception as e:
            self.logs.append(f"\n❌ Erro ao tentar instalar: {str(e)}\n")


    def remover_deb(self):
        pacote, ok = QInputDialog.getText(self, "Remover Pacote", "Digite o nome do pacote para remover:")
        
        if not ok or not pacote.strip():
            self.logs.append("\n⚠️ Nenhum pacote foi informado.\n")
            return
    
        # Verifica se o pacote está instalado
        status = subprocess.run(["dpkg", "-l", pacote], capture_output=True, text=True)
        if pacote not in status.stdout:
            self.logs.append(f"\n❌ O pacote '{pacote}' não está instalado.\n")
            return
    
        # Pergunta se quer remover completamente
        resposta, ok = QInputDialog.getItem(self, "Modo de Remoção", "Escolha o tipo de remoção:",
                                            ["Remover (Mantém configs)", "Purge (Remove tudo)"], 0, False)
        
        if not ok:
            return
    
        comando = ["sudo", "dpkg", "--remove", pacote] if resposta.startswith("Remover") else ["sudo", "dpkg", "--purge", pacote]
    
        self.logs.append(f"\n🔄 Removendo o pacote: {pacote} ({'Purge' if 'Purge' in resposta else 'Remove'})\n")
    
        try:
            process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
            for linha in process.stdout:
                self.logs.append(linha.strip())
    
            process.wait()
    
            if process.returncode == 0:
                self.logs.append(f"\n✅ Pacote '{pacote}' removido com sucesso!\n")
            else:
                self.logs.append(f"\n❌ Erro ao remover o pacote '{pacote}'. Verifique os logs acima.\n")
    
        except Exception as e:
            self.logs.append(f"\n❌ Erro ao tentar remover o pacote: {str(e)}\n")



    def verificar_instalacao(self, arquivo):
        # Obtém o nome do pacote a partir do arquivo .deb
        try:
            output = subprocess.check_output(["dpkg-deb", "--show", arquivo], text=True)
            pacote_nome = output.split()[0]  # Primeiro campo é o nome do pacote
    
            # Verifica se o pacote está instalado
            status = subprocess.run(["dpkg", "-l", pacote_nome], capture_output=True, text=True)
            return pacote_nome in status.stdout
    
        except Exception as e:
            self.logs.append(f"\n⚠️ Erro ao verificar instalação: {str(e)}\n")
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = DebmanApp()
    janela.show()
    sys.exit(app.exec())

