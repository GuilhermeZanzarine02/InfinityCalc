from flask import Flask, render_template, request, flash

app = Flask(__name__)

# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        
        flash('Formulário enviado com sucesso!')
        return render_template('Homepage/index.html') 

    return render_template('Homepage/index.html')  

# Rota para a página de juros simples (exemplo)
@app.route('/simpleInterestPage', methods=['GET', 'POST'])

def simple_interest_page():
    return render_template('simpleInterestPage/simpleInterest.html') 

if __name__ == '__main__':
    app.run(debug=True)
