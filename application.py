import os
import datetime

from flask import Flask, flash, jsonify, json, redirect, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology

# Configure application
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':

    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:SQL22!anu37@localhost/NAHS_Clicker'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dnfgfnmsjzxzlb:576441e75ea6f4dd007ea9b169f7fc7c8c00287e48ad2327400c9e9e997fad2b@ec2-34-202-65-210.compute-1.amazonaws.com:5432/daj5pb2odnlnf4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Class_Totals(db.Model):
    __tablename__= 'Class_Totals'
    id = db.Column(db.Integer, primary_key=True)
    Grade = db.Column(db.Integer)
    Score = db.Column(db.Integer)

    def __init__(self, Grade, Score):
        self.Grade = Grade
        self.Score = Score

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)


# HOMEPAGE
@app.route("/", methods=["GET", "POST"])
def main():

    if request.method == "POST":

        Score = request.form.get('score')
        Grade = request.form.get('grade')
        
        # print(score,grade)

        data = Class_Totals(Grade,Score)

        db.session.add(data)
        db.session.commit()

        return redirect("/")

    else:

        Freshmen = 0
        Sophomores = 0
        Juniors = 0
        Seniors = 0

        #i = 0
        current_score = 0
        current_grade = 0

        for ID, grade, score in db.session.query(Class_Totals.id, Class_Totals.Grade, Class_Totals.Score):

            if score == None:

                continue

            elif (0 >= score) or (score >= 200000):

                continue

            elif current_score == score and current_grade == grade:

                continue

            else: 

                #i = 0   
                current_score = score
                current_grade = grade

                if grade == 9:

                    Freshmen += score

                if grade == 10:
                    Sophomores += score
                
                if grade == 11:
                    Juniors += score

                if grade == 12:
                    Seniors += score

        return render_template("layout.html", Freshmen=Freshmen, Sophomores=Sophomores, Juniors=Juniors, Seniors=Seniors )


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:

    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run()