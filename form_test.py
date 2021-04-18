from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask,render_template

import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


app = Flask(__name__)
app.config.from_object(Config)



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign In')
@app.route('/ent',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Login requested for user {}, remember_me={}'.format(
            form.username.data, "u"))
    else:
        print("no")
    return render_template('form.html', title='Sign In', form=form)

if __name__=='__main__':
    app.run()