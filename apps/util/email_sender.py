import logging
from datetime import datetime

from django.core.mail import send_mail


class EmailSender:
    """
    This class is the email sender component of the project. The email configurations,
    such as host or backend, are defined in the `settings` file, which is updated using
    the enviroment file.
    """

    @staticmethod
    def send_email(
        sender: str,
        subject: str,
        recipient_list: list,
        content: str,
    ):
        try:
            send_mail(
                subject=subject,
                message=content,
                from_email=sender,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logging.getLogger("nau_financial_manager").info(
                f"info: email sent, time: {datetime.now()}, sender: {sender}, recipient_list: {recipient_list}, content: {content}"
            )
        except Exception as e:
            logging.getLogger("nau_financial_manager").error(
                f"error: email not sent, time: {datetime.now()}, sender: {sender}, recipient_list: {recipient_list}, content: {content}"
            )
            raise e
