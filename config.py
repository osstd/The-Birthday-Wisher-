import os


class Config:
    SECRET_KEY = os.environ.get('F_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", os.getenv('DATABASE_URL'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USERNAME = os.environ.get("E_ID")
    EMAIL_PASSWORD = os.environ.get("P_KEY")
    TWILIO_ACCOUNT_SID = os.environ.get('A_ID')
    TWILIO_AUTH_TOKEN = os.environ.get('A_T')
    TWILIO_PHONE_NUMBER = os.environ.get('S_ID')
    RECIPIENT_PHONE_NUMBER = os.environ.get('T_ID')
