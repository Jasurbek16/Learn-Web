import os
# ^ for getting an extension
import secrets
# ^ for creating a random hex
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from main_flask import app, db, bcrypt#, mail
from main_flask.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm)#, RequestResetForm, ResetPasswordForm)
from main_flask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
# from flask_mail import Message


# ^ for being able to send an email

@app.route("/")
@app.route("/home")  # two routes are available for the same page
# ^ what we type into the brow to go to some pages
# ^ these route decorators are used to create pages
# ^ allow us to write a func that  returns the information
# that will be shown on our website for this specific route
# / is the root page
def home():
    page = request.args.get('page', 1, type=int)
    # ^ getting the page specified from the query parameter in the URL
    # page is also the optional parameter in the URL
    # 1 -> default page
    # if non-int is passed, then there appears an error
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page ,per_page = 5)
    # ^ order when querying and paginate
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
    return render_template('create_post.html', 
    title = 'New Post', form = form, legend = 'New Post')

@app.route('/post/<int:post_id>')
# putting a variable into ^ the url
# we have said that we expect that to be an int
def post(post_id):
    post = Post.query.get_or_404(post_id)
    # ^ gives the post page but if that doesn't exist, then give me 404
    return render_template("post.html", title = 'Post ⚙', post = post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        # aborting an HTTP response for the forbidden route
    else:
        form = PostForm()
        form.submit.data = "Update"
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data 
            db.session.commit()
            flash('The post has been modified!', 'success')
            return redirect(url_for('post', post_id = post.id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template('create_post.html', 
        title = 'Update Post 📤', form = form, legend = 'Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required # only accept the POST coz we would accept when submitted from the modal
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('The post has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page ,per_page = 5)    
    return render_template('user_posts.html', posts=posts, user=user)

# # used for passing a token via email
# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request', 
#                   sender='noreply@demo.com', 
#                   recipients=[user.email])
#     # ^ creating our email
#     # 1st arg -> subject line
#     # 2nd -> sender (HAS TO BE FROM OUR DOMAIN OR OUR EMAIL ADDRESS)
#     # 3rd -> recepients

#     # the main body of our email
#     msg.body = f'''For resetting your password, visit the following link:
# {url_for('reset_token', token=token, _external=True)}

# If there were no intentions of changing your password, you can ignore the message and not changed would be applied.
# '''
# # ^ _external=True -> for getting abs urls not relative
#     mail.send(msg)
#     return "Good"


# confirm that we are the existing user by sending our email
# @app.route('/reset_password', methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('Consider looking at your email to continue further!', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title = 'Reset Password', form=form)

# Resetting the password by sending a token to users' emails'
# The token in the email is a link so that only      
# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('Invalid or expired token was gotten!', 'warning')
#         return redirect(url_for('reset_request'))
#     # form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         flash(f'The password has been updated!', 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', title = 'Reset Password', form=form)





