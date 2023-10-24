from datetime import datetime
from typing import Dict

from django.db.models import Q

from apps.billing.models import Transaction, TransactionItem
from apps.organization.models import Organization
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
            transactions = Transaction.objects.filter(transaction_date__range=[self.start_date, self.end_date])
            transaction_items: list[TransactionItem] = []
            for transaction in transactions:
                kwargs["transaction"] = transaction
                transaction_items += TransactionItem.objects.filter(**kwargs)

            return transaction_items
        except Exception as e:
            raise e

    def _filter_revenue_configurations(self, **kwargs) -> list[RevenueConfiguration]:
        try:
            configurations = RevenueConfiguration.objects.filter(
                Q(start_date__isnull=True) | Q(end_date__isnull=True) | Q(end_date__gte=self.start_date),
            )
            if kwargs:
                new_kwargs = kwargs
                if kwargs["organization_code"]:
                    organization = Organization.objects.filter(short_name=kwargs["organization_code"]).first()
                    del new_kwargs["organization_code"]
                    new_kwargs["organization"] = organization

                configurations = configurations.filter(**new_kwargs)
                return configurations

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
            "organization_code": configuration.organization.short_name,
            "amount_for_nau": item.transaction.total_amount_include_vat * (1 - configuration.partner_percentage),
            "amount_for_organization": item.transaction.total_amount_include_vat * configuration.partner_percentage,
        }

    def _calculate_transactions(
        self,
        transaction_items: list[TransactionItem],
        configurations: list[RevenueConfiguration],
    ) -> list[Dict]:
        split_results: list[Dict] = []

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
                file_name="excel_organizations",
                results=split_results,
                columns=[
                    "product_name",
                    "transaction_date",
                    "total_amount_include_vat",
                    "total_amount_exclude_vat",
                    "organization_code",
                    "amount_for_nau",
                    "amount_for_organization",
                ],
            )

            return split_result
        except Exception as e:
            raise e
