from flask import Flask, render_template,redirect,url_for,request
from flask_login import LoginManager,login_user,logout_user,UserMixin,current_user
from flask_sqlalchemy import SQLAlchemy
import os
app=Flask(__name__)
file_path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'project.db')
app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{file_path}"
app.config['SECRET_KEY']='abc'

db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class Users(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False)
    fullname=db.Column(db.String(200),nullable=False)
    username=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False,unique=True)

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("Error creating database",e)

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        person=Users.query.filter_by(username=username).first()
        if person.password==password:
            login_user(person)
            return render_template('explore.html')
    if current_user.is_authenticated:
        return render_template("explore.html")
    else:
        return render_template("home.html")
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        fullname=request.form.get('fullname')
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        user=Users(fullname=fullname,email=email,username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return render_template('home.html')
    return render_template("signup.html")
@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/explore')
def explore():
    return render_template("explore.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
if __name__== '__main__':
    app.run(debug=True)