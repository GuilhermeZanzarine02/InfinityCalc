import random
import os
from flask import Flask, render_template, request, flash
from blackscholes.calculo import calculo_blaack_sholes, calculo_nd1_nd2, calculos_intermediarios
from templates.exchangeRate.exchangerate import get_exchange_rate
from templates.Homepage.news import get_news
from simpleInterest.simpleInterest import SimpleInterest

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

            simple_interest = SimpleInterest(pi, tj, t)
            resultado = round(simple_interest.calculo(), 2)

            GRAPH_PATH = 'ImagemGrafico.png'

            simple_interest.gerarGrafico(graph_path=os.path.join('static', GRAPH_PATH))

            return render_template('simpleInterestPage/simpleInterest.html', resultado=resultado,
                                                                             graph_pah = GRAPH_PATH)

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

            compound_interest = SimpleInterest(pi, tj, t)
            resultado = round(compound_interest.calculo(), 2)

            GRAPH_PATH = 'ImagemGrafico.png'

            compound_interest.gerarGrafico(graph_path=os.path.join('static', GRAPH_PATH))

            return render_template('compoundInterestPage/compoundInterest.html', resultado=resultado,
                                                                             graph_pah = GRAPH_PATH)

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
@app.route('/exchangeRate', methods=['GET'])

def exchange_rate(moeda):
    pass

if __name__ == '__main__':
    app.run(debug=True)
