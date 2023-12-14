from datetime import datetime
from typing import Dict, List

from django.utils.timezone import get_current_timezone

from apps.util.file_generator import FileGenerator

from .split_execution import SplitExecutionService


class SplitExportService:
    def _generate_file_name(
        self,
        optional: dict,
    ) -> str:
        """
        Generates the file name based on the given informations to execute the split revenue.

        Args:
            optional (dict): The optional parameters might be `organization_code` and `product_id`

        Returns:
            str:  The file name
        """

        optinal_parameters = "_"
        for key in ["organization_code", "product_id"]:
            if key in optional:
                optinal_parameters = f"{optinal_parameters}{optional[key].replace(' ', '-')}_"

        now = datetime.now(tz=get_current_timezone()).strftime("%Y%m%d%H%M%S")
        prefix = "report_split_revenue"
        file_name = f"{prefix}{optinal_parameters}{now}"

        return file_name

    def export_split_to_xlsx(
        self,
        start_date: datetime,
        end_date: datetime,
        **kwargs,
    ) -> None:
        """
        Exports as xlsx format the calculated split revenue based on the given parameters.

        Args:
            start_date (datetime): The start date of the range of dates that needs to be calculated
            end_date (datetime): The end date of the range of dates that needs to be calculated
        """

        try:
            split_sheets: list[List[Dict]] = SplitExecutionService(
                start_date=start_date,
                end_date=end_date,
            ).execute_split_steps(**kwargs)
            if not len(split_sheets[0]) == 0:
                file_name: str = self._generate_file_name(optional=kwargs)
                FileGenerator().generate_xlsx(file_name=file_name, sheets=split_sheets)
            else:
                print(
                    f"\nNo data available to generate file using the parameters:\nstart_date: {start_date}\nend_date: {end_date}\noptions: {kwargs}"
                )
        except Exception as e:
            raise e
