import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.factories import RevenueConfigurationFactory
from apps.billing.factories import TransactionFactory, TransactionItemFactory


def populate_shared_revenue(organization, product_ids: list[str]) -> None:
    """
    Populates shared_revenue module, creates RevenueConfiguration
    """    
    
    for product_id in product_ids:
        RevenueConfigurationFactory.create(
            organization=organization,
            product_id=product_id,
            partner_percentage=0.70
        )


def populate_billing(organization) -> list[str]:
    """
    Populates billing module, creates five transactions per organization and one TransactionItem per Transaction
    """  

    amount_of_transactions = 5
    transactions = TransactionFactory.create_batch(amount_of_transactions)
    product_ids = []
    for transaction in transactions:
        item: TransactionItemFactory = TransactionItemFactory.create(
            transaction=transaction,
            organization_code=organization.short_name,
        )
        if not item.product_id in product_ids:
            product_ids.append(item.product_id)
    
    return product_ids


def populate():
    """
    Starts the populate feature, creates five organizations
    """  
    
    try:
        organizations_amount = 5
        organizations = OrganizationFactory.create_batch(organizations_amount)
        for organization in organizations:
            product_ids = populate_billing(organization=organization)
            populate_shared_revenue(
                product_ids=product_ids,
                organization=organization,
            )
    except Exception as e:
        raise e


if __name__ == "__main__":
    """
    Main method, triggers the populate script and calculate the time to do
    """ 
    
    print("Starting population script...")
    start = time.time()
    populate()
    finish = time.time() - start
    print(f"Finished population script in {finish}")
