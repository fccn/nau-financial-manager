from typing import Dict

import xlsxwriter


class XlsxGenerator:
    """
    This class is a based package class, an package abstraction

    At the moment it is using xlsxwriter package to work, but if it's necessary to change the package
    just implement the new package business logic in generate_xlsx method, mantaining the basic parameters to work
    and it will not affect any part of the system

    """

    def generate_xlsx(
        self,
        file_name: str,
        columns: list[str],
        values: list[Dict],
    ):
        workbook = xlsxwriter.Workbook(file_name)
        work_sheet = workbook.add_worksheet()

        for column in columns:
            work_sheet.set_column(column, width=len(column))

        row = 0
        for value in values:
            for column in columns:
                work_sheet.write(value[column], row=row, col=column)
            row = +1

        workbook.close()


class PdfGenerator:
    def generate_pdf(self, data):
        """
        Implement here the business logic to generate PDF files
        """
        pass


class CsvGenerator:
    def generate_csv(self, data):
        """
        Implement here the business logic to generate CSV files
        """
        pass


class FileGenerator(XlsxGenerator, PdfGenerator, CsvGenerator):

    """
    This class implements the files generators

    It is injected through the system in all file generator features and applies the dependency inversion, it aways calls
    the super() in each method to work with its business logic, and the system does not know the super(), each means that,
    the system will never depends on the implementations, just depends on this class

    """

    def generate_xlsx(
        self,
        file_name: str,
        columns: list[str],
        values: list[Dict],
    ):
        try:
            super().generate_xlsx(
                self,
                file_name=file_name,
                columns=columns,
                values=values,
            )
        except Exception as e:
            raise e

    def generate_pdf(self, file_name: str, data):
        try:
            super().generate_pdf(file_name=file_name, data=data)
        except Exception as e:
            raise e

    def generate_csv(self, file_name: str, data):
        try:
            super().generate_csv(file_name=file_name, data=data)
        except Exception as e:
            raise e
