import random
import os
import pandas as pd
from flask import Flask, render_template, request, flash
from blackscholes.calculo import calculo_blaack_sholes, calculo_nd1_nd2, calculos_intermediarios
from templates.exchangeRate.exchangerate import get_exchange_rate
from Criptomoedas.cripto import get_crypto_currency, calculo
from Cambio.cambio import get_currency_value
from RendaFixa.business_days_counter import contar_datas_pareclas, contar_dias_uteis_entre_datas
from templates.Homepage.news import get_news

# Import para calculos de juros simples e compostos
from simpleInterest.simpleInterest import SimpleInterest
from compoundInterest.compoundInterest import CompoundInterest

# Import para formatação usando o formato Brasileiro
# Configurar o local para o formato brasileiro
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = Flask(__name__)

# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])

def index():
    # Busca dados de câmbio
    exchange_data = get_exchange_rate("USD-BRL")
    exchange_rate = exchange_data.get("USDBRL") if exchange_data else None

    exchange_data_eur_brl = get_exchange_rate("EUR-BRL")
    exchange_rate_eur_brl = exchange_data_eur_brl.get("EURBRL") if exchange_data_eur_brl else None

    exchange_data_gbp_brl = get_exchange_rate("GBP-BRL")
    exchange_rate_gbp_brl = exchange_data_gbp_brl.get("GBPBRL") if exchange_data_gbp_brl else None

    exchange_data_cny_brl = get_exchange_rate("CNY-BRL")
    exchange_rate_cny_brl = exchange_data_cny_brl.get("CNYBRL") if exchange_data_cny_brl else None

    exchange_data_aud_brl = get_exchange_rate("AUD-BRL")
    exchange_rate_aud_brl = exchange_data_aud_brl.get("AUDBRL") if exchange_data_aud_brl else None

    exchange_data_jpy_brl = get_exchange_rate("JPY-BRL")
    exchange_rate_jpy_brl = exchange_data_jpy_brl.get("JPYBRL") if exchange_data_jpy_brl else None


    # Busca dados de notícias
    data = get_news()
    random_article = None

    if data:
        articles = data.get("articles", [])
        if articles:
            random_article = random.choice(articles)

    return render_template(
        'Homepage/index.html',
        exchange_rate=exchange_rate,
        exchange_rate_eur_brl=exchange_rate_eur_brl,
        exchange_rate_gbp_brl=exchange_rate_gbp_brl,
        exchange_rate_cny_brl=exchange_rate_cny_brl,
        exchange_rate_aud_brl=exchange_rate_aud_brl,
        exchange_rate_jpy_brl=exchange_rate_jpy_brl,
        random_article=random_article
    )

# Rota para a página de juros simples
@app.route('/simpleInterestPage', methods=['GET', 'POST'])

def simple_interest_page():
    
    if request.method == "POST":
        try:
            pi = float(request.form['pi'])
            tj = float(request.form['tj'])
            t  = float(request.form['t'])
            unidade_tempo = request.form['unidade_tempo'].lower().strip()
            periodo_taxa = request.form['txp'].lower().strip()

            simple_interest = SimpleInterest(pi, tj, t, unidade_tempo, periodo_taxa)

            resultado = simple_interest.calculo()
            resultado_formatado = f"R$ {resultado:,.2f}"

            line_graph_path = 'ImagemGrafico.png'
            simple_interest.gerarGrafico(graph_path=os.path.join('static', line_graph_path))

            pie_graph_path =  'ImagemPizza.png'
            simple_interest.gerarGraficoPizza(graph_path=os.path.join('static', pie_graph_path))

            
            return render_template('simpleInterestPage/simpleInterest.html', resultado=resultado_formatado,
                                                                             line_pah = line_graph_path,
                                                                             pie_path = pie_graph_path)

        except ValueError:
            flash("Erro: Por favor, insira apenas números válidos.", "error")
            return render_template('simpleInterestPage/simpleInterest.html')
        
        
    return render_template('simpleInterestPage/simpleInterest.html') 

