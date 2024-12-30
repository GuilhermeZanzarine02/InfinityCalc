import requests

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=8ad6c940dae44b1ba98f31e297fa38ff"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None