from flask import Flask,render_template,request,jsonify
import json
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('index.html',kyriws = ['Patatosalata','Gemista','Tzatzikara'])

@app.route('/menu/<voter>/<event_code>',methods=['GET','POST'])
def menu(voter,event_code):

    return render_template('menu.html',kyriws = {'Patatosalata',
                                                'Gemista',
                                                'Tzatzikara',
                                                'Makaronia',
                                                'Rizoto'})

@app.route('/receiver',methods=['POST','GET'])
def receiver():
    if request.method=='POST':
        print("hello from Receiver")
        food = json.loads(request.form['food'])
        voter = request.form['voter']
        event_code = request.form['event_code']
        submenu = request.form['submenu']
        for item in food:
            new_entry = MenuVote(event_code,voter,submenu,item.strip())
            db.session.add(new_entry)
            db.session.commit()
    return {'status':'OK'}


        #new_entry = Example(id_,food)
        #db.session.add(new_entry)
        #db.session.commit()


## Run the App
if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
