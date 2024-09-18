import tkinter as tk
from tkinter import ttk, Toplevel, PhotoImage
from lxml import etree
from tkinter.filedialog import asksaveasfilename
from xml.dom import minidom
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
from selenium.common.exceptions import TimeoutException
import threading
import pandas as pd
from Vitoria_extract import Pesquisa_perfil


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.system = self.check_os()
        self.root.title("Vitoria")
        self.root.geometry("1000x600")
        self.username = ""
        self.password = ""
        self.lista_seguidores = False

        # Divisão principal (esquerda 30% e direita 70%)
        self.frame_left = tk.Frame(self.root, bg="lightblue", width=240)
        self.frame_left.pack(side="left", fill="y")

        self.rodando = False
        self.popup= None
        self.popup2= None
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
        #Lado direito

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
        #botao para exportar excel
        self.exportar_xls = ttk.Button(self.frame_right, text="Exportar Lista", command=self.exportar_numeros)
        self.exportar_xls.pack(pady=1, fill="y", expand=False)
        #Barra de progresso
        self.progress = ttk.Progressbar(self.frame_right, orient="horizontal", length=100, mode="determinate")
        self.progress.pack(pady=1, fill="x", expand=False)
        self.progress["value"] = 0
        self.max_value = 100
        self.progress["maximum"] = self.max_value
        #Esse tree é para os seguidores
        self.tree = ttk.Treeview(self.frame_right, columns=("Ordem","ID", "Usuário"), show="headings")
        self.tree.heading("Ordem", text="Ordem")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Usuário", text="Usuário")
        self.tree.pack(side="top",fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        #Esse tree é para os números
        self.tree2 = ttk.Treeview(self.frame_right, columns=("Ordem","Usuário", "Número"), show="headings")
        self.tree2.heading("Ordem", text="Ordem")
        self.tree2.heading("Usuário", text="Usuário")
        self.tree2.heading("Número", text="Número")
        self.tree2.pack(side="top",fill="both", expand=True)
        self.scrollbar2 = ttk.Scrollbar(self.tree2, orient="vertical", command=self.tree2.yview)
        self.tree2.configure(yscroll=self.scrollbar.set)
        self.scrollbar2.pack(side="right", fill="y")
        self.tree2.pack_forget()

        users = self.carregar_usuarios("seguidores.json")
        cont= 1
        for valor in users:
            self.tree.insert("", "end", values=(cont,valor["id"], valor["user"]))
            cont+=1

        # Exemplo de opções para o OptionMenu
        self.options = ["Pelo @", "Assunto", "Opção 3"]
        self.selected_option = tk.StringVar(value=self.options[0])
        
        # OptionMenu
        self.option_menu = tk.OptionMenu(self.right_header, self.selected_option, *self.options)
        self.option_menu.grid(row=0, column=0, padx=10, pady=10)
        self.button_seach = ttk.Button(self.right_header, text="Extrair", command=lambda:self.iniciar_atualizacao(False))
        self.button_seach.grid(row=0,  column=2, padx=10, pady=10, sticky="ew")
        self.numeric_spinbox = tk.Spinbox(self.right_header, from_=0, to=10000000)  # Valores de 0 a 100
        self.numeric_spinbox.grid(row=0,  column=3, padx=10, pady=10, sticky="ew")


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
        self.ver_numero = tk.Button(self.botoes_extracao, text="Ver Números",image=self.image, compound="right", command=self.mostrar_números)
        self.ver_numero.pack(side="left", padx=5, pady=5)
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
    def iniciar_login(self,check):
        # Iniciar o processo de atualização em uma thread separada
        self.thread = threading.Thread(target=self.iniciar_login)
        self.thread.start()
    def iniciar_atualizacao(self,check):
        # Iniciar o processo de atualização em uma thread separada
        self.thread = threading.Thread(target=lambda:self.extrari_usuarios_intaloader(check))
        self.thread.start()
    def iniciar_extracao_numero(self):
        # Iniciar o processo de atualização em uma thread separada
        self.thread = threading.Thread(target=self.pegar_numeros)
        self.thread.start()
    def definir_usuario(self,file_path, target):
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
        data['user'] = target
        # Escrever o conteúdo atualizado de volta no arquivo
        write_json_file(file_path, data)
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
    def extrari_usuarios_intaloader(self,check):
        self.tree2.pack_forget()
        self.tree.pack(side="top",fill="both", expand=True)
        self.definir_usuario("target_user.json", self.entry_right.get())
        if self.entry_right.get() =="" or self.entry_right.get() == None:
            self.popop_custom("Digite um @")
        else:
            self.lista_seguidores = check
            self.rodando = True
            L = instaloader.Instaloader()
            user = None
            file_path = os.path.join(self.appdata_path, 'login.json')
            with open(file_path, 'r') as file:
                data = json.load(file)
                if data.get('username') !=None or data.get('password')!=None:
                    user = data.get('username')
            print(self.entry_right.get())
            if os.path.isfile("1_session"):
                L.load_session_from_file(user,"1_session")
            else:
                result = Login(self.username, self.password)
                time.sleep(1)
                if result ==1:
                    L.load_session_from_file(user,"1_session")
            # Faça login (opcional, se precisar acessar perfis privados)
            # Carregue um perfil
            try:
                cont= 1
                profile = instaloader.Profile.from_username(L.context, self.entry_right.get())
                # Exiba algumas informações do perfil
                #print(s)
                self.usuario_indexador = 0
                if check==False:
                    with open('seguidores.json', 'w') as file:
                        json.dump([], file, indent=4)
                else:
                   with open('target_seguidor.json', 'r') as file:
                        carregamento_json = json.load(file)
                        self.usuario_indexador = carregamento_json["id"]
                lista = []
                print("chegou aqui?")
                seguidores = profile.get_followers()
                if int(self.numeric_spinbox.get()) >=int(seguidores._data["count"]):
                        self.popop_custom("O número de seguidores que voce quer é maior que o número de seguidores deste perfil")
                else:
                    self.progress["maximum"] =int(self.numeric_spinbox.get())
                    if self.lista_seguidores == True:
                        with open('seguidores.json', 'r') as file:
                            lista= json.load(file)
                    else:
                        self.tree.delete(*self.tree.get_children())
                    if seguidores._data["edges"] == []:
                        os.remove("1_session")
                        time.sleep(1)
                        Login(self.username, self.password)
                        time.sleep(1)
                        self.iniciar_atualizacao(True)
                    else:
                        while self.rodando:
                            for seguidor in seguidores:                                    
                                if len(lista) >=int(self.numeric_spinbox.get() or self.rodando ==False):
                                    print("quebrou")
                                    self.salvar_usuario_atual({"id":cont})
                                    if len(lista) >=int(self.numeric_spinbox.get()):
                                        self.lista_seguidores == False
                                        self.rodando= False
                                        L= None
                                        break
                                    if self.rodando ==False:
                                        break
                                else:
                                    index_json ={"id":"","user":""}
                                    try:
                                        time.sleep(0.7)
                                        cont+=1
                                        if cont >=self.usuario_indexador:
                                            nome = seguidor.username
                                            index_json["id"] = seguidor.userid
                                            index_json["user"] = nome
                                            print(index_json)
                                            lista.append(index_json)
                                            self.tree.insert("", "end", values=(cont, index_json["id"], index_json["user"]))
                                            valor_barra = self.progress["value"]
                                            self.progress["value"] =valor_barra+1
                                            with open('seguidores.json', 'w') as file:
                                                json.dump(lista, file, indent=4)
                                    except Exception as ja_nao_sei_o_que_e:
                                        print(ja_nao_sei_o_que_e)
                                        self.salvar_usuario_atual({"id":cont})
                                        print("deu erro")
                        self.salvar_usuario_atual({"id":cont})
                        with open('seguidores.json', 'w') as file:
                            json.dump(lista, file, indent=4)
            except Exception as er:
                print(er)
                self.salvar_usuario_atual({"id":cont})
                if str(er).find("challenge") != -1:
                    print("Detectou o desafio")
                    self.contingencia(self.entry_right.get(), self.extrari_usuarios_intaloader)
                    time.sleep(1)
                if str(er).find("checkpoint") != -1:
                    print("Detectou o desafio")
                    self.contingencia(self.entry_right.get(), self.extrari_usuarios_intaloader)
                    time.sleep(1)
                if str(er).find("few minutes") != -1:
                    print("Detectou o erro de espera")
                    os.remove("1_session")
                    time.sleep(1)
                    self.iniciar_atualizacao(True)
    def exportar_numeros(self):
        data = self.carregar_usuarios("user_contact.json")
        self.arroba = {}
        with open("target_user.json", 'r') as file:
            self.arroba= json.load(file)
        nome = self.arroba["user"] +"_contatos"

        # Converter o JSON para um DataFrame
        df = pd.DataFrame(data['num'], columns=['Nome', 'Número'])
        df = df[['Número', 'Nome']]
        # Abre o diálogo para salvar o arquivo
        caminho_arquivo = asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")],
            initialfile=nome,
            title="Escolha o local para salvar o arquivo"
        )
        if caminho_arquivo:
            # Salva o DataFrame em um arquivo Excel
            df.to_excel(caminho_arquivo, index=False,  header=False,engine='openpyxl')
            print("Planilha criada com sucesso!")
        # Salvar o DataFrame em um arquivo Excel
    def mostrar_números(self):
        self.tree2.pack(side="top",fill="both", expand=True)
        users = self.carregar_usuarios("user_contact.json")
        cont= 1
        def puxar_numero_seguidores():
            with open("seguidores.json", "r") as file:
                return len(json.load(file))
        self.progress["maximum"] =puxar_numero_seguidores()
        for valor in users["num"]:
            self.tree2.insert("", "end", values=(cont,valor[0], valor[1]))
            cont+=1
        self.tree.pack_forget()
    def salvar_usuario_atual(self, user):
        with open('target_seguidor.json', 'w') as file:
            json.dump(user, file, indent=4)


    def pegar_numeros(self):
        self.tree2.pack(side="top",fill="both", expand=True)
        users = self.carregar_usuarios("user_contact.json")
        cont= 1
        def puxar_numero_seguidores():
            with open("seguidores.json", "r") as file:
                return len(json.load(file))
        self.progress["maximum"] =puxar_numero_seguidores()

        for valor in users["num"]:
            self.tree2.insert("", "end", values=(cont,valor[0], valor[1]))
            cont+=1
        def atualizar_percentual():
            valor = self.progress["value"]
            self.progress["value"]=valor+1

        def atulizar_linhas_grafico(linha_user, linha_numero):
            valor = self.progress["value"]
            self.progress["value"]=valor+1
            self.tree2.insert("", "end", values=(1, linha_user, linha_numero))
        self.tree.pack_forget()
        arroba = ""
        with open("target_user.json", 'r') as file:
            arroba= json.load(file)
        self.tree2.delete(*self.tree2.get_children())
        api = Pesquisa_perfil(arroba["user"], self.username, self.password)
        result = api.pegar_numeros(atulizar_linhas_grafico, atualizar_percentual,False )
        print(result)
    def carregar_usuarios(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    def popop_custom(self, message):
        def popup(m):
            self.popup2 = Toplevel()
            self.popup2.title("Aguarde")
            
            # Configura o tamanho da janela
            self.popup2.geometry("300x200")
            
            # Exibe a mensagem "Aguarde" no popup
            label = tk.Label(self.popup2, text=m,  wraplength=270, padx=10, pady=10)
            label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            def close_popup():
                self.popup2.destroy()
            
            close_button = tk.Button(self.popup2, text="OK", command=close_popup)
            close_button.pack(pady=10)
            # O popup permanece at é que seja fechado
            self.popup2.transient(root)  # Mantém o popup acima da janela principal
            self.popup2.grab_set()       # Bloqueia interações com a janela principal enquanto o popup está aberto
            self.root.wait_window(self.popup2) 

        self.thread2 = threading.Thread(target=lambda:popup(message))
        self.thread2.start()

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
                if data.get('username') != "" and data.get('password') != "":
                    self.username = data.get('username')
                    self.password = data.get('password')
                    if data.get('username') !=None or data.get('password')!=None:
                        self.exibir_user(data.get('username'))
                else:
                    with open(self.file_path, 'w') as file:
                        json.dump({'username': None, 'password': None}, file)
                        self.username = None
                        self.password = None

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
        if result ==0:
            self.error_label.config(text="Por favor, preencha todos os campos.")
            self.fechar_popup()
        if result ==2:
            self.error_label.config(text="")
            self.popop_custom("Esse perfil esta pedindo Teste Capcha ou verficacão de Email")
        if result ==3:
            self.error_label.config(text="")
            self.popop_custom("A senha está errada")
        if result ==4:
            self.error_label.config(text="")
            self.popop_custom("Ocorreu um erro ao tentar fazer login")
        if result ==1:
            self.error_label.config(text="")
            self.salvar_login(usuario, senha)
            self.exibir_user(usuario)
            self.fechar_popup()
    def logout(self):
        with open(self.file_path, 'w') as file:
            json.dump({'username': "", 'password': ""}, file)
        self.reiniciar()


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
        self.deslogar = tk.Button(self.header, text="Deslogar", bg="red", command=self.logout)
        self.deslogar.grid(row=2, columnspan=2, padx=10, pady=10)
    def reiniciar(self):
        global root
        # Destruir a janela principal atual
        root.destroy()
        # Criar uma nova janela principal
        root = tk.Tk()
        app = LoginApp(root)
        root.mainloop()
    def contingencia(self, target, function):
        url = f"https://i.instagram.com/challenge/?next=/api/v1/users/{target}/usernameinfo/"
        driver = webdriver.Chrome()
        retornar = True
        driver.get(url)
        try:
            time.sleep(5)
            print("testando1")
            # Espera até que o campo de username esteja presente e interativo
            campo_username = driver.find_element(By.NAME, 'username')
            campo_username.send_keys(self.username) 
            time.sleep(0.6)
            print("testando2")
            campo_password = driver.find_element(By.NAME, 'password')
            campo_password.send_keys(self.password)
            time.sleep(0.6)
            print("testando3")
            botao_login = driver.find_element(By.XPATH, '//button[@type="submit"]')
            botao_login.click()
            try:
                ignorar = self.elemento_presente(driver,'//span[text()="Ignorar"]')
                print(len(ignorar))
                time.sleep(1)
                if ignorar == False:
                    ajude_nos = driver.find_elements(By.XPATH, '//span[text()="Ajude-nos a confirmar que é você"]')
                    time.sleep(1)
                    if len(ajude_nos) ==0:
                        verificacao_email = driver.find_elements(By.XPATH, '//h2[text()="Detectamos uma tentativa de login incomum"]')
                        time.sleep(0.4)
                        if len(verificacao_email) ==0:
                            apelacao = driver.find_elements(By.XPATH, '//span[text()="Fazer uma apelação"]')
                            time.sleep(0.4)
                            print(len(apelacao))
                            if len(apelacao) ==0:
                                driver.quit()
                                self.popop_custom("Infelizmente esse perfil parece ter sido suspenso :,)")
                                retornar =False
                        else:
                            driver.quit()
                            self.popop_custom("Perfil está pedindo verificae Email ou Telefone)")
                            retornar =False
                    else:
                        ignorar2 = driver.find_element(By.XPATH, '//span[text()="Ignorar"]')
                        ignorar2.click()
                else:
                    driver.quit()
                    retornar =True


                print("passou 2")
                
                self.popup = Toplevel()
                self.popup.title("Aguarde")
                print("passou 3")
                # Configura o tamanho da janela
                self.popup.geometry("200x100")
                print("passou 4")
                # Exibe a mensagem "Aguarde" no popup
                driver.quit()  
                print("passou 4")     
            except NoSuchElementException as teste:
                print(f"Ocorreu um erro: {teste}")
                # Espera até que o botão "ignorar" esteja presente e clicável
                span_ignorar = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="Ignorar"]'))
                )
                span_ignorar.click()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            # Opcional: Fechar o navegador após o login
            time.sleep(2)  # Dê tempo para observar o resultado antes de fechar
            driver.quit()
            if retornar == True:
                function(True)
    def elemento_presente(self,driver, xpath):
        try:
            span_ignorar = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            span_ignorar.click()
            return True
        except TimeoutException:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()