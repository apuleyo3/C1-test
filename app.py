from flask import Flask, render_template,redirect, url_for, request, jsonify, session
from forms import ContactForm, QuestNum, QuestSel, QuestFeed
from flask_mysqldb import MySQL
from mail import sendConf
import requests
import os
import datetime
import random
import numpy as np


SECRET_KEY = os.urandom(32)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = SECRET_KEY

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=60)
    session.modified = True
    #Flask.g.user = flask_login.current_user

'''
FIRST ROUTE 

RECEIVES USERS, IF A USER SAVED A PREVIOUS ASSESSMENT, *** IT JUST NOT LET IT DO IT AGAIN ***, DON'T KNOW IF IT'S WHAT YOU WANTED, BUT, IT CAN USE
IN FURTHER VERSIONS TO DETECT A NEWER ASSESSMENT
'''

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ContactForm()
    if request.method == 'POST':
        #RETRIEVE VARIABLES FROM FORM
        fname = form.firstname.data
        lname = form.lastname.data
        mail = form.email.data

        #SESSION VARIABLES
        session['username'] = mail
        session['key'] = SECRET_KEY
        session['time'] = datetime.datetime.now()
        session['position'] = 0

        #MAKING REQUESTS TO API SERVICE AND TRANSFORM TO A JSON OBJECT
        a = requests.get('http://172.17.0.4/api/v1/search?key=-----------------------------&elem=id&table=Users&where=email&val=' + mail)
        a = a.json()
        if len(a) > 0:
            #IF YOUR MAIL IS IN DATABASE, NO WAY JOSÉ, YOU CAN'T DO IT AGAIN
            return render_template("index.html", form=form, title='Data Scientist Assessment', message=1)
        else:
            #CREATE A NEW SUBMISSION TO KNOW THE DATE IT WAS CREATED AND COMPARE IT LATER TO GET THE SESSION EXPIRE
            requests.post("http://172.17.0.4/api/v1?key=-----------------------------&elems=name,lastname,email&table=Users&vals='" + fname + "','" + lname + "','" + mail + "'")
            b = requests.get('http://172.17.0.4/api/v1/search?key=-----------------------------&elem=id&table=Users&where=email&val=' + mail)
            b = b.json()

            #USER ID AND GROUP OF QUESTIONS IS STORED IN SESSION
            session['id'] = main_id = str(b[0][0])
            session['group'] = random.sample(range(1, 11), 6)
            requests.post("http://172.17.0.4/api/v1?key=-----------------------------&elems=user_id,status&table=Submission&vals='" + main_id + "',false")
            sub = requests.get('http://172.17.0.4/api/v1/search?key=-----------------------------&elem=id&table=Submission&where=id&val=' + main_id)
            sub = sub.json()
            session['sub'] = sub = str(sub[0][0])

            if len(b) > 0:
                uri = '/quest?id=' + main_id + '&q=0' + '&sub=' + sub
                return redirect(uri)
            else:
                return render_template("index.html", form=form, title='Data Scientist Assessment', message="2")

    return render_template("index.html", form=form, title='Data Scientist Assessment', message="0")

'''
SURVEY WRAPPER, IT EVALS IF THE USER HAS THE POSSIBLITY TO CONTINUE IN EVERY STEP, THEN IT FORWARDS USER TO HOME OR FEEDBACK
'''

@app.route("/quest", methods=['GET', 'POST'])
def quests():
    
    label = 'http://172.17.0.4/api/v1/search?key=-----------------------------&elem=id,category_id,q_text&table=Questions&where=id&val='
    pos = int(request.args['q'])
    gp_elem = list(session.get('group'))
    info = requests.get(label + str(gp_elem[pos]))
    info = info.json()
    my_type = int(info[0][1])
    text = str(info[0][2])

    aform = QuestSel()
    bform = QuestNum()

    session_init = datetime.datetime.strptime(str(session.get('time')), '%Y-%m-%d %H:%M:%S')
    present = datetime.datetime.now()
    session_time = present - session_init
    minutes = session_time.seconds / 60
    minutes = int(60-minutes)


    if request.method == 'POST':
        mtype = request.args['tp']
        user_id = request.args['id']
        q_id = int(request.args['sub'])
        uri = "http://172.17.0.4/api/v1?key=-----------------------------&elems=user_id,q_id,sb_id,q_ans&table=Answers&vals='"
        if mtype == '1':
            ans = aform.q_sel.data
            requests.post(uri + str(user_id) + "','" + str(q_id) + "','" + str(user_id) + "','" + str(ans) + "'")
        else:
            ans = bform.q_num.data
            requests.post(uri + str(user_id) + "','" + str(q_id) + "','" + str(user_id) + "','" + str(ans) + "'")

    if my_type == 1:
        ans = 'http://172.17.0.4/api/v1/search?key=-----------------------------&elem=q_text&table=Qoption&where=q_id&val='
        rev = requests.get(ans + str(gp_elem[pos]))
        rev = rev.json()
        groups_list = []
        for k,v in enumerate(rev):
            groups_list.append((k, v[0]))

    if 'q' in request.args:
        position = int(request.args['q'])
        my_id = str(request.args['id'])

        st = 'http://172.17.0.4/api/v1/search?key=-----------------------------&elem=status&table=Submission&where=id&val=' + my_id
        status = requests.get(st)
        status = status.json()
        status = int(status[0][0])

        if status > 0:
            return redirect('/')

        if minutes == 0:
            return redirect('/feedback?id=' + my_id)

        position += 1
        if position < 6:
            if my_type == 1:
                aform.q_sel.choices = groups_list
                return render_template("survey.html", title="Questionnaire", form=aform, tp=my_type, pos=position, id=my_id, sub=gp_elem[pos], text=text, time=minutes)
            else:
                return render_template("survey.html", title="Questionnaire", form=bform, tp=my_type, pos=position, id=my_id, sub=gp_elem[pos], text=text, time=minutes)
        else:
            fd = '/feedback?id=' + str(my_id)
            return redirect(fd)
    else:
        return redirect('/')

@app.route('/feedback', methods=['GET', 'POST'])
def feedme():
    form = QuestFeed()
    if request.method == 'POST':
        feed = form.q_feed.data
        uri = "http://172.17.0.4/api/v1?key=-----------------------------&elems=user_id,feed&table=Feedback&vals='"
        id = str(session.get('id'))
        requests.post(uri + id + "','" + feed + "'")
        receive = str(session.get('username'))
        sendConf(receive)
        for key in list(session.keys()):
            session.pop(key)
        return render_template("thanks.html", title="Thank you")

    if 'id' in request.args:
        pct = 'http://172.17.0.4/api/v1?key=-----------------------------&table=Submission&elem=status&val=1&id='
        sb = str(session.get('sub'))
        requests.patch(pct + sb)
        return render_template("feedback.html", title="Feedback", form=form)
    else:
        return redirect('/')


app.run(host='0.0.0.0', port=80)
