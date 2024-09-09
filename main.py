import tkinter as tk
from tkinter import ttk, Toplevel, PhotoImage
from PIL import Image, ImageTk
from login import Login
import platform
import json
import os
import instaloader
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import threading
from Vitoria_extract import Pesquisa_perfil


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.system = self.check_os()
        self.root.title("Interface Tkinter")
        self.root.geometry("800x600")
        self.username = ""
        self.password = ""

        # Divisão principal (esquerda 30% e direita 70%)
        self.frame_left = tk.Frame(self.root, bg="lightblue", width=240)
        self.frame_left.pack(side="left", fill="y")

        self.rodando = False
        self.popup= None
        self.appdata_path = ""
        #localiza a pasta com o json
        if self.system == 1:        
            self.appdata_path = os.path.join(os.getenv('LOCALAPPDATA'), 'vitoria_dados')
        if self.system == 2:
            self.appdata_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'vitoria_dados')
        self.file_path = os.path.join(self.appdata_path, 'login.json')

        # Certificar-se de que a pasta existe
        if not os.path.exists(self.appdata_path):
            os.makedirs(self.appdata_path)

        #carregar e exibir o usuário se tiver 
        self.frame_right = tk.Frame(self.root, bg="white")
        self.frame_right.pack(side="left", fill="both", expand=True)



        # Dentro do frame
        #  esquerdo, criando o "header" com inputs, imagem e botão
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
        self.right_header.pack(side="top", fill="x")
        self.tree = ttk.Treeview(self.frame_right, columns=("ID", "Usuário"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Usuário", text="Usuário")
        self.tree.pack(side="top",fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        users = self.carregar_usuarios("seguidores.json")
        for valor in users:
            self.tree.insert("", "end", values=(valor["id"], valor["user"]))

        # Exemplo de opções para o OptionMenu
        self.options = ["Pelo @", "Assunto", "Opção 3"]
        self.selected_option = tk.StringVar(value=self.options[0])
        
        # OptionMenu
        self.option_menu = tk.OptionMenu(self.right_header, self.selected_option, *self.options)
        self.option_menu.grid(row=0, column=0, padx=10, pady=10)
        self.button_seach = ttk.Button(self.right_header, text="Extrair", command=self.iniciar_atualizacao)
        self.button_seach.grid(row=0,  column=2, padx=10, pady=10, sticky="ew")


        original_image = Image.open("phone.png")  # Substitua pelo caminho da sua imagem
        resized_image = original_image.resize((15, 15))  # Redimensiona para 50x50 pixels
        self.image = ImageTk.PhotoImage(resized_image)
        # Entry
        self.entry_right = ttk.Entry(self.right_header)
        self.entry_right.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.botoes_extracao = tk.Frame(self.frame_right, bg="lightgray", height=100)
        self.botoes_extracao.pack(side="bottom", fill="x")
        self.extrair_numero = tk.Button(self.botoes_extracao, text="Extrair Números",image=self.image, compound="right", command=self.iniciar_extracao_numero)
        self.extrair_numero.pack(side="left", padx=5, pady=5)
        self.extrair_email = tk.Button(self.botoes_extracao, text="Extrair Emails")
        self.extrair_email.pack(side="left", padx=5, pady=5)
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.load_login_data()
    def fechar_janela(self):
        self.rodando = False
        # Desativa a flag para interromper a função de scraping
        self.root.destroy()
    def carregar_indice(self):
        try:
            with open("index.json", 'r') as file:
                   index =json.load(file)
                   return index["index"]
        except FileNotFoundError:
            return 0  

    def iniciar_atualizacao(self):
        # Iniciar o processo de atualização em uma thread separada
        self.thread = threading.Thread(target=self.extrari_usuarios_intaloader)
        self.thread.start()

    def iniciar_extracao_numero(self):
        # Iniciar o processo de atualização em uma thread separada
        self.thread = threading.Thread(target=self.pegar_numeros)
        self.thread.start()
    def atualizar_index(self,file_path, i):
        """Atualiza o valor do índice no arquivo JSON."""
        # Ler o conteúdo do arquivo
        def read_json_file(file_path):
            with open(file_path, 'r') as file:
                   return json.load(file)
        def write_json_file(file_path, data):
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

        data = read_json_file(file_path)
        
        # Atualizar o valor do índice
        if i =="end":
            data['index'] = 0
        else:
            data['index'] += 1
        
        # Escrever o conteúdo atualizado de volta no arquivo
        write_json_file(file_path, data)

    def extrari_usuarios_intaloader(self):
        self.rodando =True
        L = instaloader.Instaloader()
        user = None
        file_path = os.path.join(self.appdata_path, 'login.json')
            
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data.get('username') !=None or data.get('password')!=None:
                user = data.get('username')


        # Faça login (opcional, se precisar acessar perfis privados)
        L.load_session_from_file(user,"1_session")


        # Carregue um perfil
        try:
            profile = instaloader.Profile.from_username(L.context, self.entry_right.get())
            # Exiba algumas informações do perfil
            #print(s)
            seguidores = profile.get_followees()

            lista = []
            self.tree.delete(*self.tree.get_children())
            while self.rodando: 
                for seguidor in seguidores:
                    if len(lista) ==500 or self.rodando ==False:
                        break
                    else:
                        index_json ={"id":"","user":""}
                        try:
                            time.sleep(0.7)
                            nome = seguidor.username
                            
                            index_json["id"] = seguidor.userid
                            index_json["user"] = nome
                            print(index_json)
                            lista.append(index_json)
                            self.tree.insert("", "end", values=(index_json["id"], index_json["user"]))
                            with open('seguidores.json', 'w') as file:
                                json.dump(lista, file, indent=4)
                        except:
                            print("deu erro")
            with open('seguidores.json', 'w') as file:
                json.dump(lista, file, indent=4)
        except Exception as er:
            if str(er).find("challenge") != -1:
                self.contingencia(self.entry_right.get(), self.extrari_usuarios_intaloader)
                time.sleep(1)
    def pegar_numeros(self):
        def atulizar_linhas_grafico(linha_user, linha_numero):
            self.tree.insert("", "end", values=(linha_user, linha_numero))
        
        self.tree.delete(*self.tree.get_children())
        api = Pesquisa_perfil(self.entry_right.get(), self.username, self.password)
        api.pegar_numeros(atulizar_linhas_grafico)
    def carregar_usuarios(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    def mostrar_popup(self):
        # Cria uma nova janela Toplevel
        self.popup = Toplevel()
        self.popup.title("Aguarde")
        
        # Configura o tamanho da janela
        self.popup.geometry("200x100")
        
        # Exibe a mensagem "Aguarde" no popup
        label = tk.Label(self.popup, text="Aguarde...")
        label.pack(pady=20)
        
        # O popup permanece até que seja fechado
        self.popup.transient(root)  # Mantém o popup acima da janela principal
        self.popup.grab_set()       # Bloqueia interações com a janela principal enquanto o popup está aberto
        self.root.wait_window(self.popup) 
    def fechar_popup(self):
        self.popup.destroy()  # Fecha o popup
        self.popup = None 
    def load_login_data(self):
        # Verificar se o arquivo JSON existe
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.username = data.get('username')
                self.password = data.get('password')
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
            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(resized_image)
            self.img_label.config(image=self.img_tk)
    def check_os(self):
        system = platform.system()
        if system == 'Windows':
            return 1
        elif system == 'Darwin':
            return 2
        elif system == 'Linux':
            return 3
        else:
            return 0

    def login(self):
        usuario = self.entry_user.get()
        senha = self.entry_pass.get()
        result = result =Login(usuario, senha)
        self.mostrar_popup()
        if result ==3:
            self.error_label.config(text="Por favor, preencha todos os campos.")
            self.fechar_popup()
        if result ==2:
            self.msg_label = tk.Label(self.header, text="Ocorreu um erro ao fazer login", bg="lightgray", font=("Arial", 12))
            self.msg_label.grid(row=1, columnspan=2, padx=10, pady=10)
            self.fechar_popup()
        else:
            self.salvar_login(usuario, senha)
            self.exibir_user(usuario)
            self.fechar_popup()
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
    def contingencia(self, target, function):
        url = f"https://i.instagram.com/challenge/?next=/api/v1/users/{target}/usernameinfo/"
        driver = webdriver.Chrome()
        driver.get(url)

        try:
            time.sleep(5)
            # Espera até que o campo de username esteja presente e interativo
            campo_username = driver.find_element(By.NAME, 'username')
            campo_username.send_keys(self.username) 
            time.sleep(0.6)
            campo_password = driver.find_element(By.NAME, 'password')
            campo_password.send_keys(self.password)
            time.sleep(0.6)
            botao_login = driver.find_element(By.XPATH, '//button[@type="submit"]')
            botao_login.click()
            try:
                print("passou 1")
                driver.find_element(By.XPATH, '//span[text()="Ajude-nos a confirmar que é você"]')
                print("passou 2")
                self.popup = Toplevel()
                self.popup.title("Aguarde")
                print("passou 3")
                # Configura o tamanho da janela
                self.popup.geometry("200x100")
                print("passou 4")
                # Exibe a mensagem "Aguarde" no popup
                label = tk.Label(self.popup, text="Faça o capcha no seu celular!!")
                label.pack(pady=20)
                driver.quit()  
                print("passou 4")      


            except NoSuchElementException:
                # Espera até que o botão "ignorar" esteja presente e clicável
                span_ignorar = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="Ignorar"]'))
                )
                span_ignorar.click()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            # Opcional: Fechar o navegador após o login
            time.sleep(20)  # Dê tempo para observar o resultado antes de fechar
            driver.quit()
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()