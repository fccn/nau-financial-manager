from datetime import datetime
from typing import Dict

from apps.billing.models import TransactionItem
from apps.shared_revenue.models import RevenueConfiguration


class SplitResult:
    def __init__(
        self,
        columns,
        results,
        file_name,
    ) -> None:
        self.file_name = file_name
        self.results = results
        self.columns = columns

    file_name: str = None
    columns: list[str] = None
    values: list[Dict] = None


class SplitExecutionService:
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        self.start_date = start_date
        self.end_date = end_date

    start_date: datetime
    end_date: datetime

    def _filter_transaction_items(self, **kwargs) -> list[TransactionItem]:
        try:
            if kwargs:
                transction_items = TransactionItem.objects.filter(**kwargs)
                return transction_items

            transction_items = TransactionItem.objects.all()
            return transction_items
        except Exception as e:
            raise e

    def _filter_revenue_configurations(self, **kwargs) -> list[RevenueConfiguration]:
        try:
            if kwargs:
                configurations = RevenueConfiguration.objects.filter(**kwargs)
                return configurations

            configurations = RevenueConfiguration.objects.all()
            return configurations
        except Exception as e:
            raise e

    def _assembly_each_result(
        self,
        item: TransactionItem,
        configuration: RevenueConfiguration,
    ) -> dict:
        return {
            "product_name": item.description,
            "transaction_date": item.transaction.transaction_date,
            "total_amount_include_vat": item.transaction.total_amount_include_vat,
            "total_amount_exclude_vat": item.transaction.total_amount_exclude_vat,
            "organization_code": configuration.organization,
            "amount_for_organization": item.transaction.total_amount_exclude_vat * configuration.partner_percentage,
        }

    def _calculate_transactions(
        self,
        transaction_items: list[TransactionItem],
        configurations: list[RevenueConfiguration],
    ) -> list[Dict]:
        split_results: list[Dict] = {}

        for item in transaction_items:
            for configuration in configurations:
                result = self._assembly_each_result(item=item, configuration=configuration)
                split_results.append(result)
        return split_results

    def execute_split_steps(self, **kwargs) -> SplitResult:
        try:
            transaction_items: list[TransactionItem] = self._filter_transaction_items(**kwargs)
            configurations: list[RevenueConfiguration] = self._filter_revenue_configurations(**kwargs)
            split_results = self._calculate_transactions(
                transaction_items=transaction_items,
                configurations=configurations,
            )

            split_result = SplitResult(
                file_name="teste",
                results=split_results,
                columns=[
                    "product_name",
                    "transaction_date",
                    "total_amount_include_vat",
                    "total_amount_exclude_vat",
                    "organization_code",
                    "amount_for_organization",
                ],
            )
            return split_result
        except Exception as e:
            raise e
