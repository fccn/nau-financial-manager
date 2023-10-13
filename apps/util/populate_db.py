import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()

from apps.organization.factories import OrganizationAddressFactory, OrganizationContactFactory, OrganizationFactory
from apps.shared_revenue.factories import RevenueConfigurationFactory, ShareExecutionFactory
from apps.billing.factories import ReceiptFactory, ReceiptItemFactory
from apps.shared_revenue.serializers import RevenueConfigurationSerializer

import random
import string


def populate_organizations_resources(organization: OrganizationFactory) -> None:
    
    """
    
    Populates organizations resources, address and contacts
    """
    
    OrganizationContactFactory.create(organization=organization)
    OrganizationAddressFactory.create(organization=organization)


def generate_course_code() -> str:
    
    """
    
    Generates a fake course code of length of 10 chars
    """
    
    letters = f"{string.ascii_uppercase}1234567890" 
    code = "".join(["".join(random.choices(letters)) for i in range(10)])
    return code


def generate_revenue_configuration(
    organization: OrganizationFactory
) -> RevenueConfigurationFactory:
    
    """
    
    Generates and populates RevenueConfiguration model
    """

    if [True, False][random.randint(0, 1)]:
        revenue_configuration: RevenueConfigurationFactory = RevenueConfigurationFactory.create(
            organization=organization
        )
        return revenue_configuration
   
    course_code: str = generate_course_code()
    revenue_configuration: RevenueConfigurationFactory = RevenueConfigurationFactory.create(
        course_code=course_code
    )
    return revenue_configuration
    


def populate_shared_revenue(organization: OrganizationFactory) -> None:

    """
    
    Starts populate of shared_revenue module, creates RevenueConfiguration and ShareExecution
    """    
    
    revenue_configuration = generate_revenue_configuration(
        organization=organization,
    )
    revenue_configuration = RevenueConfigurationSerializer(revenue_configuration).data
    ShareExecutionFactory.create(
        revenue_configuration=revenue_configuration,
    )


def populate_billing(organization: OrganizationFactory) -> None:
    
    """
    
    Populates billing module, creates five receipts per organization and one ReceiptItem per Receipt
    """  

    amount_of_receipts = 5
    receipts: list[ReceiptFactory] = ReceiptFactory.create_batch(amount_of_receipts, organization=organization)
    for receipt in receipts:
        ReceiptItemFactory.create(receipt=receipt)


def populate():
    
    """
    
    Starts the populate feature, creates five organizations
    """  
    
    try:
        organizations_amount: int = 5
        organizations: list[OrganizationFactory] = OrganizationFactory.create_batch(organizations_amount)
        for organization in organizations:
            populate_organizations_resources(organization=organization)
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
