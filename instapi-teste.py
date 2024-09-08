from instagrapi import Client

try:
    cl = Client()
    cl.login("vitor_andrademanoel04", "BRksedu1@1234")
    user_id = cl.user_id_from_username("breno_fons")
    medias = cl.user_medias(user_id, 20)

except Exception as e:
    print(f'Erro ao fazer login: {e}')