# Rota para a página de juros compostos
@app.route('/compoundInterestPage', methods=['GET', 'POST'])

def compound_Interest_page():
    if request.method == "POST":
        try:
            pi = float(request.form['pi'])
            tj = float(request.form['tj'])
            t  = float(request.form['t'])
            unidade_tempo = request.form['unidade_tempo']
            periodo_taxa = request.form['txp'].lower().strip()

            compound_interest = CompoundInterest(pi, tj, t, unidade_tempo, periodo_taxa)

            resultado = compound_interest.calculo()
            resultado_formatado = f"R$ {resultado:,.2f}"

            line_graph_path = 'ImagemGrafico2.png'
            compound_interest.gerarGrafico(graph_path=os.path.join('static', line_graph_path))

            pie_graph_path =  'ImagemPizza2.png'
            compound_interest.gerarGraficoPizza(graph_path=os.path.join('static', pie_graph_path))

            return render_template('compoundInterestPage/compoundInterest.html', resultado=resultado_formatado,
                                                                                 line_pah = line_graph_path,
                                                                                 pie_path = pie_graph_path)

        except ValueError:
            flash("Erro: Por favor, insira apenas números válidos.", "error")
            return render_template('compoundInterestPage/compoundInterest.html')
        
    return render_template('compoundInterestPage/compoundInterest.html') 

#Rota para a página Black Scholes
@app.route('/BlackScholesPage', methods=['GET', 'POST'])

def black_scholes_page():
    if request.method == 'POST':

        try:
            s = float(request.form['S0'])
            x = float(request.form['X'])
            r = float(request.form['r'])/100
            t = float(request.form['T'])/365
            sigma = float(request.form['sigma'])/100

            if s <= 0 or x <= 0 or r <= 0 or t <= 0 or sigma <= 0:
                    flash("Por favor, insira valores válidos (números positivos).", "error")
                    return render_template('BlackScholesPage/blackscholes.htm')
            
            d1, d2 = calculos_intermediarios(s, x, r, t, sigma)
            nd1, nd2, nd1n, nd2n = calculo_nd1_nd2(d1, d2)
            call, put = calculo_blaack_sholes(s, x, r, t, nd1, nd2, nd1n, nd2n)

            return render_template('BlackScholesPage/blackscholes.htm', call=call, put=put)
        
        except ValueError:
            flash("Erro: Por favor, insira apenas números válidos.", "error")
            return render_template('BlackScholesPage/blackscholes.htm')
        
    return render_template('BlackScholesPage/blackscholes.htm')

# Rota para exibir os dados de câmbio
@app.route('/Cambiot', methods=['GET', 'POST'])

def cambio():
    currencies = ["USD-BRL", "EUR-BRL", "GBP-BRL", "CNY-BRL", "AUD-BRL", "JPY-BRL"]
    exchange_rates = {}

    for currency_pair in currencies:
        exchange_data = get_exchange_rate(currency_pair)
        currency_key = currency_pair.replace("-", "")
        exchange_rates[currency_key] = exchange_data.get(currency_key) if exchange_data else None
        formatted_response = ""

    exchange_rate_usd_brl = exchange_rates.get("USDBRL")
    exchange_rate_eur_brl = exchange_rates.get("EURBRL")
    exchange_rate_gbp_brl = exchange_rates.get("GBPBRL")
    exchange_rate_cny_brl = exchange_rates.get("CNYBRL")
    exchange_rate_aud_brl = exchange_rates.get("AUDBRL")
    exchange_rate_jpy_brl = exchange_rates.get("JPYBRL") 

    if request.method == 'POST':
        try:
            valor = float(request.form['valor'])
            moedaOrigem = request.form['moedaOrigem'].upper()
            moedaDestino = request.form['moedaDestino'].upper()
        
            response = get_currency_value(valor, moedaOrigem, moedaDestino)

            formatted_response = locale.format_string("%.2f", response,  grouping=True)

        except ValueError as e:
            flash(f"Erro! Erro ao validar informações do formulário. {e}")
            return render_template('Cambiot/cambio.html')
        
    return render_template('Cambiot/cambio.html', exchange_rate_usd_brl=exchange_rate_usd_brl,
                                                  exchange_rate_eur_brl=exchange_rate_eur_brl,
                                                  exchange_rate_gbp_brl=exchange_rate_gbp_brl,
                                                  exchange_rate_cny_brl=exchange_rate_cny_brl,
                                                  exchange_rate_aud_brl=exchange_rate_aud_brl,
                                                  exchange_rate_jpy_brl=exchange_rate_jpy_brl,
                                                  formatted_response=formatted_response)

