from templates.exchangeRate.exchangerate import get_exchange_rate

def get_currency_value(value, moedaOrigem, moedaDestino): 
   currency_pair = f"{moedaOrigem}-{moedaDestino}"
   exchange_data = get_exchange_rate(currency_pair)
   concatenated = currency_pair.replace("-", "")
   value_currency = 0
   exchange_info = exchange_data[concatenated]

   if 'bid' not in exchange_info:
      raise ValueError(f"Chave 'bid' não encontrada nos dados de câmbio para {currency_pair}")
   
   else:
        value_currency = float(exchange_info['bid'])

   respose = value * value_currency

   return respose


  

   