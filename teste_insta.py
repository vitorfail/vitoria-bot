import requests
import json
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

            # Obtém os cookies
            cookies = driver.get_cookies()
            print(cookies)
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

        print(response.content)
    def pegar_id(self, user):
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={user}"  # Substitua pela URL desejada
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
        print(response.headers)
        #user_id = response.json()['graphql']['user']['id']
        #return user_id
