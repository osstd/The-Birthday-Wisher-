from datetime import date
from celery import Celery
from app import app
from sqlalchemy import extract
from models.models import Birthdays
from utils import get_birthday_message, send_email_async, send_text
from email.mime.text import MIMEText
import os
import asyncio

celery = Celery('tasks', broker=os.environ.get('R_KEY'))


@celery.task
def send_email_task():
    with app.app_context():
        print('Will start checking for birthdays')

        today = date.today()
        birthdays = Birthdays.query.filter(
            extract('month', Birthdays.date) == today.month,
            extract('day', Birthdays.date) == today.day
        ).all()

        for birthday in birthdays:
            try:
                send_birthday_email(birthday)
                send_notification_email(birthday)
                print('Messages Sent!')

            except Exception as e:
                print(f"An error occurred: {e}")
                try:
                    message = f"Troubleshoot The Birthday Wisher.\nThe error message:\n{e}"
                    asyncio.run(send_text(message))

                except Exception as e:
                    print(f"Error sending text message: {e}")


def send_birthday_email(birthday):
    recipient_name = birthday.name
    recipient_email = birthday.email
    wisher_name = birthday.author.name

    message = get_birthday_message()

    subject = "Happy Birthday!"
    body = f"Hey {recipient_name},\n{message}{wisher_name}."
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject

    asyncio.run(send_email_async(message=msg, recepient_email=recipient_email))


def send_notification_email(birthday):
    wisher_email = birthday.author.email
    recipient_name = birthday.name
    recipient_email = birthday.email

    subject = "Birthday Wish Sent."
    body = f"A birthday wish has been sent to your friend: {recipient_name}, @ {recipient_email}\nThe Birthday Wisher."

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject

    asyncio.run(send_email_async(message=msg, recepient_email=wisher_email))
