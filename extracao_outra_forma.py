from teste_insta import Vitoria
import json
import time
import random
vitoria_bot = Vitoria("EdileusaGila266", "MLmzxMRM87A")
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

for seg in lista_seguidores:
    cont+=1
    print("passou aqui")
    delay = random.uniform(2, 4)
    time.sleep(delay)

    try:
        seguidores = vitoria_bot.pegar_numero(seg[0])
        lista_numeros.append(seguidores)
        with open("index_contato.json", "w") as file:
            json.dump({"cont":cont}, file, indent=4)
        with open("user_contact.json", "w") as file:
            json.dump({"num":lista_numeros}, file,indent=4 )

    except Exception as ex:
        print(f"deu erro:{ex}")
        with open("user_contact.json", "w") as file:
            json.dump({"num":lista_numeros}, file,indent=4 )
            