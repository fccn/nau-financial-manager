from datetime import datetime

from apps.util.file_generator import FileGenerator

from .split_execution import SplitExecutionService


class SplitExportService:
    @staticmethod
    def export_split_to_xlsx(start_date: datetime, end_date: datetime, **kwargs) -> None:
        try:
            split_result = SplitExecutionService(
                start_date=start_date,
                end_date=end_date,
            ).execute_split_steps(**kwargs)

            FileGenerator().generate_xlsx(
                file_name=split_result.file_name,
                columns=split_result.columns,
                values=split_result.results,
            )
        except Exception as e:
            raise e
