import secrets
# ^ for creating a random hex
import os
# ^ for getting an extension
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from main_flask import app, db, bcrypt
from main_flask.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from main_flask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")  # two routes are available for the same page
# ^ what we type into the brow to go to some pages
# ^ these route decorators are used to create pages
# ^ allow us to write a func that  returns the information
# that will be shown on our website for this specific route
# / is the root page
def home():
    posts = Post.query.all()
    return render_template('home_temp.html', posts=posts)
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # for saving as the same file ext as before
    _, f_ext = os.path.splitext(form_picture.filename)
    # form_picture -> data from the field that the user submits and there is the filename
    picture_fn = random_hex + f_ext
    # ^ complete name of the picture 
    picture_path = os.path.join(app.root_path, 'static\profile_pics', picture_fn)
    # ^ for saving in the specified dir 
    # app.root_path -> the full path all the way up to our package directory
    # os.path.join -> to concat properly all of the data
    
    # resizing and saving the picture into our path

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size) 
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required # we need to login before getting to account page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # changin' info in SQLAlchemy
        # (below) coz that's optional, so we check 
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('The account has been successfully modified!', category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        # ^ populating the form with our user's data
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file )
    return render_template('account.html', title="Account", 
                           image_file=image_file, form=form)
    # ! ^ we are not in the same indentation with redirect coz of "post get redirect pattern"
    # avoid using two post requests at one time 

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('The post has been shared successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title = 'New Post', form = form)