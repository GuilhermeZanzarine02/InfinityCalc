import requests

def get_crypto_currency(crypto):
    api_key = "3693a3f897435a97878dacce9c24c84daa42508e1cbe13211ba0b8b5b09ae861"
    url = f"https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms={crypto}&tsyms=USD,JPY,EUR,BRL,GBP,CNY,AUD"

    headers = {
        "Authorization": f"Apikey {api_key}"
    }

    try:
        response = requests.get(url, headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None
