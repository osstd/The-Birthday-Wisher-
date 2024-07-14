from datetime import date
from celery import Celery
from app import app
from sqlalchemy import extract
from models.models import Birthdays
from utils import get_birthday_message, send_email_async, send_text
from email.mime.text import MIMEText
import logging
import os
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery = Celery('tasks', broker=os.environ.get('R_KEY'))


@celery.task
def send_email_task():
    with app.app_context():
        logger.info('Will start checking for birthdays')

        today = date.today()
        birthdays = Birthdays.query.filter(
            extract('month', Birthdays.date) == today.month,
            extract('day', Birthdays.date) == today.day
        ).all()

        for birthday in birthdays:
            try:
                send_birthday_email(birthday)
                send_notification_email(birthday)
                logger.info('Messages Sent!')

            except Exception as e:
                logger.error(f"An error occurred: {e}")
                try:
                    message = f"Troubleshoot The Birthday Wisher.\nThe error message:\n{e}"
                    asyncio.run(send_text(message))

                except Exception as e:
                    logger.error(f"Error sending text message: {e}")


def send_birthday_email(birthday):
    message = get_birthday_message()

    subject = "Happy Birthday!"
    body = f"Hey {birthday.name},\n{message}{birthday.author.name}."
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject

    asyncio.run(send_email_async(message=msg, recepient_email=birthday.email))


def send_notification_email(birthday):
    subject = "Birthday Wish Sent."
    body = f"Hey {birthday.author.name}, \nA birthday wish has been sent to your friend: {birthday.name}, @ {birthday.email}\nThe Birthday Wisher."

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject

    asyncio.run(send_email_async(message=msg, recepient_email=birthday.author.email))
