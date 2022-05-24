from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from main_flask import db, login_manager
from flask_login import UserMixin
# ^ would allow us to have required attrs and methods for the login

@login_manager.user_loader # will expect the User model to have some certain attrs and methods
def load_user(user_id):
    return User.query.get(int(user_id)) 
# for the extension to know that this is the func that gets a user by a user_id

# creating the user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #                               ^ would be hashed and the algorithm would make that specified chars long
    posts = db.relationship('Post', backref='author', lazy=True)
    # posts has a relationship to the post model
    # backref -> like creating a col in Post module
    # lazy -> defines when SQL Alch loads data from the datbas
    # True -> SQLALCH will load the data as necessary in one go
    # we wouldn't see that posts col

    # # Creating a token for a user 
    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    # # For verifying the token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # we used user as lowercase coz in the user model we are referncing the actual post class
    # User set its name as the lowercase user
    # ^ means: we are accessing the table name and the col name

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
