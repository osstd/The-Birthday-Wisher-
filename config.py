import os


class Config:
    SECRET_KEY = os.environ.get('F_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", "sqlite:///posts.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # RECAPTCHA_SECRET_KEY = os.environ.get("G_KEY")
    # EMAIL_HOST = "smtp.gmail.com"
    # EMAIL_PORT = 587
    # RECAPTCHA_SITE_KEY = os.environ.get("S_KEY")