# Rota para a página de CriptoMoedas
@app.route('/Criptomoedas', methods=['GET', 'POST'])

def criptomoedas():
    
    btc_data = get_crypto_currency("BTC")
    eth_data = get_crypto_currency("ETH")
    xrp_data = get_crypto_currency("XRP")
    tether_data = get_crypto_currency("USDT")
    solana_data = get_crypto_currency("SOL")
    cardano_data = get_crypto_currency("ADA")

    if request.method == 'POST':
        try:
            valor = float(request.form["valor"])
            c_crypto = request.form["c_crypto"].upper()
            moeda = request.form["moeda"].upper()
            option = request.form["opcao"].lower().strip()

            resultado = calculo(valor, c_crypto, moeda, option)
            resultado_formatado = locale.format_string("%.2f", resultado,  grouping=True)

            return render_template('Criptomoedas/criptomoedas.html', btc_data=btc_data,
                                                             eth_data=eth_data,
                                                             xrp_data=xrp_data,
                                                             tether_data=tether_data,
                                                             solana_data=solana_data,
                                                             cardano_data=cardano_data,
                                                             resultado_formatado=resultado_formatado)

        except ValueError as e:
            flash(f"Erro! Erro ao validar informações do formulário. {e}")
            return render_template('Criptomoedas/criptomoedas.html')
        
    return render_template('Criptomoedas/criptomoedas.html')

# Rota para a página de Debêmtures
@app.route('/RendaFixaPage', methods=['GET', 'POST'])

def renda_fixa():
    if request.method == 'POST':
       try:
           valor = float(request.form["vi"])
           taxa_pre = float(request.form["tj"])
           emissao = pd.to_datetime(request.form["emissao"])
           vencimento = pd.to_datetime(request.form["vencimento"])
           intervalo_parcela = request.form["intervalo"].lower().strip()
           amortizacoes = request.form["amortizacoes"]
 
           if intervalo_parcela:
                if intervalo_parcela == "mensal": intervalo_parcela = 1
                if intervalo_parcela == "bimestral": intervalo_parcela = 2
                if intervalo_parcela == "trimestral": intervalo_parcela = 3
                if intervalo_parcela == "semestral": intervalo_parcela = 6
                if intervalo_parcela == "anual": intervalo_parcela = 12
           else:
               flash(f"Intervalo {intervalo_parcela} não encontrado.")

           print(f"Valor: {valor} - Taxa: {taxa_pre} - Emissão: {emissao} - Vencimento: {vencimento} - Amortizações: {amortizacoes} - Intervalo Parcela: {intervalo_parcela}")
           
           return render_template("RendaFixaPage/rendaFixa.html")
       
       except ValueError as e:
           flash(f"Erro! Erro ao validar informações do formulário. {e}")
           return render_template("RendaFixaPage/rendaFixa.html")
       
    return render_template("RendaFixaPage/rendaFixa.html")

# Rota para a página de CDB
@app.route('/CdbPage', methods=['GET', 'POST'])

def cbd():
    if request.method == 'POST':
        try:
            return render_template('CdbPage/cdb.html')
        
        except ValueError as e:
            flash(f"Erro! Erro ao validar informações do formulário. {e}")
            return render_template('CdbPage/cdb.html')
        
    return render_template('CdbPage/cdb.html')

if __name__ == '__main__':
    app.run(debug=True)
 