import random
from flask import Flask, render_template, url_for, request, redirect,Blueprint,session
from flask_sqlalchemy import SQLAlchemy
import os

#from database import db

db = SQLAlchemy(app)
class Userlog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    time=db.Column(db.String(8))

    def __repr__(self):
        return f'<Userlog> {self.username}>'

game_db = Blueprint('Game', __name__)
@game_db.route("/")
def game():
    print(session)
    if 'username' in session:
        print("True")
        new_tuple = Userlog(username=session['username'], time='4')
        try:
            db.session.add(new_tuple)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return "error"
    else:
        print("not added")
    n=6
    grid=[]
    for i in range(n):
        l=[]
        for j in range(n):
            l.append(random.randint(1,10))
        grid.append(l)
  
    row_sum=[]
    col_sum=[]
    indexes=[]
    for i in range(n):
        x=random.randint(2,n-1)
        s=0
        l=[]
    
        for j in range(x):
            y=random.randint(0,n-1)
            while ( y in l):
                
                y=random.randint(0,n-1)
            l.append(y)
            s+=grid[i][l[-1]]
          
        indexes.append(l)
        row_sum.append(s)

    for i in range(n):
        s=0
        k=0
        for j in indexes:
            if i in j:
                s+=grid[k][i]
            k+=1
        col_sum.append(s)

    
    return render_template("game.html",board=grid,row_sum=row_sum,col_sum=col_sum)


