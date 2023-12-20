import time
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

from apps.organization.models import Organization
from apps.shared_revenue.services.split_export import SplitExportService
from apps.shared_revenue.tasks import send_email_to_organization


class Command(BaseCommand):
    """
    This command triggers the export of all the transactions splitted based on the given parameters per organization.

    Required parameters:
        - start_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD
        - send_file: true / false

    How to use:

        python manage.py export_split_revenue_per_organizations  {start_date} {end_date} {send_file}

        Exemple:

            python manage.py export_split_revenue_per_organizations 2023-12-01 2024-01-01 true
    """

    help = "Based on the given informations, this command will generate a xlsx file with the split configurations per organization"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("start_date", type=str)
        parser.add_argument("end_date", type=str)
        parser.add_argument("send_file", type=str)

    def handle(self, *args, **options) -> str | None:
        try:
            start = time.time()
            self.stdout.write("\nStarting file export...\n")
            start_date = datetime.strptime(options["start_date"], "%Y-%m-%d").isoformat()
            send_file: str = options.get("send_file", "false")
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

                # TODO: insert the list of organization emails in the for
                if file_name and send_file.upper() == "TRUE":
                    for email in [organization.email]:
                        try:
                            sender = getattr(settings, "EMAIL_SENDER")
                            file_path_link = getattr(settings, "FILE_PATH_LINK")
                            send_email_to_organization(
                                sender=sender, receiver=email, content=f"{file_path_link}{file_name}"
                            )
                        except Exception as e:
                            raise e

            finish = time.time() - start
            self.stdout.write("\n-----FILE GENERATION EXECUTED SUCCESSFULLY-----\n")
            self.stdout.write(f"\nThe time to the file export was {finish}\n")
        except Exception as e:
            raise CommandError(f"\n-----AN ERROR HAS BEEN RAISED RUNNING THE FILE EXPORT: {e}")
