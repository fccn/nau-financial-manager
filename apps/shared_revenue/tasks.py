from celery import shared_task

from apps.util.email_sender import EmailSender


@shared_task(name="apps.shared_revenue.tasks.send_email_to_organization")
def send_email_to_organization(
    sender: str,
    subject: str,
    recipient_list: str,
    content: str,
):
    try:
        EmailSender.send_email(
            sender=sender,
            subject=subject,
            recipient_list=recipient_list,
            content=content,
        )
    except Exception as e:
        raise e
