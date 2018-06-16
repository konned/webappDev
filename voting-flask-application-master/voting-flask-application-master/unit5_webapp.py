from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics
from RiskFactorCalculation import risk_factor_calculate
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'formdata'

    """
    #To co było w wersji demo, tak wiem, że się nie używa
    do tego tego typu komentarzy
        id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    firstname = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    income = db.Column(db.Integer)
    satisfaction = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    """

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    question1 = db.Column(db.String)
    question2 = db.Column(db.String)
    question3 = db.Column(db.String)
    question4 = db.Column(db.String)
    question5 = db.Column(db.String)
    question6 = db.Column(db.String)
    question7 = db.Column(db.String)
    question8 = db.Column(db.String)
    question9 = db.Column(db.String)
    question10 = db.Column(db.String)
    question11 = db.Column(db.String)
    question12 = db.Column(db.String)
    question13 = db.Column(db.Float) #bo waga w kg
    question13_2 = db.Column(db.Integer) #bo wzrost w cm
    question14 = db.Column(db.String)
    question15 = db.Column(db.String)
    question16 = db.Column(db.String)
    question17 = db.Column(db.String)
    chorzyHPV = db.Column(db.String)
    typHPV = db.Column(db.String)
    risk = db.Column(db.Float)

    def __init__(self, question1, question2, question3, question4, question5,
                          question6, question7, question8, question9, question10,
                          question11, question12, question13, question13_2,question14,
                          question15, question16, question17, chorzyHPV, typHPV, risk):
        self.question1 = question1
        self.question2 = question2
        self.question3 = question3
        self.question4 = question4
        self.question5 = question5
        self.question6 = question6
        self.question7 = question7
        self.question8 = question8
        self.question9 = question9
        self.question10 = question10
        self.question11 = question11
        self.question12 = question12
        self.question13 = question13
        self.question13_2 = question13_2
        self.question14 = question14
        self.question15 = question15
        self.question16 = question16
        self.question17 = question17
        self.chorzyHPV = chorzyHPV
        self.typHPV = typHPV
        self.risk = risk


db.create_all()


@app.route("/", )
def welcome():
    return render_template('index.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Formdata).all() #wyciaga wszystko
    fd_risk = db.session.query(Formdata.risk) #powinno wyciagać cala kolumne z wynikami
    #fd_risk powinno załatwić wynik na tle innych i te slupkowe, ale trzeba bd dobrać progi
    #tego z pie chartem trochę nie rozumiem, to może jak już bd risk na 100% ustalony :D



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
    if question2 != "0":
        question3 = request.form['sexWiek']
        question4 = request.form['ciaza']
    else:
        question3 = "0"
        question4 = "0"

    if question4 != "0":
        question5 = request.form['ciazaWiek']
    else:
        question5 = "0"

    #question3=request.form['sexWiek']
    #question4=request.form['ciaza']
    #question5=request.form['ciazaWiek']
    question6 = request.form['cytologia']
    question7 = request.form['palenie']
    question8 = request.form['alkohol']
    question9 = request.form['warzywa']
    question10 = request.form['wf']
    question11 = request.form['chorzySM']
    question12 = request.form['chorzyIN']
    chorzyHPV = request.form['chorzyHPV']

    if chorzyHPV == "Tak":
        typHPV = request.form["HPV"]
    else:
        typHPV = "-1"

    question13 = request.form['waga']
    question13_2 = request.form['wzrost']
    question14 = request.form['wiek']
    question15 = request.form['miasto']
    question16 = request.form['praca']
    question17 = request.form['wyksztalcenie']

    #pytania warunkowe
    #if question2 == "0":
    #    question3 = "0"
    #    question4 = "0" #brak dzieci
    #    question5 = "0"
    #elif question4 == "0":
    #    question5 = "0"




    #funkcja obliczajaca risk factor. zwraca risk factor
    risk = risk_factor_calculate(question1, question2, question3, question4, question5,
                          question6, question7, question8, question9, question10,
                          question11, question12, question13, question13_2,question14,
                          question15, question16, question17, chorzyHPV, typHPV)
    # Save the data
    fd = Formdata(question1, question2, question3, question4, question5,
                          question6, question7, question8, question9, question10,
                          question11, question12, question13, question13_2,question14,
                          question15, question16, question17, chorzyHPV, typHPV, risk)
    db.session.add(fd)
    db.session.commit()

    return redirect('/result')


if __name__ == "__main__":
    app.debug = True
    app.run()
