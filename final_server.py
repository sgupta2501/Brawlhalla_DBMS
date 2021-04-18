from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.validators import DataRequired
from flask import Flask,render_template
import os
import requests
import mysql.connector
import sys
import json
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="hello0hello",
database="brawlhalla"
)
cur=mydb.cursor()
def insert_steamid(s):

    api_key="4S1L2NNFYUEZ6V3RUE4W"
    res=requests.get("https://api.brawlhalla.com/search?steamid="+str(s)+"&api_key="+api_key);
    data=json.loads(res.text)
    brawl_id=str(data['brawlhalla_id'])
    res2=requests.get("https://api.brawlhalla.com/player/"+brawl_id+"/ranked?api_key="+api_key)
    data2=json.loads(res2.text)
    rank=data2['global_rank']
    # if(rank==0):
    #     return("no competitive stats available")
    temp=(rank,data2['name'],data2['brawlhalla_id'],data2['region'],data2['legends'][0]['legend_id'])
    sql = "insert into test_table  values (%s,%s,%s,%s,%s)"
    try:
        cur.execute(sql,temp)
        mydb.commit()
        return("data added")
    except mysql.connector.Error as err:
        return(err)



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


app = Flask(__name__)
app.config.from_object(Config)



class LoginForm(FlaskForm):
    username = IntegerField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign In')


main_query="select players_1v1.rankp , players_1v1.name , players_1v1.region , legends.legend_name_key  from players_1v1,legends where players_1v1.best_legend = legends.legend_id ;"
cur.execute(main_query)
data=cur.fetchall()




@app.route('/',methods=['GET','POST'])
def example(): 
    print("ss")
    # cursor.execute("select * from legends") 
    # data = cursor.fetchall() 
    return render_template("index.html", test=data) 

@app.route('/ent',methods=['GET','POST'])
def login():
    steam_id=int(0)
    form = LoginForm()
    msg=str('')
    if form.validate_on_submit():
        msg=insert_steamid(form.username.data)
        print(msg)
        # print('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, "u"))
    else:
        print("no")
    return render_template('form.html', title='Sign In', form=form, message=msg)
if __name__ == '__main__':
    app.run(debug=True)	
