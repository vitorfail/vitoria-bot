import instaloader
import time
import os
import json

# Crie uma instância do Instaloader
def extract_user():
    L = instaloader.Instaloader()
    user = "vitor_andrademanoel04"
 


    # Faça login (opcional, se precisar acessar perfis privados)
    L.load_session_from_file(user,"1_session")


    # Carregue um perfil
    profile = instaloader.Profile.from_username(L.context, "breno_fons")
    # Exiba algumas informações do perfil
    #print(s)
    seguidores = profile.get_followees()

    lista = []

    for seguidor in seguidores:
        seguidor.username
        if len(lista) ==500:
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
            except:
                print("deu erro")
    with open('seguidores.json', 'w') as file:
        json.dump(lista, file, indent=4)
extract_user()