import requests

dict_crypto ={}

def get_crypto_currency(crypto):
    api_key = "3693a3f897435a97878dacce9c24c84daa42508e1cbe13211ba0b8b5b09ae861"
    url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms=USD,EUR,BRL"

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


def adicionar_crypto_ao_dicionario():
    lista = ["BTC", "ETH", "XRP", "USDT", "SOL", "ADA"]
    
    for item in lista:
        dados = get_crypto_currency(item)
        if dados:
            dict_crypto[item] = dados
            print(f"Adicionado: {item} -> {dados}")
        else:
             print(f"Não foi possível obter dados para {item}")
             
    return dict_crypto


def calculo(valor, c_crypto, moeda, option):
    data = adicionar_crypto_ao_dicionario()

    if not data or c_crypto not in data or moeda not in data[c_crypto]:
        print("Erro: Dados inválidos ou criptomoeda/moeda não encontrada.")
        return None

    try:
        cripto_value = data[c_crypto][moeda]
        output = 0

        if option == "converter":
            output = valor / cripto_value
        
        elif option == "comprar":
            output = valor * cripto_value
        
        else:
            print(f"Opção {option} não encontrada.")
            return None

        print(f"valor: {valor} crypto: {c_crypto} moeda: {moeda} opcao: {option}")
        return output
        
    
    except Exception as e:
        print(f"Ocorreu um erro ao calcular: {e}")
        return None




    

