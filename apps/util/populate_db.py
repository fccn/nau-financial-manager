import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()

from apps.organization.factories import OrganizationAddressFactory, OrganizationContactFactory, OrganizationFactory
from apps.shared_revenue.factories import RevenueConfigurationFactory, ShareExecutionFactory
from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.shared_revenue.serializers import RevenueConfigurationSerializer
from django.utils import timezone

def generate_revenue_configuration(
    organization,
) -> RevenueConfigurationFactory:
    """
    Generates and populates RevenueConfiguration model.
    """
    
    revenue_configuration = RevenueConfigurationFactory.create(
            organization=organization,
            partner_percentage=0.70
        )
    
    return revenue_configuration
    

def populate_shared_revenue(organization) -> None:
    """
    
    Starts populate of shared_revenue module, creates RevenueConfiguration and ShareExecution
    """    
    
    revenue_configuration = generate_revenue_configuration(
        organization,
    )
    revenue_configuration_json = RevenueConfigurationSerializer(revenue_configuration).data
    ShareExecutionFactory.create(
        percentage=70.0,
        revenue_configuration=revenue_configuration_json,
    )


def populate_billing(organization) -> None:
    """
    Populates billing module, creates five transactions per organization and one TransactionItem per Transaction
    """  

    amount_of_transactions = 5
    transactions = TransactionFactory.create_batch(amount_of_transactions)
    for transaction in transactions:
        TransactionItemFactory.create(transaction=transaction)


def populate():
    """
    Starts the populate feature, creates five organizations
    """  
    
    try:
        organizations_amount = 5
        organizations = OrganizationFactory.create_batch(organizations_amount)
        for organization in organizations:
            OrganizationContactFactory.create(organization=organization)
            OrganizationAddressFactory.create(organization=organization)
            populate_shared_revenue(organization=organization)
            populate_billing(organization=organization)
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
