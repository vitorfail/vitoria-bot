import instaloader

# Crie uma instância do Instaloader
L = instaloader.Instaloader()

# Faça login (opcional, se precisar acessar perfis privados)
L.login('vitor_andrademanoel04', 'BRksedu1@1234')

# Carregue um perfil
L.save_session_to_file("1_session")