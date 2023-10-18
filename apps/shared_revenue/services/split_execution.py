from datetime import datetime
from typing import Dict

from apps.billing.models import ReceiptItem
from apps.shared_revenue.models import RevenueConfiguration


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

    def _fetch_all_transaction_items(self, **kwargs) -> list[ReceiptItem]:
        try:
            transction_items = ReceiptItem.objects.filter(**kwargs).all()
            return transction_items
        except Exception as e:
            raise e

    def _fetch_all_revenue_configurations(self, **kwargs) -> list[RevenueConfiguration]:
        try:
            configurations = RevenueConfiguration.objects.filter(**kwargs).all()
            return configurations
        except Exception as e:
            raise e

    def _assembly_each_result(
        self,
        item: ReceiptItem,
        configuration: RevenueConfiguration,
    ) -> dict:
        return {
            "product_name": item.description,
            "transaction_date": item.receipt.transaction_date,
            "total_amount_include_vat": item.receipt.total_amount_include_vat,
            "total_amount_exclude_vat": item.receipt.total_amount_exclude_vat,
            "organization": configuration.organization,
            "amount_for_organization": item.receipt.total_amount_exclude_vat * configuration.partner_percentage,
        }

    def _calculate_transactions(
        self,
        transaction_items: list[ReceiptItem],
        configurations: list[RevenueConfiguration],
    ) -> list[Dict]:
        split_results: list[Dict] = {}

        for item in transaction_items:
            for configuration in configurations:
                result = self._assembly_each_result(item=item, configuration=configuration)
                split_results.append(result)

        return split_results

    def execute_split_steps(self, **kwargs) -> dict:
        try:
            transaction_items: list[ReceiptItem] = self._fetch_all_transaction_items(**kwargs)
            configurations: list[RevenueConfiguration] = self._fetch_all_revenue_configurations(**kwargs)
            split_results = self._calculate_transactions(
                transaction_items=transaction_items,
                configurations=configurations,
            )

            return split_results
        except Exception as e:
            raise e