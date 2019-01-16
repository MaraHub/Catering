from flask import Flask,render_template,request,jsonify,redirect, url_for
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import random
app = Flask(__name__)


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

@app.route('/menu/',methods=['GET','POST'])
def menu():
    voter = request.args.get('reservation__form__name')
    code = request.args.get('reservation__form__phone')
    entre = db.session.query(MenuAvailable.item).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='entre')).all()
    kyriws = db.session.query(MenuAvailable.item).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='main')).all()
    desserts = db.session.query(MenuAvailable.item).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='dessert')).all()
    drinks = db.session.query(MenuAvailable.item).filter(and_(MenuAvailable.event_code == code,MenuAvailable.submenu=='drinks')).all()
    entre = [str(item).replace("'","").replace("(","").replace(")","").replace(",","") for item in entre]
    kyriws = [str(item).replace("'","").replace("(","").replace(")","").replace(",","") for item in kyriws]
    desserts = [str(item).replace("'","").replace("(","").replace(")","").replace(",","") for item in desserts]
    drinks = [str(item).replace("'","").replace("(","").replace(")","").replace(",","") for item in drinks]

    #print(type(list_[0]))

    return render_template('menu.html',entre = entre,kyriws=kyriws,desserts=desserts,drinks=drinks)

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
        entree = json.loads(request.form['entree'])
        kyriws = json.loads(request.form['kyriws'])
        desserts = json.loads(request.form['desserts'])
        drinks = json.loads(request.form['drinks'])
        voter = request.form['voter']
        event_code = request.form['event_code']

        for item in entree:
            new_entry = MenuVote(event_code,voter,'entree',item.strip())
            db.session.add(new_entry)
            db.session.commit()

        for item in kyriws:
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



    return {'status':'OK'}



@app.route('/submit_menu',methods=['POST','GET'])
def submit_menu():
    return render_template('submit_menu.html')





## Run the App
if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
