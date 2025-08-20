from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_paciente = db.Column(db.String(100), nullable=False)
    nome_medico = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    data_consulta = db.Column(db.DateTime, nullable=False)


@app.route('/')
def index():
    tarefas = Tarefas.query.all()
    return render_template('index.html', tarefas=tarefas)

@app.route('/criar')
def criar():
    return render_template('criar.html')

@app.route('/editar')
def editar():
    return render_template('editar.html')

@app.route('/deletar')
def deletar():
    return render_template('deletar.html')

@app.route('/criar', methods=['POST'])
def criar_tarefas():
    nome_paciente = request.form['nome_paciente']
    nome_medico = request.form['nome_medico']
    especialidade = request.form['especialidade']
    data_consulta = datetime.strptime(request.form['data_consulta'], '%Y-%m-%dT%H:%M')

    new_task = Tarefas(
        nome_paciente=nome_paciente,
        nome_medico=nome_medico,
        especialidade=especialidade,
        data_consulta=data_consulta
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/editar', methods=['POST'])
def editar_tarefas():
    id = request.form['id']
    nome_paciente = request.form['nome_paciente']
    nome_medico = request.form['nome_medico']
    especialidade = request.form['especialidade']
    data_consulta = datetime.strptime(request.form['data_consulta'], '%Y-%m-%dT%H:%M')

    tarefa = Tarefas.query.filter_by(id=id).first()
    if tarefa:
        tarefa.nome_paciente = nome_paciente
        tarefa.nome_medico = nome_medico
        tarefa.especialidade = especialidade
        tarefa.data_consulta = data_consulta
        db.session.commit()
    return redirect('/')

@app.route('/deletar', methods=['POST'])
def deletar_tarefas():
    id = request.form['id']
    tarefa = Tarefas.query.filter_by(id=id).first()
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
    return redirect('/')

@app.route('/pesquisar', methods=['POST'])
def pesquisar_tarefas():
    nome_paciente = request.form['nome_paciente']
    tarefas = Tarefas.query.filter_by(nome_paciente=nome_paciente).all()
    if tarefas:
        return render_template('index.html', tarefas=tarefas)
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
