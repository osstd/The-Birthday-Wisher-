from datetime import date
from celery import Celery
from app import app
from sqlalchemy import extract
from models.models import Birthdays
from utils import get_birthday_message, send_email_async, send_text, text_unsent
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
                birthday_email = send_birthday_email(birthday)
                notification_email = send_notification_email(birthday)

                if birthday_email and notification_email:
                    logger.info('Messages Sent!')

                if not birthday_email or not notification_email:
                    logger.error('An error occurred, check logs!')

            except Exception as e:
                logger.error(f"An error occurred: {e}")
                try:
                    result = asyncio.run(send_text(f"Troubleshoot The Birthday Wisher.\nThe error message:\n{e}"))

                    if not result['success']:
                        text_unsent(
                            MIMEText(
                                f"An error occurred while sending a text notification:\n{result['error']}.\n Check logs"
                                f".",
                                'plain',
                                'utf-8'))

                    logger.info(f"Text message notification of error is sent: {e}")

                except Exception as e:
                    text_unsent(
                        MIMEText(f"An error occurred while sending a text notification:\n{str(e)}.\n Check logs",
                                 'plain',
                                 'utf-8'))
                    logger.error(f"Error sending text message to notify of error: {e}")

                return


def send_birthday_email(birthday):
    message = get_birthday_message()

    subject = "Happy Birthday!"
    body = f"Hey {birthday.name},\n{message}{birthday.author.name}."
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject

    return asyncio.run(send_email_async(message=msg, recepient_email=birthday.email))


def send_notification_email(birthday):
    subject = "Birthday Wish Sent."
    body = f"Hey {birthday.author.name}, \nA birthday wish has been sent to your friend: {birthday.name}, @ " \
           f"{birthday.email}\nThe Birthday Wisher."

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject

    return asyncio.run(send_email_async(message=msg, recepient_email=birthday.author.email))
