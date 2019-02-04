from app import app
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask_login import login_required, login_user,current_user, logout_user
from .models import User, Post, Category, Feedback, db
from .forms import ContactForm, LoginForm
from .utils import send_mail





@app.route('/login_options', methods=['GET', 'POST'])
def login_options():
    return render_template('login.html')



@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # if request.method == 'POST':
    #     print("hello from upload_file")
    #     f = request.files['file']
    #     print(f)
    #     f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('submit_menu'))




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

@app.route('/change_input')
def change_input():
    return render_template('change_menu_input.html')
