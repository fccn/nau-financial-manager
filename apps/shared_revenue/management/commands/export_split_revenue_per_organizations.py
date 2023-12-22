import time
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.template.loader import render_to_string

from apps.organization.models import Organization
from apps.shared_revenue.services.split_export import SplitExportService
from apps.shared_revenue.tasks import send_email_to_organization
from apps.util.email_helper import EmailHelper


class Command(BaseCommand):
    """
    This command triggers the export of all the transactions splitted based on the given parameters per organization.

    Required parameters:
        - start_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD
        - send_email: true / false

    Optional parameters:
        - bcc: email@email.com

    How to use:
        To add more than one email as bcc, just repeat the parameter `--bcc`.

        python manage.py export_split_revenue_per_organizations  {start_date} {end_date} --send_email={send_email} --bcc={bcc1} --bcc={bcc2}

        Exemple:

            python manage.py export_split_revenue_per_organizations 2023-12-01 2024-01-01 --send_email=true --bcc=bcc1@email.com --bcc=bcc2@email.com
    """

    help = "Based on the given informations, this command will generate a xlsx file with the split configurations per organization"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("start_date", type=str)
        parser.add_argument("end_date", type=str)
        parser.add_argument("--send_email", dest="send_email", type=str, required=True)
        parser.add_argument("--bcc", dest="bcc", action="append", default=[])

    def handle(self, *args, **options) -> str | None:
        try:
            start = time.time()
            self.stdout.write("\nStarting file export...\n")
            start_date = datetime.strptime(options["start_date"], "%Y-%m-%d").isoformat()
            send_email: str = options.get("send_email", "false")
            bcc = options.get("bcc", [])
            end_date = (
                datetime.strptime(options["end_date"], "%Y-%m-%d") + (timedelta(days=1) - timedelta(milliseconds=1))
            ).isoformat()

            for organization in Organization.objects.all():
                kwargs = {"organization_code": organization.short_name}
                file_name = SplitExportService().export_split_to_xlsx(
                    start_date=start_date,
                    end_date=end_date,
                    **kwargs,
                )

                if file_name and send_email.upper() == "TRUE":
                    # TODO: insert the list of organization emails in the for
                    self.__send_email(
                        file_name=file_name,
                        to=[organization.email],
                        bcc=bcc,
                    )

            finish = time.time() - start
            self.stdout.write("\n-----FILE GENERATION EXECUTED SUCCESSFULLY-----\n")
            self.stdout.write(f"\nThe time to the file export was {finish}\n")
        except Exception as e:
            raise CommandError(f"\n-----AN ERROR HAS BEEN RAISED RUNNING THE FILE EXPORT: {e}")

    def __send_email(self, file_name: str, to: list, bcc: list):
        try:
            base_dir = getattr(settings, "BASE_DIR")
            email_sender = getattr(settings, "EMAIL_HOST_USER")
            file_link = getattr(settings, "FILE_PATH_LINK")
            content = render_to_string(
                f"{base_dir}/templates/emails/shared_revenue_export_per_organization.txt",
                {"file_link": f"{file_link}{file_name}"},
            )
            email_helper = EmailHelper(
                from_email=email_sender,
                to=to,
                subject="NAU financial report.",
                body=content,
                bcc=bcc,
            )

            send_email_to_organization(email_helper=email_helper)
        except Exception as e:
            raise e
