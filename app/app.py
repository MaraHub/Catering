
############################## Imports ##########################
#################################################################

from flask import Flask,render_template,request,jsonify,redirect, url_for,session
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import random
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_required, login_user, \
    logout_user, current_user, UserMixin
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
import datetime
from config import Config,DevConfig,ProdConfig,Auth
from models import db,MenuAvailable,User,MenuVote
from help_functions import clean_text
############################## App ##########################
#################################################################
app = Flask(__name__)
app.secret_key = os.urandom(24)

## Database Initializatrion and stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Aajlm1981#@localhost/catering_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

## Login stuff
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
############################## App ##########################
#################################################################


############################## Routes ##########################
#################################################################


############################## MainPage Start ##########################
#################################################################
@app.route('/mainpage')
def main():
    return render_template('index.html')

############################## MainPage End ##########################
#################################################################


#####################Voter Section Start ##########################
#################################################################

######## Display MenuAvailable for voting given the name and Event code Id
## It picks up the voter name and code from the
@app.route('/menu/',methods=['GET','POST'])
def menu():
    if  request.args.get('voter_name'):
        voter = request.args.get('voter_name')
        print("the voter is : "+voter)
        code = request.args.get('event_code_id')
        print("the code is : "+str(code))
        session['voter_vote'] = voter
        session['event_code'] = code
    else:
        voter = session['voter_vote']
        code = session['event_code']
    starter = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='starter')).all()]
    starter_desc = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish_desc).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='starter')).all()]

    main = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='main')).all()]
    main_desc = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish_desc).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='main')).all()]

    desserts = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='desserts')).all()]
    desserts_desc = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish_desc).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='desserts')).all()]

    drinks = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='drinks')).all()]
    drinks_desc = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish_desc).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='drinks')).all()]


    return render_template('menu.html',starter = starter,starter_desc = starter_desc,
                                       main=main,main_desc = main_desc,
                                       desserts=desserts,desserts_desc = desserts_desc,
                                       drinks=drinks,drinks_desc=drinks_desc)

########## This is the Route that gets the menu voted from the guests and saves it in the MenuVote table
########## Refers to submit_menu_guest JS function
@app.route('/post_menu_voted',methods=['POST','GET'])
def post_menu_voted():
    if request.method=='POST':
        print("hello from post_menu_voted")
        session['starters_vote'] = json.loads(request.form['starters'])
        session['main_vote'] = json.loads(request.form['main'])
        session['desserts_vote'] = json.loads(request.form['desserts'])
        session['drinks_vote'] = json.loads(request.form['drinks'])
        return jsonify(dict(redirect=url_for('menu_voted_conf')))

@app.route('/menu_voted_conf')
def menu_voted_conf():
    return render_template('menu_voted_conf.html')

@app.route('/menu_voted_submitted')
def menu_voted_submitted():
    starters = session['starters_vote']
    main = session['main_vote']
    desserts = session['desserts_vote']
    drinks = session['drinks_vote']
    voter = session['voter_vote']
    event_code = session['event_code']
    for item in starters:
        new_entry = MenuVote(event_code,voter,'starters',item.strip())
        db.session.add(new_entry)
        db.session.commit()

    for item in main:
        new_entry = MenuVote(event_code,voter,'main',item.strip())
        db.session.add(new_entry)
        db.session.commit()
    for item in desserts:
        new_entry = MenuVote(event_code,voter,'desserts',item.strip())
        db.session.add(new_entry)
        db.session.commit()
    for item in drinks:
        new_entry = MenuVote(event_code,voter,'drinks',item.strip())
        db.session.add(new_entry)
        db.session.commit()

    return render_template('menu_voted_thanks.html')


#####################Voter Section End ##########################
#################################################################


######################################################################
#####################Business Section Start ##########################
######################################################################


########## This is the Catering Business Part
@app.route('/submit_menu')
@login_required
def submit_menu():
    print("###########################")
    print(current_user)
    print("###########################")
    return render_template('submit_menu.html')




@app.route('/receiver2',methods=['POST','GET'])
def receiver2():
    if request.method=='POST':
        print("hello from Receiver2")

        session['dish_starter'] = json.loads(request.form['dish_starter'])
        session['desc_starter'] = json.loads(request.form['desc_starter'])
        session['dish_main'] = json.loads(request.form['dish_main'])
        session['desc_main'] = json.loads(request.form['desc_main'])
        session['dish_desserts'] = json.loads(request.form['dish_desserts'])
        session['desc_desserts'] = json.loads(request.form['desc_desserts'])
        session['drinks'] = json.loads(request.form['drinks'])
        session['desc_drinks'] = json.loads(request.form['desc_drinks'])

        return jsonify(dict(redirect=url_for('submit_menu_confirmation')))


