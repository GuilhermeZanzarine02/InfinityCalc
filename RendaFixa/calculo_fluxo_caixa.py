from RendaFixa.business_days_counter import contar_dias_uteis_entre_datas

import pandas as pd



def calculate_cash_flow(valor, taxa_pre, emissao, vencimento, intervalo_parcela, lista_formatada):

    dados = []
    
    datas = contar_dias_uteis_entre_datas(emissao, vencimento, intervalo_parcela)
    df_response = pd.DataFrame(datas, columns=["Datas", "DU"])

    amortizacao = None
    porcent_amortizacao = 0

    for i in range(len(df_response)):
        data_inicial = df_response["Datas"][i]
        dias_uteis = df_response["DU"][i]

        if i == 0:
            fator_pre = 1
            vna = valor
            juros = 0
            amortizacao = 0
            parcela = 0
            saldo_devedor = valor
        else:
            fator_pre = (1 + (taxa_pre / 100))**(dias_uteis/252)
            vna = saldo_devedor * fator_pre
            juros = saldo_devedor * (fator_pre -1)

            amortizacao = 0
            porcent_amortizacao = 0
            for data_amort, valor_amort in lista_formatada:
                data_amort = pd.to_datetime(data_amort)
                if data_amort == data_inicial:
                    porcent_amortizacao = valor_amort
                    amortizacao = valor * (porcent_amortizacao / 100)
                    break
                    
        parcela = juros + amortizacao
        saldo_devedor = vna - parcela

        dados.append([data_inicial,
                      dias_uteis,
                      round(vna, 2),
                      round(fator_pre, 8),
                      round(juros, 2),
                      round(amortizacao, 2),
                      round(parcela, 2),
                      round(saldo_devedor, 2),
                      round(porcent_amortizacao, 2)])
        
    colunas = ["Data", "DU", "VNA", "Fator Pré", "Juros", "Amortização", "Parcela", "Saldo Devedor", "% Amortização"]
    df = pd.DataFrame(dados, columns=colunas)         

    nome_arquivo = "fluxo_de_caixa_teste.xlsx"
    df.to_excel(nome_arquivo, index=False, engine='openpyxl')
    print(f"Arquivo salvo como {nome_arquivo}")   
