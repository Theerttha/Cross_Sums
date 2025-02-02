from flask import Flask, render_template, url_for, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
import os, random,time
from database import db
app = Flask(__name__)

# Database configuration
if os.environ.get('RENDER'):  # Running on Render
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
database_url="postgresql://pheonix_protocol:15oCUeAKcbej9PnPEtlQd4WWImruy1HL@dpg-cuahs0tsvqrc73dp1uvg-a.oregon-postgres.render.com/community_r69k"
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.config.update(
    SECRET_KEY='Please work',
    SESSION_TYPE='sqlalchemy',
    SESSION_SQLALCHEMY=db,
    SESSION_SQLALCHEMY_TABLE='sessions',
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=5)
)




#Session(app)
#app.register_blueprint(game.game_db, url_prefix='/game')
""""
class FlaskSession(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(255), primary_key=True,extend_existing=True)
    session_data = db.Column(db.LargeBinary,extend_existing=True)
    expiry = db.Column(db.DateTime, nullable=True,extend_existing=True)

    def __init__(self, id, session_data, expiry):
        self.id = id
        self.session_data = session_data
        self.expiry = expiry
"""
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Userlog(db.Model):
    __tablename__ = 'userlog'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    time=db.Column(db.String(8))

    def __repr__(self):
        return f'<Userlog {self.username}>'


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        reg=request.form.get("register_button")
        if reg is not None:
      
            return redirect(url_for('register'))
        user_name = request.form['user']
        pass_word = request.form['password']
        
        user = User.query.filter_by(username=user_name, password=pass_word).first()
        login=request.form.get("login_button")
        if user:
            session.clear()
            session['username']=user_name

   
                
            if login is not None:
                return redirect(url_for('interface'))
            else:
                return render_template('login.html',user_exists=True)
        else:
            return render_template('login.html',user_exists=False)
    else:
        return render_template('login.html',user_exists=True)
        

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
            session.clear()
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html')
        except Exception as e:
            db.session.rollback()
            return "error"

    return render_template('register.html')

@app.route('/game',methods=['POST','GET'])
def game():
    
    if request.method=='GET':
        grid=[]
        row_sum=[]
        col_sum=[]
        indexes=[]
        print(session)
        if 'username' in session:
            print("True")
            User_name=session['username']
            session.clear()
            session['username']=User_name
        else:
            return "error"
        n=4
        
        for i in range(n):
            l=[]
            for j in range(n):
                l.append(random.randint(1,10))
            grid.append(l)
        row=[n]*n
        col=[n]*n    
        for i in range(n):
            x=random.randint(2,n-2)
            s=0
            l=[]
            for j in range(x):
                y=random.randint(0,n-1)
                print(col[y],n-i,n)
                while ( y in l or col[y]==1):
                    y=random.randint(0,n-1)
                l.append(y)
                row[i]-=1
                col[l[-1]]-=1
                
                s+=grid[i][l[-1]]
            indexes.append(l)
            print(row,col)
            row_sum.append(s)

        for i in range(n):
            s=0
            k=0
            for j in indexes:
                if i in j:
                    s+=grid[k][i]
                k+=1
            col_sum.append(s)
        session['grid']=grid
        session['indexes']=indexes
        session['row_sum']=row_sum
        session['col_sum']=col_sum
        session['lives']=3
        session['row']=row
        session['col']=col
    
        return render_template("game.html",board=session['grid'],row_sum=session['row_sum'],col_sum=session['col_sum'],hearts=session['lives'],row=session['row'],col=session['col'])
    if request.method=='POST':
        x=request.form['get_data'].split(',')
        x[0]=int(x[0])
        x[1]=int(x[1])
        if (session['grid'][x[0]][x[1]]==" "):
            return render_template("game.html",board=session['grid'],row_sum=session['row_sum'],col_sum=session['col_sum'],hearts=session['lives'],row=session['row'],col=session['col'])
        grid=session['grid']
        row=session['row']
        col=session['col']
        session.pop('grid')
        session.pop('row')
        session.pop('col')
        if x[1] not in session['indexes'][x[0]]:
            grid[x[0]][x[1]]=" "
            row[x[0]]-=1
            col[x[1]]-=1
        else:
            hearts=session['lives']
            session.pop('lives')
            hearts-=1
            session['lives']=hearts
        if session['lives']==0:
            session['result']=0
            return redirect(url_for('result'))
        n=len(grid)
        if row.count(0)==n and col.count(0)==n:
            session['result']=1
            return redirect(url_for('result'))
        session['grid']=grid
        session['row']=row
        session['col']=col
        print(session['grid'])
        return render_template("game.html",board=session['grid'],row_sum=session['row_sum'],col_sum=session['col_sum'],hearts=session['lives'],row=session['row'],col=session['col'])
@app.route('/result',methods=['POST','GET'])
def result():
    print("sesson")
    if request.method=='GET':
        print(session)

        if session['result']==1:
            
            
            end_time=time.time()
            period=end_time-session['begin_time']
            new_tuple = Userlog(username=session['username'], time=int(period))

            try:
                db.session.add(new_tuple)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return "error"
 
            return render_template("result.html", res=session['result'],time=period)
        else:

            return render_template("result.html", res=session['result'])
    if request.method=="POST":
        res=request.form["result_buttons"]
        if res=="1":
            return redirect(url_for("game"))
        elif res=="2":
            return redirect(url_for("leaderboard"))
                    
@app.route('/time',methods=['POST','GET'])
def stopwatch():
    
    if 'begin_time' not in session:
        now=time.time()
        session['begin_time']=now

    return render_template("time.html",time=time,begin_time=session['begin_time'])
@app.route('/interface',methods=['POST','GET'])
def interface():
    if request.method=='GET':
        return render_template("interface.html")
    if request.method=='POST':
        next_page=request.form['interface_buttons']
        print(next_page,type(next_page))
        if next_page=="1":
            return redirect(url_for('game'))
        elif next_page=="2":
            return redirect(url_for('leaderboard'))
        elif next_page=="0":
            return redirect(url_for('login'))
@app.route('/leaderboard',methods=['GET'])
def leaderboard():
    if request.method=='GET':
        x=Userlog.query.order_by(Userlog.time).limit(5).all()
        for i in x:
            print(i.time,x[0])
        print(x)
        return render_template("leader.html",leaderboard=x)

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)



