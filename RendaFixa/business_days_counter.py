import pandas as pd
from dateutil.relativedelta import relativedelta

df = pd.read_excel("BaseDeDados/Feriados.xlsx")
feriados = pd.to_datetime(df["DATA"])

def contar_datas_pareclas(emissao, vencimento, intervalo_parcela):
    emissao = pd.to_datetime(emissao)
    vencimento = pd.to_datetime(vencimento)
    datas_parcelas = []
    data_atual = emissao

    while data_atual <= vencimento:
        if data_atual not in feriados:
            datas_parcelas.append(data_atual)
        data_atual += relativedelta(months=intervalo_parcela)

    return datas_parcelas

def contar_dias_uteis_entre_datas(emissao, vencimento, intervalo_parcela):
    datas = contar_datas_pareclas(emissao, vencimento, intervalo_parcela)

    lista_datas_uteis = []
    lista_datas_uteis.append([datas[0], None])

    for i in range(1, len(datas)):
        data_inicio = datas[i - 1]
        data_fim = datas[i] - pd.Timedelta(days=1)
        range_dias = pd.date_range(start=data_inicio, end=data_fim, freq="B")
        dias_uteis = len(range_dias.difference(feriados))
        lista_datas_uteis.append([datas[i], dias_uteis])
        
    return lista_datas_uteis
         