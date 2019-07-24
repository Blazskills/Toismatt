from flask import Flask,request,url_for, render_template
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from test import app
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')


@app.route('index2', methods=['GET', 'POST'])
def index2():
    try:
        if request.method =='GET':
            return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
        email = request.form['email']
        token = s.dumps(email, salt='email-confirm')
        msg = Message('confirm_email', sender='ilesanmiisaac@gmail.com', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)
        return '<h1>The email you entered is {}.The token is {}</h1>'.format(email,link, token)
    except:
        return "<h1 Style=color:red;>Network error</h1>"

# route for token confirmation 
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
         email = s.loads(token, salt='email-confirm', max_age=1000)
    except:
        return '<h1> The token is expired!</h1>'

    return '<h1>This token works!</h1>'


if __name__ == '__main__':
    app.run(debug=True)