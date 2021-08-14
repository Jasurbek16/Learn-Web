import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
# ^ .config -- the configuration dictionary
# ^ could be set as an env var
# ^ The secret key is needed to keep the client-side sessions secure. You can generate some random key
# ^ # ! we need to put a secret key for our application --> protects modifying cookies, avoid forgery attacks
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
# /// are relative paths from the current file via sqlite

    MAIL_PORT = 587
    # port that email is sent thru on our server
    MAIL_USE_TLS = True
    # ^ for encryption purposes
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
