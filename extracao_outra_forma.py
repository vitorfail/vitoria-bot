from testa import Vitoria
vitoria_bot = Vitoria("IsaLancastre348", "TLLrFpB9yli")
url = "https://www.instagram.com/api/v1/friendships/13731379247/followers/?count=12&search_surface=follow_list_page"
resultado = vitoria_bot.login()


id = vitoria_bot.pegar_id("mr.deliveryy")
print(id)