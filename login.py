import instaloader


def Login(user, senha):
    if user == "" or user == None or senha =="" or senha ==None:
        return 0
    else:
        try:
            # Crie uma instância do Instaloader        
            L = instaloader.Instaloader()

            # Faça login (opcional, se precisar acessar perfis privados)
            L.login(user, senha)

            # Carregue um perfil
            L.save_session_to_file("1_session")
            return 1
        except Exception as err:
            print(err)
            if str(err).find("Checkpoint") != -1:
                return 2
            if str(err).find("Wrong") != -1:
                return 3
            else:
                return 4