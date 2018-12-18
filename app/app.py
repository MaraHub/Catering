from flask import Flask,render_template,request,jsonify
import json
app = Flask(__name__)


def array(list):
    string = ""
    for x in list:
        string+= x
    return string



@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/mainpage')
def main():
    return render_template('index.html',kyriws = ['Patatosalata','Gemista','Tzatzikara'])

@app.route('/menu')
def menu():
    return render_template('menu.html',kyriws = {'Patatosalata',
                                                'Gemista',
                                                'Tzatzikara',
                                                'Makaronia',
                                                'Rizoto'})

@app.route('/receiver',methods=['POST','GET'])
def worker():
    #data = json.loads(request.form['cars'])
    return 'ok'


## Run the App
if __name__ == '__main__':
  app.run(debug=True)
