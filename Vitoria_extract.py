import json
import sys
import os
import codecs
from pathlib import Path
import time
import random
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Substitua pelo caminho para o seu WebDriver
caminho_chromedriver = '/caminho/para/chromedriver'

import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from instagram_private_api import Client as AppClient
from instagram_private_api import ClientCookieExpiredError, ClientLoginRequiredError, ClientError, ClientThrottledError, ClientChallengeRequiredError, ClientConnectionError



class Pesquisa_perfil:
    api = None
    api2 = None
    user_id = None
    target_id = None
    is_private = True
    following = False
    target = ""
    numero_de_seguidores= 0
    array_de_seguidores= 0
    writeFile = False
    jsonDump = False
    cli_mode = False
    output_dir = "output"
    t =""
    u = ""
    s = ""
    def __init__(self, target, usuario, senha):
        self.t =target
        self.u = usuario
        self.s = senha
        #definir variaveis d usuário
        self.login(usuario, senha)
        self.setTarget(target)

    def login(self, user, senha):
        settings_file = "ig_session.json"

        if not os.path.isfile(settings_file):

            # settings file does not exist
            print('Fazendo um novo login')
            try:
                self.api = AppClient(auto_patch=True, authenticate=True, username=user, password=senha, on_login=lambda x: self.armazenar_login(x, settings_file))
                print(self.api.current_user())

            except Exception as e:
                if str(e).find("challenge") != -1:
                    self.contingencia2()
        else:
            print('Usando login Existente')
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=self.from_json)
            # print('Reusing settings: {0!s}'.format(settings_file))
            try:
                self.api = AppClient(username=user, password=senha,settings=cached_settings,on_login=lambda x: self.armazenar_login(x, settings_file))
                print(self.api.current_user())
            except Exception as e:
                if str(e).find("login") != -1:
                    print("Vamos exectuar um novo login")
                    os.remove("ig_session.json")
                    time.sleep(3)
                    self.__init__(self.t, self.u, self.s)
                    self.pegar_numeros()
                if str(e).find("challenge") != -1:
                    self.contingencia1()

    def contingencia2(self):
        url = f"https://i.instagram.com/challenge/?next=/api/v1/users/{self.target}/usernameinfo/"
        driver = webdriver.Chrome()
        # Abrir a URL no navegador
        driver.get(url)
        time.sleep(5)
        campo_username = driver.find_element(By.NAME, 'username')
        campo_username.send_keys(self.u) 
        time.sleep(0.6)
        campo_password = driver.find_element(By.NAME, 'password')
        campo_password.send_keys(self.s)
        time.sleep(0.6)
        botao_login = driver.find_element(By.XPATH, '//button[@type="submit"]')
        botao_login.click()
        wait = WebDriverWait(driver, 20)
        span_ignorar = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Ignorar"]'))
        )
        # Clicar no botão "ignorar"
        span_ignorar.click()
        time.sleep(0.6)
        os.remove("ig_session.json")
        time.sleep(0.6)
        self.login(self.u, self.s)

    def contingencia1(self):
        url = f"https://i.instagram.com/challenge/?next=/api/v1/users/{self.target}/usernameinfo/"
        driver = webdriver.Chrome()
        # Abrir a URL no navegador
        driver.get(url)
        time.sleep(5)
        campo_username = driver.find_element(By.NAME, 'username')
        campo_username.send_keys(self.u) 
        time.sleep(0.6)
        campo_password = driver.find_element(By.NAME, 'password')
        campo_password.send_keys(self.s)
        time.sleep(0.6)
        botao_login = driver.find_element(By.XPATH, '//button[@type="submit"]')
        botao_login.click()
        wait = WebDriverWait(driver, 20)
        span_ignorar = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="button"]'))
        )
        # Clicar no botão "ignorar"
        span_ignorar.click()
        self.login(self.u, self.s)

    def armazenar_login(self, api, new_settings_file):
        cache_settings = api.settings
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object
    def checar_perfil_privado(self):
        if self.is_private:
            send = input("Do you want send a follow request? [Y/N]: ")
            if send.lower() == "y":
                self.api.friendships_create(self.target_id)
                print("Sent a follow request to target. Use this command after target accepting the request.")

            return True
        return False
    def generate_random_float(self,min_value, max_value, decimal_places):
        # Define o range e o passo baseado nas casas decimais
        step = 10 ** -decimal_places
        
        # Gera um valor randômico inteiro dentro do range ajustado
        random_int = random.randint(int(min_value / step), int(max_value / step))
        
        # Converte o valor randômico inteiro de volta para float
        random_float = random_int * step
        
        return random_float
    def pegar_seguidores(self):
        try:
            print("Pesquisando os seguidores aguarde..")
            lista_de_seguidores = []

            rank_token = AppClient.generate_uuid()
            
            seguindo = self.api.user_followers(str(self.target_id), rank_token=rank_token)
            user = self.api.user_info(self.target_id)
            print(seguindo.get('users', []))
            for seguidores in seguindo.get('users', []):
                lista_de_seguidores.append(seguidores['username'])
                print(seguidores['username'])
                time.sleep(0.5)

            maximo_de_perfis= seguindo.get('next_max_id')
            while int(maximo_de_perfis)< int(self.numero_de_seguidores):
                print(maximo_de_perfis)                
                time.sleep(5)

                results = self.api.user_followers(str(self.target_id), rank_token=rank_token, max_id=maximo_de_perfis)
                for user in results.get('users', []):
                    lista_de_seguidores.append(user['username'])
                    print(user['username'])
                    time.sleep(0.5)

                maximo_de_perfis = results.get('next_max_id')
            
            print("\n")   
        except ClientThrottledError as e:
            print("O instagram bloqueou sua requisição tente denovo em alguns minutos")
        except ClientError as err:
            print("deu erro")
 
    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def pegar_numeros(self):
        numeros = self.pegar_lista_num()
        try:
            print("Pesquisando os numeros aguarde..")
            with open("seguidores.json", 'r') as file:
                self.array_de_seguidores = json.load(file) 
                print("Carregamento Concluido!")
            lista_de_seguidores = []
            count =self.carregar_indice()

            for seg in range(count, len(self.array_de_seguidores)-1):
                count=count+1
                self.atualizr_index("index.json", "start")
                time.sleep(self.generate_random_float(1, 5, 1))
                user = self.api.user_info(self.array_de_seguidores[count]['id'])
                if 'contact_phone_number' in user['user']:
                    if(user['user']['contact_phone_number']!= ""):
                        print(user['user']['full_name'] +'e'+ user['user']['contact_phone_number'])
                        numeros["num"].append([user['user']['full_name'], user['user']['contact_phone_number']])
                        time.sleep(0.5)
                        lista_de_seguidores.append(user['user']['contact_phone_number'])
                time.sleep(0.3)
            self.atualizr_index("index.json", "end")
            self.atualizar_numero(numeros)
        except ClientChallengeRequiredError as er:
            print("deu erro1")
            self.atualizar_numero(numeros)
            os.remove("ig_session.json")
            print(err)
        except ClientThrottledError as err:
            print("deu erro2")
            self.atualizar_numero(numeros)
            os.remove("ig_session.json")
            print(err)
        except ClientLoginRequiredError as er:
            print("deu erro3")
            self.atualizar_numero(numeros)
            os.remove("ig_session.json")
            print(er)
        except ClientCookieExpiredError as er:
            print("deu erro4")
            self.atualizar_numero(numeros)            
            print(er)
        except ClientConnectionError as er:
            print("deu erro5")
            self.atualizar_numero(numeros)            
            print(er)
        except ClientError as err:
            print("deu erro6")
            print(err)
            self.atualizar_numero(numeros)
            if str(err).find("login") != -1:
                self.login(self.u, self.s)
            if str(err).find("Unauthorized:") != -1:
                os.remove("ig_session.json")
                self.login(self.u, self.s)
            if str(err).find("challenge") != -1:
                self.contingencia1()
                self.pegar_numeros()
    def carregar_indice(self):
        try:
            with open("index.json", 'r') as file:
                   index =json.load(file)
                   return index["index"]
        except FileNotFoundError:
            return 0  

    def setTarget(self, target):
        self.target = target
        user = self.pegar_usuario(target)
        self.target_id = user['user']['pk']
        self.numero_de_seguidores = user['user']['follower_count']
        self.is_private = False
        self.output_dir = self.output_dir + "/" + str(self.target)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    def pegar_usuario(self, username):
        try:
            content = self.api.username_info(username)
            if content['user']['is_private'] ==False:
                return content
            else:
                return "PRIVADO"
        except ClientError as e:
            error = json.loads(e.error_response)
            if 'message' in error:
                print(error['message'])
            if 'error_title' in error:
                print(error['error_title'])
            if 'challenge' in error:
                print("Please follow this link to complete the challenge: " + error['challenge']['url'])    
            sys.exit(2)


    def atualizr_index(self,file_path, i):
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
    def pegar_lista_num(self):
        """Atualiza o valor do índice no arquivo JSON."""
        # Ler o conteúdo do arquivo
        file_path = "user_contact.json"
        with open(file_path, 'r') as file:
            return json.load(file)

    def atualizar_numero(self,data):
        """Atualiza o valor do índice no arquivo JSON."""
        # Ler o conteúdo do arquivo
        file_path = "user_contact.json"
        def write_json_file(file_path, data):
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        
        # Escrever o conteúdo atualizado de volta no arquivo
        write_json_file(file_path, data)
