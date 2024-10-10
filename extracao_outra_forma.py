from teste_insta import Vitoria
import json
import time
import random
import pandas as pd
vitoria_bot = Vitoria("BetinaAntunes336", "kE6xTH0k5lc")
resultado = vitoria_bot.login()

#luna = vitoria_bot.login_2()
#id = vitoria_bot.pegar_id("mr.deliveryy")
#print(id)
#seguidores = vitoria_bot.pegar_seguidores(id, 20000, "mr.deliveryy")

lista_seguidores =[]
lista_numeros = []
cont =0
with open("index_contato.json", "r") as file:
   cont=json.load(file)["cont"]
with open("seguidores.json", "r") as file:
    lista_seguidores = json.load(file)
with open("user_contact.json", "r") as file:
    lista_numeros = json.load(file)["num"]


for i, seg in enumerate(lista_seguidores):
    if i >= cont:    
        delay = random.uniform(2, 4)
        time.sleep(delay)
        try:
            seguidores = vitoria_bot.pegar_numero(seg[0])
            if seguidores[0] !="" or  seguidores[1] !="":
                if seguidores[0] == "quebrar":
                    break
                else:
                    lista_numeros.append(seguidores)
                    with open("user_contact.json", "w") as file:
                        json.dump({"num":lista_numeros}, file,indent=4 )
            with open("index_contato.json", "w") as file:
                json.dump({"cont":cont}, file, indent=4)
        except Exception as ex:
            print(f"deu erro:{ex}")
            with open("user_contact.json", "w") as file:
                json.dump({"num":lista_numeros}, file,indent=4 )
        cont+=1
        print(cont)
