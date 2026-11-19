import logging
import secrets
import string
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
        choices = string.ascii_letters + string.digits
        hash_code = "".join(secrets.choice(choices) for i in range(10))
        file_name = f"report_split_revenue{optinal_parameters}{now}_{hash_code}"

        return file_name

    def export_split_to_xlsx(
        self,
        start_date: datetime,
        end_date: datetime,
        **kwargs,
    ):
        """
        Exports as xlsx format the calculated split revenue based on the given parameters.

        Args:
            start_date (datetime): The start date of the range of dates that needs to be calculated
            end_date (datetime): The end date of the range of dates that needs to be calculated
        """
        split_sheets: list[List[Dict]] = SplitExecutionService(
            start_date=start_date,
            end_date=end_date,
        ).execute_split_steps(**kwargs)
        if not len(split_sheets[0]) == 0:
            file_name: str = self._generate_file_name(optional=kwargs)
            FileGenerator().generate_xlsx(file_name=file_name, sheets=split_sheets)

            return file_name

        logging.getLogger("nau_financial_manager").warning(
            f"No data available to generate file using the parameters: start_date: {start_date}, end_date: {end_date}, options: {kwargs}"
        )

    def export_split_to_xlsx_content(
        self,
        start_date: datetime,
        end_date: datetime,
        **kwargs,
    ) -> tuple[str, bytes] | None:
        """
        Calculates the split revenue based on the given parameters and returns it as a xlsx file content,
        without saving the file in the storage. It is meant to be delivered directly, as a download.

        Args:
            start_date (datetime): The start date of the range of dates that needs to be calculated
            end_date (datetime): The end date of the range of dates that needs to be calculated

        Returns:
            tuple[str, bytes] | None: The file name, with its extension, and the file content.
            None if there is no data for the given parameters.
        """
        split_sheets: list[List[Dict]] = SplitExecutionService(
            start_date=start_date,
            end_date=end_date,
        ).execute_split_steps(**kwargs)
        if len(split_sheets[0]) == 0:
            return None

        file_name: str = self._generate_file_name(optional=kwargs)
        content: bytes = FileGenerator().generate_xlsx_content(sheets=split_sheets)

        return f"{file_name}.xlsx", content
