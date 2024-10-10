import requests
import json
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random

class Vitoria:
    senha =None
    usuario = None
    def __init__(self, u, s):
        self.senha = s
        self.usuario = u

    def retornar_(self,c, nome):
        for cookie in c:
            if cookie['name'] == nome:
                return cookie['value']

    def login(self):
        valores = False
        js ={}
        with open("coockie.json", "r") as file:
            js = json.load(file)
            if js["coockie"] != "":
                valores = True
        if valores == False:
            driver = webdriver.Chrome()
            driver.get("https://www.instagram.com/accounts/login/")

            # Espera a página carregar
            time.sleep(3)

            # Localiza os campos de login e senha
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")

            # Preenche os campos
            username_input.send_keys(self.usuario)
            password_input.send_keys(self.senha)

            # Envia o formulário
            password_input.send_keys(Keys.RETURN)

            # Espera um pouco para garantir que o login foi feito
            time.sleep(8)
            #chegagem de verificação
            checkout_numero_email = len(driver.find_elements(By.ID, "choice_0"))
            checkout_ignorar = len(driver.find_elements(By.XPATH, '//span[text()="Ignorar"]'))
            checkout_capcha = len(driver.find_elements(By.XPATH, '//span[text()="Ajude-nos a confirmar que é você"]'))
            if checkout_numero_email > 0:
                print("Faça Checkout do seu numero ou email")
                while checkout_numero_email > 0:
                    print("ainda esperando")
                    time.sleep(6)
            if checkout_ignorar>0:
                ignorar2 = driver.find_element(By.XPATH, '//span[text()="Ignorar"]')
                ignorar2.click()
            if checkout_capcha>0:
                print("Faça Checkout do capcha")
                while checkout_capcha > 0:
                    time.sleep(6)

            # Obtém os cookies
            cookies = driver.get_cookies()
            mid= self.retornar_(cookies, "mid")
            datr= self.retornar_(cookies, "datr")
            ig_did= self.retornar_(cookies, "ig_did")
            csrftoken= self.retornar_(cookies, "csrftoken")
            ds_user_id=self.retornar_(cookies, "ds_user_id")
            sessionid=self.retornar_(cookies, "sessionid")
            rur=self.retornar_(cookies, "rur")
            cookies = f'mid={mid}; datr={datr}; ig_did={ig_did}; ig_nrcb=1; ps_l=1; ps_n=1;  wd=440x696; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}; rur={rur}'
            with open("coockie.json", "w") as file:
                json.dump({"coockie":cookies},file, indent=4)
            return cookies
        else:
            return js["coockie"]
    def login_2(self):
        url = "https://www.instagram.com/accounts/login/ajax/"
        username = self.senha
        password = self.usuario

        # Criando uma sessão
        session = requests.Session()

        # Headers comuns usados em uma solicitação de login
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "X-CSRFToken": "TOKEN_AQUI"  # O CSRF token é geralmente necessário
        }

        # Primeiro, você pode precisar acessar a página de login para obter o CSRF token
        response = session.get("https://www.instagram.com/accounts/login/")
        csrf_token = response.cookies['csrftoken']

        # Atualiza o header com o CSRF token
        headers["X-CSRFToken"] = csrf_token

        # Dados para o login
        data = {
            "username": username,
            "password": password
        }

        # Realiza a solicitação de login
        response = session.post(url, headers=headers, data=data)

        # Verifica a resposta
        print(response.text)  # Mostra a resposta da tentativa de login
    def logout(self):
        with open("coockie.json", "w") as file:
            json.dump({"coockie": ""}, file, indent=4)
    def pegar_numero(self, id):
        
        url = f"https://i.instagram.com/api/v1/users/{id}/info/"  # Substitua pela URL desejada
        coockies = self.login()
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",  # Adicione um valor apropriado
            "Priority": "u=1, i",
            "Sec-CH-UA": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "Sec-CH-UA-Mobile": "?1",
            "Sec-CH-UA-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Cookie": coockies,
            "User-Agent": "Instagram 123.0.0.0 (iPhone; iOS 14.0; Scale/3.00)"
        }

        # Inicializando o navegador
        response = requests.get(url, headers=headers)
        json_convertido = json.loads(response.content.decode('utf-8'))
        if "message" in json_convertido:
            print(json_convertido["message"])
            self.logout()
            self.login()
            return ["",""]
        if "public_phone_number" in json_convertido["user"] or "public_email" in json_convertido["user"]:
            print([json_convertido["user"]["public_phone_number"], json_convertido["user"]["public_email"]])
            return [json_convertido["user"]["public_phone_number"], json_convertido["user"]["public_email"]]
        else:
            return ["", ""]
    def pegar_id(self, user):
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={user}"  # Substitua pela URL desejada
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",  # Adicione um valor apropriado
            "Priority": "u=1, i",
            "Sec-CH-UA": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "Sec-CH-UA-Mobile": "?1",
            "Sec-CH-UA-Platform": '"Android"',
            "User-Agent": "Instagram 123.0.0.0 (iPhone; iOS 14.0; Scale/3.00)"
        }

        # Inicializando o navegador
        response = requests.get(url, headers=headers)
        json_convertido = json.loads(response.content.decode('utf-8'))
        return json_convertido["data"]["user"]["id"]

    def pegar_seguidores(self, id, quantidade,username):
        lista_seguidores = []
        with open("seguidores.json", "r") as file:
            jss = json.load(file)
            lista_seguidores = jss
        max_id= ""
        cont = 0
        with open("index_seguidores.json", "r") as file:
            js = json.load(file)
            cont = js["cont"]

        index_pages = 250
        with open("index_pages.json", "r") as file:
            jsss = json.load(file)
            index_pages = jsss["page"]

        index_page = None
        url1 = f"https://www.instagram.com/graphql/query/?query_hash=37479f2b8209594dde7facb0d904896a&variables=%7B%22id%22:%22{id}%22,%22first%22:50,%22after%22:%22%22%7D"
        coockies = self.login()
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",  # Adicione um valor apropriado
            "Priority": "u=1, i",
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "Cookie": coockies,
            "referer":f"https://www.instagram.com/{username}/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
        response = requests.get(url1, headers=headers)
        json_convertido = json.loads(response.content.decode('utf-8'))
        if "message" in json_convertido:
            if json_convertido["message"] == 'Aguarde alguns minutos antes de tentar novamente.':
                self.logout()
                time.sleep(0.1)
                self.login()
                self.pegar_seguidores(id)
            if  json_convertido["message"] == "challenge":
                print("sem tentar")
            if json_convertido["message"] == 'feedback_required':
                print("teste")
        else:
            json_seguidores = json_convertido["data"]["user"]["edge_followed_by"]["edges"]
            max_id = json_convertido["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
            for seguidores in json_seguidores:
                lista_seguidores.append([seguidores["node"]["id"], seguidores["node"]["username"]])
                cont+=1
        with open("seguidores.json", "w") as file:
                json.dump(lista_seguidores,file,indent=4)
            
        while cont<quantidade:
            delay = random.uniform(2, 4)
            time.sleep(delay)
            url2 = f"https://www.instagram.com/graphql/query/?query_hash=37479f2b8209594dde7facb0d904896a&variables=%7B%22id%22:%22{id}%22,%22first%22:50,%22after%22:%22{max_id}%22%7D"
            # Inicializando o navegador
            response = requests.get(url2, headers=headers)
            json_convertido = json.loads(response.content.decode('utf-8'))
            print(json_convertido.keys())
            if "message" in json_convertido:
                if json_convertido["message"] == 'Aguarde alguns minutos antes de tentar novamente.':
                    self.logout()
                    time.sleep(0.1)
                    self.login()
                    self.pegar_seguidores(id)
                if json_convertido["message"] == 'feedback_required':
                    print("passou aqui")
 
            else:
                json_seguidores = json_convertido["data"]["user"]["edge_followed_by"]["edges"]
                max_id = json_convertido["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
                for seguidores in json_seguidores:
                    lista_seguidores.append([seguidores["node"]["id"], seguidores["node"]["username"]])
                    cont+=1
                    print([seguidores["node"]["id"], seguidores["node"]["username"]])
                    print(cont)
            with open("index_pages.json", "w") as file:
                json.dump({"page":index_pages},file,indent=4)
            with open("target_seguidor.json", "w") as file:
                json.dump({"id":max_id},file,indent=4)
            with open("seguidores.json", "w") as file:
                json.dump(lista_seguidores,file,indent=4)
            with open("index_seguidores.json", "w") as file:
                json.dump({"cont":cont},file,indent=4)

            

