import random
import smtplib
from datetime import datetime
from celery import Celery
from main import app, db, Birthdays
from twilio.rest import Client
import os
celery = Celery('tasks', broker=os.environ.get('R_KEY'))

messages = ["Happy Birthday!\nAll the best for the year!\n", "Happy birthday! Have a wonderful time today and eat "
                                                             "lots of cake!\nLots of love,\n", "It's your birthday! "
                                                                                               "Have a great "
                                                                                               "day!\nAll my love,\n"]


@celery.task
def send_email_task():
    with app.app_context():
        print('Will start checking for birthdays')
        records = db.session.execute(db.select(Birthdays))
        birthdays = records.scalars().all()
        for birthday in birthdays:
            if (birthday.date.split('-')[1] + '-' + birthday.date.split('-')[2]) == datetime.today().strftime('%m-%d'):
                recipient_name = birthday.name
                recipient_email = birthday.email
                wisher_name = birthday.author.name
                wisher_email = birthday.author.email
                message = messages[random.randint(0, 2)]
                email = os.environ.get('E_ID')
                password = os.environ.get('P_KEY')
                try:
                    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                        connection.starttls()
                        connection.login(user=email, password=password)
                        connection.sendmail(from_addr=email,
                                            to_addrs=recipient_email,
                                            msg=f"Subject: Happy Birthday!\n\nHey {recipient_name},\n{message}{wisher_name}."
                                            )
                        connection.sendmail(from_addr=email,
                                            to_addrs=wisher_email,
                                            msg=f"Subject: Birthday Wish Sent.\n\nHey {wisher_name},\nA birthday wish "
                                                f"has been sent to your friend: {recipient_name}, @ {recipient_email}\nThe"
                                                f" Birthday Wisher.")
                        connection.close()
                    print('Messages Sent!')
                except Exception as e:
                    print(f"An error occurred: {e}")
                    message = f"Troubleshoot The Birthday Wisher.\nThe error message:\n{e}"
                    try:
                        client = Client(os.environ.get('A_ID'), os.environ.get('A_T'))
                        client.messages.create(
                            body=message,
                            from_=os.environ.get('S_ID'),
                            to=os.environ.get('T_ID')
                        )
                    except Exception as e:
                        print(f"Error sending text message: {e}")
