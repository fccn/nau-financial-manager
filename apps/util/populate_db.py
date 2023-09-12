import os
import time
from typing import Any

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()


from apps.organization.factories import OrganizationAddressFactory, OrganizationContactFactory, OrganizationFactory
from apps.shared_revenue.factories import  PartnershipLevelFactory, RevenueConfigurationFactory, ShareExecutionFactory

import json
from json import JSONEncoder


def populate_organizations_resources(organization: OrganizationFactory) -> None:
    OrganizationContactFactory.create(organization=organization)
    OrganizationAddressFactory.create(organization=organization)

def populate_shared_revenue(organization: OrganizationFactory) -> None:
    partnership_level: PartnershipLevelFactory = PartnershipLevelFactory.create()
    revenue_configuration: RevenueConfigurationFactory = RevenueConfigurationFactory.create(
        organization=organization,
        partnership_level=partnership_level
    )
    revenue_configuration = JSONEncoder().encode({str(k) : str(v) for k, v in revenue_configuration.__dict__.items()})
    revenue_configuration = json.dumps(revenue_configuration)
    ShareExecutionFactory.create(
        organization=organization,
        revenue_configuration=revenue_configuration,
    )


def populate():
    try:
        organizations_amount: int = 5
        organizations: list[OrganizationFactory] = OrganizationFactory.create_batch(organizations_amount)
        for organization in organizations:
            populate_organizations_resources(organization=organization)
            populate_shared_revenue(organization=organization)
    except Exception as e:
        raise e


if __name__ == "__main__":
    print("Starting population script...")
    start = time.time()
    populate()
    finish = time.time() - start
    print(f"Finished population script in {finish}")
