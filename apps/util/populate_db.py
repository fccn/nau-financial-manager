import os
import time

import django

from apps.organization.factories import OrganizationAddressFactory, OrganizationContactFactory, OrganizationFactory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()


def populate_organizations(organizations_amount: int) -> None:
    organizations: list[OrganizationFactory] = OrganizationFactory.create_batch(organizations_amount)
    for organization in organizations:
        OrganizationContactFactory.create(organization=organization)
        OrganizationAddressFactory.create(organization=organization)
    else:
        print(f"Populated with {organizations_amount} organizations")


def populate():
    try:
        populate_organizations(5)
    except Exception as e:
        raise e


if __name__ == "__main__":
    print("Starting population script...")
    start = time.time()
    populate()
    finish = time.time() - start
    print(f"Finished population script in {finish}")
