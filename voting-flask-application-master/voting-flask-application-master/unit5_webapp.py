from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics
from RiskFactorCalculation import risk_factor_calculate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    firstname = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    income = db.Column(db.Integer)
    satisfaction = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)

    def __init__(self, firstname, email, age, income, satisfaction, q1, q2):
        self.firstname = firstname
        self.email = email
        self.age = age
        self.income = income
        self.satisfaction = satisfaction
        self.q1 = q1
        self.q2 = q2

db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Formdata).all()

    # Some simple statistics for sample questions
    satisfaction = []
    q1 = []
    q2 = []
    for el in fd_list:
        satisfaction.append(int(el.satisfaction))
        q1.append(int(el.q1))
        q2.append(int(el.q2))

    if len(satisfaction) > 0:
        mean_satisfaction = statistics.mean(satisfaction)
    else:
        mean_satisfaction = 0

    if len(q1) > 0:
        mean_q1 = statistics.mean(q1)
    else:
        mean_q1 = 0

    if len(q2) > 0:
        mean_q2 = statistics.mean(q2)
    else:
        mean_q2 = 0

    # Prepare data for google charts
    data = [['Satisfaction', mean_satisfaction], ['Python skill', mean_q1], ['Flask skill', mean_q2]]

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    question1=request.form['antykoncepcja']
    question2=request.form['partnerzy']
    question3=request.form['sexWiek']
    question4=request.form['ciaza']
    question5=request.form['ciazaWiek']
    question6 = request.form['cytologia']
    question7 = request.form['palenie']
    question8 = request.form['alkohol']
    question9 = request.form['warzywa']
    question10 = request.form['wf']
    question11 = request.form['chorzySM']
    question12 = request.form['chorzyIN']
    question13 = request.form['waga']
    question13_2=request.form['wzrost']
    question14 = request.form['wiek']
    question15 = request.form['miasto']
    question16 = request.form['praca']
    question17 = request.form['wyksztalcenie']
    #firstname = request.form['firstname']
    #email = request.form['email']
    #age = request.form['age']
    #income = request.form['income']
    #satisfaction = request.form['satisfaction']
    #q1 = request.form['q1']
    #q2 = request.form['q2']

    #funkcja obliczajaca risk factor. zwraca risk factor
    risk_factor_calculate(question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11, question12, question13, question13_2,question14, question15, question16, question17)
    # Save the data
    #fd = Formdata(firstname, email, age, income, satisfaction, q1, q2)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
