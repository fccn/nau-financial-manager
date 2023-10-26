from string import ascii_uppercase
from typing import Dict

import xlsxwriter


class XlsxGenerator:
    """
    This class is a based package class, an package abstraction

    At the moment the system is using XlsxWriter package to work, but if it's necessary to change the package,
    just implement the new package business logic in generate_xlsx method, mantaining the basic parameters to work
    and it will not affect any part of the system

    """

    def _generate_column_letter_position(self, column_position: int):
        """
        This method generates the column position as letters in the way that it's possible to get the column letter position such as 1 (position A)

        Args:
            index_position (int): The column number position

        Returns:
            str: The generated string position based on the column_position converted to 26 base number
        """

        letters = []

        while column_position > 0:
            column_position -= 1
            rest = column_position % len(ascii_uppercase)
            letters.append(ascii_uppercase[rest])
            column_position //= len(ascii_uppercase)

        letters = "".join(letters.__reversed__())

        return letters

    def generate_xlsx(
        self,
        file_name: str,
        columns: list[str],
        values: list[Dict],
    ) -> None:
        """
        This method generates xlsx format files

        Args:
            file_name (str): The file name to be generated
            columns (list[str]): The columns to be created in this file
            values (list[Dict]): The values to be saved in each column
        """

        workbook = xlsxwriter.Workbook(
            f"{file_name}.xlsx",
            options={
                "remove_timezone": True,
                "default_date_format": "dd/mm/yy hh:mm:ss.000",
            },
        )
        work_sheet = workbook.add_worksheet()

        for column in columns:
            column_letter = self._generate_column_letter_position(columns.index(column) + 1)
            work_sheet.set_column(
                f"{column_letter}:{column_letter}",
                width=20,
            )
            bold = workbook.add_format({"bold": True})
            work_sheet.write(f"{column_letter}1", column.replace("_", " "), bold)

            row = 2
            for value in values:
                work_sheet.write(f"{column_letter}{row}", value[column])
                row += 1

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

    pass
