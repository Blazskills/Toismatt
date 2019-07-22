from test import app
from flask_login import LoginManager,UserMixin,login_user, logout_user, login_required,current_user
from test import db
from flask import Flask,redirect, url_for, render_template, request, flash
from models import Regtb
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
      reg_info = Regtb.query.all()
      return render_template('index.html',reg_info=reg_info)

#Register route
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method =='POST':
          try:
            Name = request.form['Name']
            Email = request.form['Email']
            Password = request.form['Password']
            Confirm_Password = request.form['Confirm_Password']
            secure_password = generate_password_hash(Password, method="sha256")
            if Password == Confirm_Password:
              new_reg = Regtb(Name=Name,Email=Email,Password=secure_password)
              db.session.add(new_reg)
              db.session.commit()
              flash("You are registed and can login","success")
              return redirect(url_for('login'))
            else:
                  flash("password does not match","danger")
                  return render_template('register.html')
          except:
            pass
            db.session.rollback()
            flash("email already existed","danger")
    return render_template('register.html')

#Login route
@app.route('/login',methods=['GET','POST'])
def login():
   if request.method == 'POST':
      Name=request.form['Name']
      Password=request.form['Password']
      user=Regtb.query.filter_by(Name=Name).first()
      if user:
         if check_password_hash(user.Password,Password):
               login_user(user) #save session
               flash("Login successful","success")
               return redirect(url_for('index'))
         else:
            flash("wrong password","danger")
            return render_template('login.html')
      else:
         flash("wrong username","danger")
         return render_template('login.html')


   return render_template('login.html')


#logout route
@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash("You're logout Successfully","success")
  return redirect(url_for('index'))