from datetime import datetime

from django.core.management.base import BaseCommand, CommandError, CommandParser

from apps.shared_revenue.services.split_export import SplitExportService


class Command(BaseCommand):

    help = "Based on the given informations, this command will generate a xlsx file with the split configurations"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("start_date", type=datetime, nargs="+")
        parser.add_argument("end_date", type=datetime, nargs="+")
        parser.add_argument("organization_code", type=str, nargs="?")
        parser.add_argument("product_id", type=str, nargs="?")

    def handle(self, *args, **options) -> str | None:
        try:
            start_date = options["start_date"]
            end_date = options["end_date"]
            kwargs = {k: v for k, v in options.items() if k not in ["start_date", "end_date"]}
            SplitExportService().export_split_to_xlsx(
                start_date=start_date,
                end_date=end_date,
                **kwargs,
            )
            self.stdout.write("exported")
        except Exception as e:
            raise CommandError(f"{e}")
