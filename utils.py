# from flask import current_app
# from twilio.rest import Client
# import aiosmtplib
# import requests
import html
import re


def sanitize_input(input_text):
    return html.escape(input_text.strip())


def validate_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email) is not None
