from flask import current_app
from twilio.rest import Client
from datetime import date, datetime
import aiosmtplib
import html
import re
import random


def sanitize_input(input_text):
    return html.escape(input_text.strip())


def validate_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email) is not None


def validate_date(date_str):
    try:
        birthday_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = date.today()

        if birthday_date > today:
            return False, "Birthday can't be in the future."
        if birthday_date.year < 1900:
            return False, "Birthday year must be 1900 or later."
        return True, ""
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."


def get_birthday_message():
    messages = ["Happy Birthday!\nAll the best for the year!\n", "Happy birthday! Have a wonderful time today and eat "
                                                                 "lots of cake!\nLots of love,\n",
                "It's your birthday! "
                "Have a great "
                "day!\nAll my love,\n"]
    return messages[random.randint(0, 2)]


async def send_email_async(message, recepient_email):
    email_username = current_app.config['EMAIL_USERNAME']
    if not recepient_email:
        recepient_email = email_username
    message["From"] = email_username
    message["To"] = recepient_email

    try:
        await aiosmtplib.send(
            message,
            hostname=current_app.config['EMAIL_HOST'],
            port=current_app.config['EMAIL_PORT'],
            start_tls=True,
            username=email_username,
            password=current_app.config['EMAIL_PASSWORD'])
        return True
    except Exception as error:
        print(f"Error sending email to {recepient_email}: {str(error)}")
        return False


async def send_text(message):
    client = Client(current_app.config['TWILIO_ACCOUNT_SID'], current_app.config['TWILIO_AUTH_TOKEN'])
    message = client.messages.create(
        body=message,
        from_=current_app.config['TWILIO_PHONE_NUMBER'],
        to=current_app.config['RECIPIENT_PHONE_NUMBER']
    )
    print(message.status)
