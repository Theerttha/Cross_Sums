from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

# Database configuration
if os.environ.get('RENDER'):  # Running on Render
    database_url = "postgresql://database_9oxp_user:BNSEJQEDmUsIqJlKH5iKNKMW1eG8Pmx1@dpg-ctnejidumphs73c5tqa0-a/database_9oxp"
else:
    database_url="postgresql://database_9oxp_user:BNSEJQEDmUsIqJlKH5iKNKMW1eG8Pmx1@dpg-ctnejidumphs73c5tqa0-a:5432/database_9oxp"
    #postgresql://database_9oxp_user:BNSEJQEDmUsIqJlKH5iKNKMW1eG8Pmx1@dpg-ctnejidumphs73c5tqa0-a.3oregon-postgres.render.com/database_9oxp



app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['user']
        pass_word = request.form['password']
        
        user = User.query.filter_by(username=user_name, password=pass_word).first()
        if user:
            return "yes"
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_reg = request.form['user_register']
        pass_word_reg = request.form['password_register']
        
        existing_user = User.query.filter_by(username=user_reg).first()
        if existing_user:
            return render_template('register.html', reg_user_exists=True)

        new_user = User(username=user_reg, password=pass_word_reg)
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html')
        except Exception as e:
            db.session.rollback()
            return "error"

    return render_template('register.html')

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)