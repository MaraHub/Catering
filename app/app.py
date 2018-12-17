from flask import Flask,render_template
app = Flask(__name__)

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

## Run the App
if __name__ == '__main__':
  app.run(host='0.0.0.0')
