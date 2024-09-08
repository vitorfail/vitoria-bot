import requests
url = "https://graph.facebook.com/v20.2/64221474449?fields=business_discovery.username(vigiliaavivados_){followers_count,media_count}&access_token=EAAXv7WkeNSIBO4El7Il9GYSgmNR5Tv3kjL5ihBo0eJYqCXfZBDEdXiUJ9Xjubju2FZBlcLArWLGIhKun3cXGrBnbLZAhD5wbKr80RzYQZBMRqYWDO5ZCb1h9PlDwfXRCpCZAniFCAVjsoe4Ll9UBZAIlWCxXJkP4m9ZAApW9XZCyT1YpACPT1DeY2JlE6PZB7pzksDqAdcb4TN8FnOcZCDAgj0qJzCu3fkZD"
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Obter o conteúdo da resposta
    content = response.text
    
    # Exibir o conteúdo
    print(content)
else:
    print(f"Falha na requisição. Status code: {response.status_code}")