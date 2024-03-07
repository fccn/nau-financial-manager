from celery import shared_task

from apps.util.email_helper import EmailHelper
from apps.util.email_sender import EmailSender


@shared_task(name="apps.shared_revenue.tasks.send_email_to_organization")
def send_email_to_organization(email_helper: EmailHelper):
    EmailSender.send_email(email_helper=email_helper)
