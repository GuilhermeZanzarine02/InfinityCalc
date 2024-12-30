from flask import Flask, render_template, request, flash
from blackscholes.calculo import calculo_blaack_sholes, calculo_nd1_nd2, calculos_intermediarios
from templates.exchangeRate.exchangerate import get_exchange_rate

app = Flask(__name__)

# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])

def index():
     #Busca dados de câmbio para USD-BRL
     exchange_data = get_exchange_rate("USD-BRL")
     exchange_rate = None

     if exchange_data:
          key = "USDBRL" 
          if key in exchange_data:
               exchange_rate = exchange_data[key]

     exchange_data_eur_brl = get_exchange_rate("EUR-BRL")
     exchange_rate_eur_brl  =  None

     if exchange_data_eur_brl:
          key = "EURBRL"
          if key in exchange_data_eur_brl:
               exchange_rate_eur_brl = exchange_data_eur_brl[key]

     return render_template('Homepage/index.html',
                             exchange_rate=exchange_rate,
                             exchange_rate_eur_brl = exchange_rate_eur_brl)
     

# Rota para a página de juros simples (exemplo)
@app.route('/simpleInterestPage', methods=['GET', 'POST'])

def simple_interest_page():
    return render_template('simpleInterestPage/simpleInterest.html') 


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
