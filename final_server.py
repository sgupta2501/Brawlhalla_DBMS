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
def search_rank2V2(s):
    if(s==0):
        return("no competitive stats available")
    cur.execute("select * from players_2v2 where rankp="+str(s))
    data=cur.fetchall()
    return data
def search_rank(s):
    if(s==0):
        return("no competitive stats available")
    cur.execute("select * from players_1v1 where rankp="+str(s))
    data=cur.fetchall()
    return data

def search_legends(s):
    query="select * from legends where legend_name_key="+'\''+s+'\''
   
    try:
        cur.execute(query)
        data=cur.fetchall()
        return data
    except mysql.connector.Error as err:
        return(err)





# def insert_steamid(s):

#     api_key="4S1L2NNFYUEZ6V3RUE4W"
#     res=requests.get("https://api.brawlhalla.com/search?steamid="+str(s)+"&api_key="+api_key);
#     data=json.loads(res.text)
#     brawl_id=str(data['brawlhalla_id'])
#     res2=requests.get("https://api.brawlhalla.com/player/"+brawl_id+"/ranked?api_key="+api_key)
#     data2=json.loads(res2.text)
#     rank=data2['global_rank']
#     # if(rank==0):
#     #     return("no competitive stats available")
#     temp=(rank,data2['name'],data2['brawlhalla_id'],data2['region'],data2['legends'][0]['legend_id'])
#     sql = "insert into test_table  values (%s,%s,%s,%s,%s)"
#     try:
#         cur.execute(sql,temp)
#         mydb.commit()
#         return("data added")
#     except mysql.connector.Error as err:
#         return(err)



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


app = Flask(__name__)
app.config.from_object(Config)



class LoginForm(FlaskForm):
    username = IntegerField('rank:', validators=[DataRequired()])

    submit = SubmitField('Enter')
class LoginForm2(FlaskForm):
    rankp = IntegerField('rank:', validators=[DataRequired()])

    submit = SubmitField('Enter')
class LoginForm3(FlaskForm):
    name = StringField('legend name:', validators=[DataRequired()])

    submit = SubmitField('Enter')
main_query="select players_1v1.rankp , players_1v1.name , players_1v1.region , legends.legend_name_key  from players_1v1,legends where players_1v1.best_legend = legends.legend_id ;"
cur.execute(main_query)
data=cur.fetchall()




@app.route('/',methods=['GET'])
def example(): 
    # cur.execute("select * from legends") 
    # data = cursor.fetchall() 
    return render_template("index.html", test=data) 

@app.route('/ent',methods=['GET','POST'])
def login():
    steam_id=int(0)
    form = LoginForm()
    data=str('')
    message=('')
    if form.validate_on_submit():
        if(form.username.data>50 or form.username.data<0):
            message="enter value 0-50"
        else:
            message=''
        data=search_rank(form.username.data)
        # print('Login requested for user {}    , remember_me={}'.format(
        #     form.username.data, "u"))
    else:
        print("no")
    return render_template('form.html', title='Sign In', form=form, answer=data,message=message)


@app.route('/ent2',methods=['GET','POST'])
def form2():
    form=LoginForm2()
    data=str('')
    message=''
    if form.validate_on_submit():
        if(form.rankp.data>47 or form.rankp.data<0):
            message="enter value 1-47"
        else:
            message=''
        data=search_rank2V2(form.rankp.data)
    # print('Login requested for user {}, remember_me={}'.format(
    #     form.username.data, "u"))
    else:
        print("no")
    return render_template('form2.html', title='Sign In', form=form, answer=data,message=message)

@app.route('/legends',methods=['GET','POST'])
def s_legend():
    form=LoginForm3()
    data=str('')
    message=str('')
    if form.validate_on_submit():
        data=search_legends(form.name.data)
        if(len(data)==0):
            message='enter valid name'
        else:
            message=''
    # print('Login requested for user {}, remember_me={}'.format(
    #     form.username.data, "u"))
    else:
        print("no")
    return render_template('legends.html', title='Sign In', form=form, answer=data,message=message)

if __name__ == '__main__':
    app.run(debug=True) 
    app.static_folder = 'static'