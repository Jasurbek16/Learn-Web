from flask import render_template, url_for, flash, redirect, request
from main_flask import app, db, bcrypt
from main_flask.forms import RegistrationForm, LoginForm
from main_flask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



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
# methods -- for allowed methods -- 'POST' -- allow posting typed info to this route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        # ^ when the user has already registered
    form = RegistrationForm()  # would be passes to a template
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # ^ hashing the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # we used the hashed_password in the argument sec, coz we don't want the plain text
        db.session.add(user)
        db.session.commit()
        flash(f'The account has been created! You\'re now able to login', 'success')
    # ^ was the form validated when submitted?
        # redirecting
        return redirect(url_for('login'))
        # the name of the func     ^
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()  # would be passes to a template
    if form.validate_on_submit():
        user = User.query.filter_by(email =form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # ^ logging in helper
            next_page = request.args.get('next')
            # ^ looking at the page we were trying to log into before going here 
            # ^ args is a dict
            # ^ we have used the get coz if the key does not exit, then we do not get an error
            flash(f'Welcome to the account {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))  
        else:
            flash('Logging was unsuccessful. Please, consider entering again!', 'danger')
            #           red alert               ^
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required # we need to login before getting to account page
def account():
    return render_template('account.html', title="Account")



