import logging
from datetime import datetime


class EmailSender:
    @staticmethod
    def send_email(sender: str, receiver: str, content: str):
        try:
            # TODO: insert the send email business logic
            logging.getLogger("nau_financial_manager").info(
                f"info: email sent, time: {datetime.now()}, sender: {sender}, receiver: {receiver}, content: {content}"
            )
        except Exception as e:
            raise e
