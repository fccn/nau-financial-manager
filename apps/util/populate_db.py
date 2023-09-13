import os
import time
from typing import Any

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()


from apps.organization.factories import OrganizationAddressFactory, OrganizationContactFactory, OrganizationFactory
from apps.shared_revenue.factories import  PartnershipLevelFactory, RevenueConfigurationFactory, ShareExecutionFactory
from apps.billing.factories import ReceiptFactory, ReceiptItemFactory
from apps.shared_revenue.serializers import PartnershipLevelSerializer, RevenueConfigurationSerializer

import json
from json import JSONEncoder


def populate_organizations_resources(organization: OrganizationFactory) -> None:
    OrganizationContactFactory.create(organization=organization)
    OrganizationAddressFactory.create(organization=organization)
    print("---Populated organizations---")

def populate_shared_revenue(organization: OrganizationFactory) -> None:
    partnership_level = PartnershipLevelFactory.create()
    revenue_configuration = RevenueConfigurationSerializer(RevenueConfigurationFactory.create(partnership_level=partnership_level)).data
    partnership_level = PartnershipLevelSerializer(partnership_level).data
    revenue_configuration["partnership_level"] = partnership_level
    ShareExecutionFactory.create(revenue_configuration=revenue_configuration)

def populate_billing(organization: OrganizationFactory) -> None:
    receipt_factory: ReceiptFactory = ReceiptFactory.create(organization=organization)  
    ReceiptItemFactory(receipt=receipt_factory)
    print("---Populated billing---")

def populate_billing(organization: OrganizationFactory) -> None:
    receipt_factory: ReceiptFactory = ReceiptFactory.create(organization=organization)  
    ReceiptItemFactory(receipt=receipt_factory)
    print("---Populated billing---")


def populate():
    try:
        organizations_amount: int = 1
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
