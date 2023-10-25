import time
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

    def handle(self, *args, **options) -> str | None:
        try:
            start = time.time()
            self.stdout.write("\nStarting file export...\n")
            start_date = datetime.strptime(options["start_date"], "%d/%m/%Y")
            end_date = datetime.strptime(options["end_date"], "%d/%m/%Y")
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
            finish = time.time() - start
            self.stdout.write("\n-----FILE GENERATED SUCCESSFULLY-----\n")
            self.stdout.write(f"\nThe time to the file export was {finish}\n")
        except Exception as e:
            raise CommandError(f"\n-----AN ERROR HAS BEEN RAISED RUNNING THE FILE EXPORT: {e}")
