import requests

def get_exchange_rate(moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"
    try:
        response = requests.get(url)
        response.raise_for_status() #Verifica se arequisição foi bem-sucedida
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None
        