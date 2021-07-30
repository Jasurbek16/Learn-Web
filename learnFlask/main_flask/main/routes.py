from flask import render_template, request, Blueprint
from main_flask.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")  # two routes are available for the same page
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



@main.route("/about")
def about():
    return render_template('about_temp.html', title='About')
