from datetime import datetime
from typing import Dict, List

from django.db.models import Q

from apps.billing.models import Transaction, TransactionItem
from apps.organization.models import Organization
from apps.shared_revenue.models import RevenueConfiguration
from apps.shared_revenue.serializers import RevenueConfigurationSerializer


class SplitExecutionService:
    """
    This is the class whose executes the split revenue based on the `start_date` and `end_date` parameters.
    """

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
        """
        Filter the transactions based on the `start_date` and `end_date` parameters.

        The kwargs might also contains filters, `organization_code` and `product_id`
        are optional filters for this function.
        """

        try:
            transactions = Transaction.objects.filter(transaction_date__range=[self.start_date, self.end_date])
            transaction_items: list[TransactionItem] = []
            for transaction in transactions:
                items = transaction.transaction_items.all()
                if items:
                    transaction_items.append(items[0])

            return transaction_items
        except Exception as e:
            raise e

    def _filter_revenue_configurations(self, **kwargs) -> list[RevenueConfiguration]:
        """
        Filter the revenue configurations based on the `start_date` and `end_date` parameters.

        The kwargs might also contains filters, `organization_code` and `product_id`
        are optional filters for this function.
        """

        try:
            configurations = RevenueConfiguration.objects.filter(
                Q(start_date__isnull=True)
                | Q(end_date__isnull=True)
                | Q(start_date__lte=self.end_date) & Q(end_date__gte=self.start_date)
            )
            if kwargs:
                new_kwargs = kwargs
                if "organization_code" in new_kwargs.keys():
                    organization = Organization.objects.filter(short_name=new_kwargs["organization_code"]).first()
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
        """
        This function makes the assembly of each result that makes sense in the revenue configuration split.

        Based on the business logic register returned from here, needs to represent the expeceted
        relevant information of each split result.

        Args:
            item (TransactionItem): The transaction item is the parameter whose has the relevant information about the transaction
            configuration (RevenueConfiguration): The configuration available to be calculated for each transaction.

        Returns:
            dict: The split revenue result.
        """

        return {
            "transaction_id": item.transaction.transaction_id,
            "transaction_date": item.transaction.transaction_date.isoformat(),
            "product_name": item.description,
            "product_id": item.product_id,
            "organization": item.organization_code,
            "total_amount_including_vat": item.transaction.total_amount_include_vat,
            "total_amount_exclude_vat": item.transaction.total_amount_exclude_vat,
            "percentage_for_organization": configuration.partner_percentage,
            "amount_for_organization_including_vat": (item.unit_price_incl_vat * configuration.partner_percentage)
            * item.quantity,
            "amount_for_organization_exclude_vat": (item.unit_price_excl_vat * configuration.partner_percentage)
            * item.quantity,
            "percentage_for_nau": configuration.nau_percentage,
            "amount_for_nau_including_vat": (item.unit_price_incl_vat * configuration.nau_percentage) * item.quantity,
            "amount_for_nau_exclude_vat": (item.unit_price_excl_vat * configuration.nau_percentage) * item.quantity,
        }

    def _calculate_nau_percentage(self, product_id: str):
        try:
            percentage = 1

            configurations: list[RevenueConfiguration] = RevenueConfiguration.objects.filter(product_id=product_id)
            for configuration in configurations:
                percentage = percentage - configuration.partner_percentage

            return percentage
        except Exception as e:
            raise e

    def _calculate_transactions(
        self,
        transaction_items: list[TransactionItem],
        configurations: list[RevenueConfiguration],
    ) -> tuple[list[Dict], list[Dict]]:
        """
        Execute the calculation step of each transaction and revenue configuration.

        Args:
            transaction_items (list[TransactionItem]): The filtered list of transactions items
            configurations (list[RevenueConfiguration]): The filtered list of configurations

        Returns:
            tuple[list[Dict], list[Dict]]: The results is a tuple of two lists, the first one is a list of calculated transactions,
            the second, a list of used `RevenueConfiguration` for calculate each transaction.
        """

        nau_percentage_per_product: dict = {}
        split_results: list[Dict] = []
        used_configurations: list[Dict] = []

        for item in transaction_items:
            for configuration in configurations:
                if item.organization_code == configuration.organization.short_name:
                    if None not in [configuration.start_date, configuration.end_date]:
                        if not configuration.start_date <= item.transaction.transaction_date <= configuration.end_date:
                            continue

                    if item.product_id not in nau_percentage_per_product:
                        nau_percentage = self._calculate_nau_percentage(product_id=item.product_id)
                        nau_percentage_per_product[item.product_id] = nau_percentage

                    configuration.nau_percentage = nau_percentage_per_product[item.product_id]
                    result = self._assembly_each_result(item=item, configuration=configuration)
                    split_results.append(result)

                    configuration_data: dict = dict(RevenueConfigurationSerializer(configuration).data)
                    configuration_data["organization"] = configuration_data["organization"]["short_name"]
                    if configuration_data not in used_configurations:
                        used_configurations.append(configuration_data)

        return split_results, used_configurations

    def execute_split_steps(self, **kwargs) -> list[List[Dict]]:
        """
        Start the split steps executions

        Returns:
            list[List[Dict]]: All the calculated split results and their used configurations
        """
        try:
            configurations: list[RevenueConfiguration] = self._filter_revenue_configurations(**kwargs)
            transaction_items: list[TransactionItem] = self._filter_transaction_items(**kwargs)
            split_results, used_configurations = self._calculate_transactions(
                transaction_items=transaction_items,
                configurations=configurations,
            )

            return [split_results, used_configurations]
        except Exception as e:
            raise e