@app.route('/submit_menu_confirmation')
def submit_menu_confirmation():
    print('hello from confirmation')

    return render_template('sbmt_menu_cnfrm_page.html',starter = session.get('dish_starter',None),
                                                        starter_desc = session.get('desc_starter',None),
                                                        main=session.get('dish_main',None),main_desc = session['desc_main'],
                                       desserts=session['dish_desserts'],desserts_desc = session['desc_desserts'],
                                       drinks=session['drinks'],drinks_desc=session['desc_drinks'])


@app.route('/change_input')
def change_input():
    return render_template('change_menu_input.html',starter = session.get('dish_starter',None),
                                                        starter_desc = session.get('desc_starter',None),
                                                        main=session.get('dish_main',None),main_desc = session['desc_main'],
                                       desserts=session['dish_desserts'],desserts_desc = session['desc_desserts'],
                                       drinks=session['drinks'],drinks_desc=session['desc_drinks'])


@app.route('/display_event_code')
def display_event_code():
    event_code = random.randint(100000,1000000)
    dish_starter = session['dish_starter']
    desc_starter = session['desc_starter']
    dish_main = session['dish_main']
    desc_main = session['desc_main']
    dish_desserts = session['dish_desserts']
    desc_desserts = session['desc_desserts']
    drinks = session['drinks']
    desc_drinks = session['desc_drinks']

    g=0
    for dish in dish_starter:
        new_entry = MenuAvailable(event_code,'starter', dish['value'],desc_starter[g]['value'],'')
        db.session.add(new_entry)
        db.session.commit()
        g+=1
    g=0
    for dish in dish_main:
        new_entry = MenuAvailable(event_code,'main', dish['value'],desc_main[g]['value'],'')
        db.session.add(new_entry)
        db.session.commit()
        g+=1
    g=0
    for dish in dish_desserts:
        new_entry = MenuAvailable(event_code,'desserts', dish['value'],desc_desserts[g]['value'],'')
        db.session.add(new_entry)
        db.session.commit()
        g+=1
    g=0
    for dish in drinks:
        new_entry = MenuAvailable(event_code,'drinks', dish['value'],desc_drinks[g]['value'],'')
        db.session.add(new_entry)
        db.session.commit()
        g+=1



    return render_template('display_event_code.html',event_code=event_code)

#######################################################
############### Google Login ##########################
#######################################################

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth



@app.route('/login')
def login():
    if current_user.is_authenticated:
        print("user is authenticated")
        return redirect(url_for('index'))
    print("user is NOT authenticated")
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.REQUEST_AUTHORIZATION,
        access_type='offline',
        prompt='select_account')
    #redirect()
    session['oauth_state'] = state
    return render_template('login.html',google_auth = auth_url)




@app.route('/google_login')
def google_login():
    # Redirect user to home page if already logged in.
    print(current_user)
    print("---------------------------------------")
    print("Hello formo google redirect uri - submit_menu")
    print("---------------------------------------")
    print(request.args)
    print("---------------------------------------")
    print("---------------------------------------")
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    # if 'code' not in request.args and 'state' not in request.args:
    #     return redirect(url_for('login'))

    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        print("---------------------------------------")
        print("Hello from getting token")
        print("---------------------------------------")

        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                # Here is where he gets the response
                authorization_response=request.url)

        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            print(token)
            print(user.name)
            print(user.email)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            print(current_user)
            return redirect(url_for('submit_menu'))
        return 'Could not fetch your information.'



@app.route('/')
@login_required
def index():
    return render_template('login.html')



##### Apendix
# @app.route('/event_login',methods=['POST','GET'])
# def event_login():
#
#     if request.method=='GET':
#         print("hello frrm GET")
#         voter = request.args.get['reservation__form__name']
#         print(str(voter))
#         code = request.args.get['reservation__form__phone']
#
#         return redirect(url_for('menu',reservation__form__name=voter,
#                                         reservation__form__phone=code,
#                                         reservation__form__email = 'test@email.com'
#                                         ))







## Run the App
if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True,ssl_context='adhoc')
