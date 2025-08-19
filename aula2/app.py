from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), unique = True, nullable=False)

@app.route('/')
def index():
    tarefas = Tarefas.query.all()
    return render_template('index.html', tarefas=tarefas)

@app.route('/criar', methods=['POST'])
def criar_tarefas():
    descricao = request.form['descricao']

    new_task = Tarefas(descricao = descricao)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/deletar', methods=['POST'])
def deletar_tarefas():
    descricao = request.form['descricao']
    tarefa = Tarefas.query.filter_by(descricao=descricao).first()
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
