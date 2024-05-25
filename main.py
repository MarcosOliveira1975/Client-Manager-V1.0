#Para funcionar é necessário criar um BD com o nome crud no Xampp

from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Secret Key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    detalhes = db.Column(db.String(300))

    def __init__(self, name, email, phone, detalhes):
        self.name = name
        self.email = email
        self.phone = phone
        self.detalhes = detalhes

@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template('index.html', contacts=all_data)

@app.route('/register')
def register():
    all_data = Data.query.all()
    return render_template('register.html', contacts=all_data)

@app.route('/gestao')
def gestao():
    all_data = Data.query.all()
    return render_template('/gestao.html', contacts=all_data)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        my_data = Data(request.form['name'],
                       request.form['email'],
                       request.form['phone'],
                       request.form['detalhes'])

        db.session.add(my_data)
        db.session.commit()

        flash("Contato cadastrado com sucesso!")

        return redirect(url_for('gestao'))
        return render_template('gestao.html')
        return redirect(url_for('index'))
        return render_template('index.html')

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.detalhes = request.form['detalhes']

        db.session.commit()
        
        flash("Contato editado com sucesso!")

        return redirect(url_for('gestao'))
        #return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)

    db.session.delete(my_data)
    db.session.commit()

    flash("Contato apagado com sucesso!")

    return redirect(url_for('gestao'))
    #return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
