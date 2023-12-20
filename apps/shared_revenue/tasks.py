import logging
from datetime import datetime

from celery import shared_task

from apps.util.email_sender import EmailSender


@shared_task(name="apps.shared_revenue.tasks.send_email_to_organization")
def send_email_to_organization(sender: str, receiver: str, content: str):
    try:
        EmailSender.send_email(sender=sender, receiver=receiver, content=content)
    except Exception as e:
        now = datetime.now()
        logging.getLogger("nau_financial_manager").error(
            f"time: {now}, error: email not sent, sender: {sender}, receiver: {receiver}, content: {content}"
        )
        raise e
