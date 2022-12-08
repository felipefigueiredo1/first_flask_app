from flask import Flask, render_template, request, redirect, abort
from models.db import db, EmployeeModel
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

app.run(host='localhost', port=5000)


@app.context_processor
def inject_menu():

    # Injetando variavel em todos os templates.
    return dict(data= date.today())


@app.route('/', methods=['GET', 'POST'])
@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def retrieve_data_list():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html',employees = employees)


@app.route('/data/<int:id>')
def retrieve_single_employee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id ={id} Doenst exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()

            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position=position)

            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist"

    return render_template('update.html', employee=employee)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/ola/')
# @app.route('/ola/<nome>')
# def ola_mundo(nome="mundo"):
#     return render_template('index.html', nome_recebido = nome)


if __name__ == '__main__':
    app.run()