from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, defaultload, lazyload
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
# we instanciated the flask app in the "app" variable
# setting up a secret key
app.config["SECRET_KEY"] = 'c647aaa08100111e2cf2b392828dbc0f'
# ^ could be set as an env var
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
# /// are relative paths from the current file
db = SQLAlchemy(app)
# ^ setting an instance

# creating the user model


class User(db.Model):
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

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


postss = [

    {
        'user': 'Jasurbek Mamurov',
        'title': 'Blog #1',
        'content': 'Blog #1"s content',
        'date_posted': 'July 25, 2021'
    },
    {
        'user': 'Jack Collins',
        'title': 'Blog #2',
        'content': 'Blog #2"s content',
        'date_posted': 'July 26, 2021'
    }

]


@app.route("/")
@app.route("/home")  # two routes are available for the same page
# ^ what we type into the brow to go to some pages
# ^ these route decorators are used to create pages
# ^ allow us to write a func that  returns the information
# that will be shown on our website for this specific route
# / is the root page
def home():
    return render_template('home_temp.html', posts=postss)
# we intend to return the html template in this func
# we would render the template
# whatever variable name we use as the
# argument name here that we pass in we will
# have access to that variable in our template


@app.route("/about")
def about():
    return render_template('about_temp.html', title='About')


# specifying allowed methods\
# getting the registration info posted and directing to the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # would be passes to a template
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
    # ^ was the form validated when submitted?
        # redirecting
        return redirect(url_for('home'))
        # the name of the func     ^
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # would be passes to a template
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            #                                   ^ bootstrap class
            return redirect(url_for('home'))
        else:
            flash('Logging is unsuccessful', 'danger')
            #           red alert               ^
    return render_template('login.html', title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
