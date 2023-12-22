import logging
from datetime import datetime

from django.core.mail.message import EmailMultiAlternatives

from apps.util.email_helper import EmailHelper


class EmailSender:
    """
    This class is the email sender component of the project. The email configurations,
    such as host or backend, are defined in the `settings` file, which is updated using
    the enviroment file.
    """

    @staticmethod
    def send_email(email_helper: EmailHelper):
        try:
            mail = EmailMultiAlternatives(
                subject=email_helper.subject,
                body=email_helper.body,
                from_email=email_helper.from_email,
                to=email_helper.to,
                bcc=email_helper.bcc,
            )
            mail.send()
            logging.getLogger("nau_financial_manager").info(
                f"info: email sent, time: {datetime.now()}, from_email: {email_helper.from_email}, to: {email_helper.to}, body: {email_helper.body}"
            )
        except Exception as e:
            logging.getLogger("nau_financial_manager").error(
                f"error: email not sent, time: {datetime.now()}, from_email: {email_helper.from_email}, to: {email_helper.to}, body: {email_helper.body}"
            )
            raise e
