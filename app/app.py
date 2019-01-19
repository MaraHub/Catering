from flask import Flask,render_template,request,jsonify,redirect, url_for,session
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import random
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

## Database Initializatrion and stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Aajlm1981#@localhost/catering_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MenuVote(db.Model):
    __tablename__ = 'menuvote'
    event_code = db.Column('event_code',db.Integer,primary_key=True)
    voter = db.Column('voter',db.Unicode,primary_key=True)
    submenu = db.Column('submenu',db.Unicode,primary_key=True)
    item = db.Column('item',db.Unicode,primary_key=True)

    def __init__(self,event_code,voter,submenu,item):
        self.event_code = event_code
        self.voter = voter
        self.submenu = submenu
        self.item = item


class MenuAvailable(db.Model):
    __tablename__ = 'availableMenu'
    event_code = db.Column('event_code',db.Integer,primary_key=True)
    submenu = db.Column('submenu',db.Unicode,primary_key=True)
    dish = db.Column('dish',db.Unicode,primary_key=True)
    dish_desc = db.Column('dish_desc',db.Unicode)
    image_path = db.Column('image_path',db.Unicode)

    def __init__(self,event_code,submenu,dish,dish_desc,image_path):
        self.event_code = event_code
        self.submenu = submenu
        self.dish = dish
        self.dish_desc = dish_desc
        self.image_path = image_path


def array(list):
    string = ""
    for x in list:
        string+= x
    return string



# @app.route('/<inname>',methods = ['POST','GET'])
# def hello_world(inname):
#     if request.method == "GET":
#         return 'Hello World'

@app.route('/mainpage')
def main():
    #print("---------------------------------------------------------------------------------")
    #print("---------------------------------------------------------------------------------")
    #return 'hi there'
    return render_template('index.html',kyriws = ['Patatosalata','Gemista','Tzatzikara'])


def clean_text(str_):
    return str_.replace("'","").replace("(","").replace(")","").replace(",","")


@app.route('/menu/',methods=['GET','POST'])
def menu():
    voter = request.args.get('reservation__form__name')
    code = request.args.get('reservation__form__phone')

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

@app.route('/event_login',methods=['POST','GET'])
def event_login():

    if request.method=='GET':
        print("hello frrm GET")
        voter = request.args.get['reservation__form__name']
        print(str(voter))
        code = request.args.get['reservation__form__phone']

        return redirect(url_for('menu',reservation__form__name=voter,
                                        reservation__form__phone=code,
                                        reservation__form__email = 'test@email.com'
                                        ))



@app.route('/receiver',methods=['POST','GET'])
def receiver():
    if request.method=='POST':
        print("hello from Receiver")
        starters = json.loads(request.form['starters'])
        main = json.loads(request.form['main'])
        desserts = json.loads(request.form['desserts'])
        drinks = json.loads(request.form['drinks'])
        voter = request.form['voter']
        event_code = request.form['event_code']

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


    return {'status':'OK'}


@app.route('/receiver2',methods=['POST','GET'])
def receiver2():
    if request.method=='POST':
        print("hello from Receiver2")

        dish_starter = json.loads(request.form['dish_starter'])
        desc_starter = json.loads(request.form['desc_starter'])
        dish_main = json.loads(request.form['dish_main'])
        desc_main = json.loads(request.form['desc_main'])
        dish_desserts = json.loads(request.form['dish_desserts'])
        desc_desserts = json.loads(request.form['desc_desserts'])
        drinks = json.loads(request.form['drinks'])
        desc_drinks = json.loads(request.form['desc_drinks'])



        # for item in dish_starter:
        #     newEntry = MenuVote()
        print(dish_starter)
        print(desc_starter)


        event_code = random.randint(100000,1000000)
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



        session['evnt_cd'] = event_code
        return jsonify(dict(redirect=url_for('submit_menu_confirmation')))
        #redirect(url_for('submit_menu_confirmation'))




@app.route('/submit_menu')
def submit_menu():
    return render_template('submit_menu.html')

@app.route('/submit_menu_confirmation')
def submit_menu_confirmation():
    print('hello from confirmation')
    code = session.get('evnt_cd',None)

    starter = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='starter')).all()]
    starter_desc = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish_desc).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='starter')).all()]

    main = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='main')).all()]
    main_desc = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish_desc).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='main')).all()]

    desserts = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='desserts')).all()]
    desserts_desc = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish_desc).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='desserts')).all()]

    drinks = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='drinks')).all()]
    drinks_desc = [clean_text(str(item)) for item in db.session.query(MenuAvailable.dish_desc).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='drinks')).all()]



    return render_template('sbmt_menu_cnfrm_page.html',event_code=code,starter = starter,starter_desc = starter_desc,
                                       main=main,main_desc = main_desc,
                                       desserts=desserts,desserts_desc = desserts_desc,
                                       drinks=drinks,drinks_desc=drinks_desc)

@app.route('/display_event_code')
def display_event_code():
    return render_template('display_event_code.html',event_code=session.get('evnt_cd'))



## Run the App
if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
