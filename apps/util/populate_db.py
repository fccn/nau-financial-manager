import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()

from apps.organization.factories import OrganizationAddressFactory, OrganizationContactFactory, OrganizationFactory
from apps.shared_revenue.factories import PartnershipLevelFactory, RevenueConfigurationFactory, ShareExecutionFactory
from apps.billing.factories import ReceiptFactory, ReceiptItemFactory
from apps.shared_revenue.serializers import PartnershipLevelSerializer, RevenueConfigurationSerializer

import random

def populate_organizations_resources(organization: OrganizationFactory) -> None:
    OrganizationContactFactory.create(organization=organization)
    OrganizationAddressFactory.create(organization=organization)


def generate_revenue_configuration(
    organization: OrganizationFactory,
    partnership_levels: list[PartnershipLevelFactory],
) -> RevenueConfigurationFactory:
    partnership_level = partnership_levels[random.randint(0, 1)]
    if [True, False][random.randint(0, 1)]:
        revenue_configuration: RevenueConfigurationFactory = RevenueConfigurationFactory.create(
            organization=organization,
            partnership_level=partnership_level,
        )
    else:
        def generate_course_code() -> str:
            import string
            letters = f"{string.ascii_uppercase}1234567890" 
            code = "".join(["".join(random.choices(letters)) for i in range(10)])
            return code
        
        revenue_configuration: RevenueConfigurationFactory = RevenueConfigurationFactory.create(
            course_code=generate_course_code(),
            partnership_level=partnership_level,
        )
    return revenue_configuration

def populate_shared_revenue(organization: OrganizationFactory) -> None:
    platinum = PartnershipLevelFactory.create(name="platinum")
    gold = PartnershipLevelFactory.create(name="gold")
    silver = PartnershipLevelFactory.create(name="silver")
    bronze = PartnershipLevelFactory.create(name="bronze")
    
    revenue_configuration = generate_revenue_configuration(
        organization=organization,
        partnership_levels=[platinum, gold, silver, bronze],
    )
    partnership_level: PartnershipLevelFactory = revenue_configuration.partnership_level
    revenue_configuration = RevenueConfigurationSerializer(revenue_configuration).data
    partnership_level = PartnershipLevelSerializer(partnership_level).data
    revenue_configuration["partnership_level"] = partnership_level
    ShareExecutionFactory.create(
        percentage=partnership_level["percentage"],
        revenue_configuration=revenue_configuration,
    )


def populate_billing(organization: OrganizationFactory) -> None:
    amount_of_receipts = 5
    receipts: list[ReceiptFactory] = ReceiptFactory.create_batch(amount_of_receipts, organization=organization)
    for receipt in receipts:
        ReceiptItemFactory.create(receipt=receipt)


def populate():
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
    print("Starting population script...")
    start = time.time()
    populate()
    finish = time.time() - start
    print(f"Finished population script in {finish}")
