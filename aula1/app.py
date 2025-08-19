from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/', methods = ['GET', 'POST'])

def index():
    resultado = None
    if request.method == 'POST':
        try:
            n1 = float(request.form['pnumero'])
            n2 = float(request.form['snumero'])
            operacao = request.form['operacao']
            if operacao == 'soma':
                resultado = n1 + n2
            elif operacao == 'subtracao':
                resultado = n1 - n2
            elif operacao == 'multiplicacao':
                resultado = n1 * n2
            elif operacao == 'divisao':
                resultado = n1 / n2 if n2 != 0 else 'Erro: Divisão por zero'
        except Exception as e:
            resultado = f'Erro: {e}'
    return render_template('index.html', resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)