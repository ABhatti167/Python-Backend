from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev' # determines our db mode

if ENV == 'dev': # if true we use a local database
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:%40Aleeza786@localhost/lexus"
    )
else: # else we use the production one
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        ""
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #otherwise we get a warning

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.String(200), unique = True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comment):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comment = comment

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods = ["POST"])
def submit():
    if request.method == "POST":
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        
        if customer == '' or dealer == '':
            return render_template('index.html', message = "Please enter required data")
        
        #if customer doesnt already exist in db we add it
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            
            db.session.add(data)
            db.session.commit()
            
            send_mail(customer, dealer, rating, comments)
        
            return render_template('success.html')
        
        return render_template('index.html', message = "You have already submitted feedback.")



if __name__ == '__main__':
    app.run()
