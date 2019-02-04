
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import (LoginManager, UserMixin, login_required,
                           login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())


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

#
#
# class MenuAvailableTemp(db.Model):
#     __tablename__ = 'availableMenutemp'
#     event_code = db.Column('event_code',db.Integer,primary_key=True)
#     submenu = db.Column('submenu',db.Unicode,primary_key=True)
#     dish = db.Column('dish',db.Unicode,primary_key=True)
#     dish_desc = db.Column('dish_desc',db.Unicode)
#     image_path = db.Column('image_path',db.Unicode)
#
#     def __init__(self,event_code,submenu,dish,dish_desc,image_path):
#         self.event_code = event_code
#         self.submenu = submenu
#         self.dish = dish
#         self.dish_desc = dish_desc
#         self.image_path = image_path
