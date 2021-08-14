from flask import Blueprint, render_template

errors = Blueprint('blueprints', __name__)


@errors.app_errorhandler(404)
def error_404(error):

    
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):

    
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):

    
    return render_template('errors/500.html'), 500
    # in the flask, we can return that status code (def: 200)
    # ^ used for getting the correct error code response

