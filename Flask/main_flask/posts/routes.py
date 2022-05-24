from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from main_flask import db
from main_flask.models import Post
from main_flask.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('The post has been shared successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', 
    title = 'New Post', form = form, legend = 'New Post')

@posts.route('/post/<int:post_id>')
# putting a variable into ^ the url
# we have said that we expect that to be an int
def post(post_id):
    post = Post.query.get_or_404(post_id)
    # ^ gives the post page but if that doesn't exist, then give me 404
    return render_template("post.html", title = 'Post ⚙', post = post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        # aborting an HTTP response for the forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('create_post.html', 
        title = 'Update Post 📤', form = form, legend = 'Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required # only accept the POST coz we would accept when submitted from the modal
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('The post has been deleted', 'success')
    return redirect(url_for('main.home'))
