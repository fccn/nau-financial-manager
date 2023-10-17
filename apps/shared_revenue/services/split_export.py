from apps.util.file_generator import FileGenerator


class SplitExportService:
    @staticmethod
    def export_split_to_xlsx(data: dict):
        try:
            file = FileGenerator.generate_xlsx(data=data)
            return file
        except Exception as e:
            raise e
