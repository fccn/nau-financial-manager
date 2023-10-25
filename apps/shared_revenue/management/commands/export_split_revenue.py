from datetime import datetime

from django.core.management.base import BaseCommand, CommandError, CommandParser

from apps.shared_revenue.services.split_export import SplitExportService


class Command(BaseCommand):

    help = "Based on the given informations, this command will generate a xlsx file with the split configurations"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("start_date", type=str)
        parser.add_argument("end_date", type=str)
        parser.add_argument("--product_id", dest="product_id", type=str)
        parser.add_argument("--organization_code", dest="organization_code", type=str)

    def _convert_date(self, date: str) -> datetime:
        splitted_date = [int(parameter) for parameter in date.split("/")]
        return datetime(splitted_date[2], splitted_date[1], splitted_date[0])

    def handle(self, *args, **options) -> str | None:
        try:
            start_date = self._convert_date(options["start_date"])
            end_date = self._convert_date(options["end_date"])
            product_id = options.get("product_id")
            organization_code = options.get("organization_code")
            kwargs = {
                k: v
                for k, v in {"product_id": product_id, "organization_code": organization_code}.items()
                if v not in ["", None]
            }
            SplitExportService().export_split_to_xlsx(
                start_date=start_date,
                end_date=end_date,
                **kwargs,
            )
            self.stdout.write("\n-----GENERATED FILE-----\n")
        except Exception as e:
            raise CommandError(f"{e}")
