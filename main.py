import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from login import Login
import json
import os

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Tkinter")
        self.root.geometry("800x600")

        # Divisão principal (esquerda 30% e direita 70%)
        self.frame_left = tk.Frame(self.root, bg="lightblue", width=240)
        self.frame_left.pack(side="left", fill="y")

        #localiza a pasta com o json
        self.appdata_path = os.path.join(os.getenv('LOCALAPPDATA'), 'vitoria_dados')
        self.file_path = os.path.join(self.appdata_path, 'login.json')

        # Certificar-se de que a pasta existe
        if not os.path.exists(self.appdata_path):
            os.makedirs(self.appdata_path)

        #carregar e exibir o usuário se tiver 
        self.frame_right = tk.Frame(self.root, bg="white")
        self.frame_right.pack(side="right", fill="both", expand=True)

        # Dentro do frame esquerdo, criando o "header" com inputs, imagem e botão
        self.header = tk.Frame(self.frame_left, bg="lightgray", height=100)
        self.header.pack(fill="x")

        # Bind para redimensionar a imagem quando a janela for redimensionada
        self.header.bind("<Configure>", self.resize_image)

        # Carregar a imagem original apenas uma vez
        self.original_image = Image.open("logo.png")
        self.img_label = tk.Label(self.header, bg="lightgray")
        self.img_label.grid(row=0, columnspan=2, pady=10)

        # Label e campo de entrada para o usuário
        self.label_user = tk.Label(self.header, text="Usuário:", bg="lightgray")
        self.label_user.grid(row=1, column=0, padx=10, pady=10)

        self.entry_user = ttk.Entry(self.header)
        self.entry_user.grid(row=1, column=1, padx=10, pady=10)

        # Label e campo de entrada para a senha
        self.label_pass = tk.Label(self.header, text="Senha:", bg="lightgray")
        self.label_pass.grid(row=2, column=0, padx=10, pady=10)

        self.entry_pass = ttk.Entry(self.header, show="*")
        self.entry_pass.grid(row=2, column=1, padx=10, pady=10)

        # Botão de login
        self.button_login = ttk.Button(self.header, text="Login", command=self.login)
        self.button_login.grid(row=3, columnspan=2, pady=10)
        self.error_label = tk.Label(self.header, text="", fg="red", bg="lightgray")
        self.error_label.grid(row=4, columnspan=2)
        self.right_header = tk.Frame(self.frame_right, bg="lightgray", height=100)
        self.right_header.pack(fill="x")

        # Exemplo de opções para o OptionMenu
        self.options = ["Pelo @", "Assunto", "Opção 3"]
        self.selected_option = tk.StringVar(value=self.options[0])
        
        # OptionMenu
        self.option_menu = tk.OptionMenu(self.right_header, self.selected_option, *self.options)
        self.option_menu.grid(row=0, column=0, padx=10, pady=10)
        self.button_seach = ttk.Button(self.right_header, text="Extrair", command=self.login)
        self.button_seach.grid(row=3,  column=1, padx=10, pady=10, sticky="ew")

        # Entry
        self.entry_right = ttk.Entry(self.right_header)
        self.entry_right.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.load_login_data()

    def load_login_data(self):
        # Verificar se o arquivo JSON existe
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.username = data.get('username')
                if data.get('username') !=None or data.get('password')!=None:
                    self.exibir_user(data.get('username'))
        else:
            with open(self.file_path, 'w') as file:
                json.dump({'username': None, 'password': None}, file)
            self.username = None
            self.password = None
    def salvar_login(self, username,password):
        # Verificar se o arquivo JSON existe
        with open(self.file_path, 'w') as file:
            json.dump({'username': username, 'password': password}, file)
            
    def resize_image(self, event):
        # Verifica se a largura realmente mudou antes de redimensionar
        if event.width > 0:
            # Obter a largura atual do header e redimensionar a imagem para caber
            new_width = event.width
            new_height = int(self.original_image.height * new_width / self.original_image.width)

            # Limitar o tamanho máximo da imagem (opcional)
            max_height = 150  # Defina o limite de altura máxima
            if new_height > max_height:
                new_height = max_height
                new_width = int(self.original_image.width * max_height / self.original_image.height)

            # Redimensionar a imagem e atualizar o label
            resized_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.img_tk = ImageTk.PhotoImage(resized_image)
            self.img_label.config(image=self.img_tk)

    def login(self):
        usuario = self.entry_user.get()
        senha = self.entry_pass.get()
        result = result =Login(usuario, senha)
        if result ==3:
            self.error_label.config(text="Por favor, preencha todos os campos.")
        if result ==2:
            self.msg_label = tk.Label(self.header, text="Ocorreu um erro ao fazer login", bg="lightgray", font=("Arial", 12))
            self.msg_label.grid(row=1, columnspan=2, padx=10, pady=10)
        else:
            self.salvar_login(usuario, senha)
            self.exibir_user(usuario)
    def exibir_user(self, user):
        if self.label_user:
            self.label_user.destroy()
        if self.entry_user:
            self.entry_user.destroy()
        if self.label_pass:
            self.label_pass.destroy()
        if self.entry_pass:
            self.entry_pass.destroy()
        if self.button_login:
            self.button_login.destroy()

        # Exibir o nome do usuário
        self.msg_label = tk.Label(self.header, text=f"{user}", bg="lightgray", font=("Arial", 12))
        self.msg_label.grid(row=1, columnspan=2, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
