from test import app
from flask_login import LoginManager,UserMixin,login_user, logout_user, login_required,current_user
from test import db
from flask import Flask,redirect, url_for, render_template, request, flash
from models import Regtb
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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




@app.route('/reset',methods=['GET','POST'])
def reset():
      if request.method == 'POST':
             Email=request.form['Email']
             user=Regtb.query.filter_by(Email=Email).first()
             if user:
                   code = str(id.uuid4())
                   user.change_configuration={"password_reset_code":code}
                   user.save()

                   #emsil the user
                   body_html = render_template('mail/user/password_reset.html', user =user)
                   body_text = render_template('mail/user/password_reset.html', user =user)
                   Email(user.Email,"password reset request", body_html, body_text)
                   #remove later
                   flash('There is an account with that email. you can now change your password','success')
                   return render_template('index.html')   
             flash('There is no account with that email. You must register first','danger')
             return render_template('reset.html')    
      return render_template('reset.html')


# @app.route('/resetpassword',methods=['GET','POST'])
# # @login_required
# def send_password_reset_email(user_email):
#        password_reset_serializer = Serializer(app.config['SECRET_KEY'])
#        password_reset_url = url_for('users.reset_with_token',token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),_external=True)
#        html = render_template( 'email_password_reset.html', password_reset_url=password_reset_url)
#       send_email('Password Reset Requested', [user_email], html)
      #  if reset():
      #         if request.method == 'POST':
      #                Password = request.form['Password']
      #                Confirm_Password = request.form['Confirm_Password']
      #                secure_password = generate_password_hash(Password, method="sha256")
      #                if Password == Confirm_Password:
      #                      return render_template('index.html')
      #         flash('something went wrong','danger')
      #         return render_template('index.html')   

      #  return render_template('resetpassword.html')


#   @app.route('/reset',methods=['GET','POST'])
#   def reset():
#    if request.method == 'POST':
#       Email=request.form['Email']
#       user=Regtb.query.filter_by(Email=Email).first()
#    return render_template('reset.html')
