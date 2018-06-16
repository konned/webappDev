from flask import Flask, render_template, redirect, request, url_for
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
    risk = db.Column(db.Float)

    def __init__(self, question1, question2, question3, question4, question5,
                          question6, question7, question8, question9, question10,
                          question11, question12, question13, question13_2,question14,
                          question15, question16, question17, risk):
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
        self.risk = risk


db.create_all()


@app.route("/")
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


    data1 = []
    for idx, val in enumerate(fd_risk):
        data1.append([idx, val])

    # Sortowanie tablicy po risk faktorze (czyli po kolumnie o indeksie 1)
    data1 = sorted(data1, key=lambda x: x[1])

    antykoncepcja = []
    partnerzy = []
    cytologia = []
    papierosy = []
    alkohol = []
    warzywa = []
    sport = []
    rak = []
    ciaze = []
    waga = []
    wiek = []

    for value in fd_list:
        antykoncepcja.append(int(value.question1))
        partnerzy.append(int(value.question2))
        cytologia.append(int(value.question6))
        papierosy.append(int(value.question7))
        alkohol.append(int(value.question8))
        warzywa.append(int(value.question9))
        sport.append(int(value.question10))
        rak.append(int(value.question11))
        ciaze.append(int(value.question4))
        waga.append(int(value.question13))
        wiek.append(int(value.question14))

    antykoncepcja_mean = statistics.mean(antykoncepcja) if len(antykoncepcja) > 0 else 0
    partnerzy_mean = statistics.mean(partnerzy) if len(partnerzy) > 0 else 0
    cytologia_mean = statistics.mean(cytologia) if len(cytologia) > 0 else 0
    papierosy_mean = statistics.mean(papierosy) if len(papierosy) > 0 else 0
    alkohol_mean = statistics.mean(alkohol) if len(alkohol) > 0 else 0
    warzywa_mean = statistics.mean(warzywa) if len(warzywa) > 0 else 0
    sport_mean = statistics.mean(sport) if len(sport) > 0 else 0
    rak_mean = statistics.mean(rak) if len(rak) > 0 else 0
    ciaze_mean = statistics.mean(ciaze) if len(ciaze) > 0 else 0
    waga_mean = statistics.mean(waga) if len(waga) > 0 else 0
    wiek_mean = statistics.mean(wiek) if len(wiek) > 0 else 0

    data2 = [
        ['antykoncepcja', antykoncepcja_mean],
        ['partnerzy', partnerzy_mean],
        ['cytologia', cytologia_mean],
        ['papierosy', papierosy_mean],
        ['alkohol', alkohol_mean],
        ['warzywa', warzywa_mean],
        ['sport', sport_mean],
        ['rak w rodzinie', rak_mean],
        ['ilość ciąż', ciaze_mean],
        ['waga', waga_mean],
        ['wiek', wiek_mean]
    ]

    low = []  # niskie ryzyko
    medium = []  # srednie ryzyko
    high = []  # wysokie ryzyko

    #wartosci risk  factorow
    medium_risk = 20
    high_risk = 50 #zmienic jak beda znane risk_faktory

    for idx, val in enumerate(fd_risk):
        if val >= high_risk:
            high.append(int(val.question6))
        elif val >= medium_risk:
            medium.append(int(val.question6))
        else:
            low.append(int(val.question6))

    if len(high) > 0:
        mean_high = statistics.mean(high)
    else:
        mean_high = 0

    if len(medium) > 0:
        mean_medium = statistics.mean(medium)
    else:
        mean_medium = 0

    if len(low) > 0:
        mean_low = statistics.mean(low)
    else:
        mean_low = 0

    data3 = [
        ['Niskie', mean_low],
        ['Średnie', mean_medium],
        ['Wysokie', mean_high]
    ]

    data = [data1, data2, data3]

    current = request.args.get('form_id')

    if current is None:
        current = -1

    return render_template('result.html', data=data, current=current)


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
                          question15, question16, question17)
    # Save the data
    fd = Formdata(question1, question2, question3, question4, question5,
                          question6, question7, question8, question9, question10,
                          question11, question12, question13, question13_2,question14,
                          question15, question16, question17, risk)
    db.session.add(fd)
    db.session.commit()

    return redirect(url_for('show_result', form_id=fd.id))


if __name__ == "__main__":
    app.debug = True
    app.run()
