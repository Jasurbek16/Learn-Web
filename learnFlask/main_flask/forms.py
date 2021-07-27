from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# make sure that the field is not empty ^
# specifying the range of chars to be used in the input -> Length
# wtforms is used for working with forms in flask
from main_flask.models import User


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    #                         ^ the name of this field
    # would also be used as the label in our html
    # validations can be put using validators (as 2nd argument)
    # a list of what we want to be validated
    # validators are also classes that we import
    # we need to put ()s after the DataRequired class
    email = StringField("Email", validators=[
        DataRequired(), Email()])
    #                 ^ a valid email
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirming the Password", validators=[DataRequired(), EqualTo('password')])
    #   the confirm password has to be = to the password                ^
    # the submit button
    submit = SubmitField("Join Us")

    #!!! creating a custom validation
    #!!! def validate_field(self, field):
    #!!!     if True:
    #!!!         raise ValidationError('Validation Message')
    #!!! ^ a template for our validation methods

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        
        if user:
            raise ValidationError('Existing username is passed, please consider another one!')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        
        if user:
            raise ValidationError('Existing email is passed, please consider another one!')


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[
        DataRequired(), Email()])
    #                 ^ a valid email
    password = PasswordField("Password", validators=[DataRequired()])
    # adding the remember field to stay logged in for some time after a browser closes using a secure cookie
    remember = BooleanField("Remember Me")
    # the submit button
    submit = SubmitField("Login")
