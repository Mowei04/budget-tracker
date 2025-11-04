import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "change-me"  # 用于CSRF
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True