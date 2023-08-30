# Organization Module

Descripton:
This modules is responsible for handling informations of organizations.

## ERD of models

```mermaid
classDiagram
    class BaseModel {
        &lt;&lt;abstract&gt;&gt;
        -id: Integer
        -created_at: DateTime
        -updated_at: DateTime
    }
    class Organization {
        -uuid: UUIDField
        -name: CharField
        -short_name: CharField
        -slug: SlugField
        -vat_country: CharField
        -vat_number: CharField
        -iban: CharField
        +organization_addresses: OrganizationAddress[]
        +organization_contacts: OrganizationContact[]
        +__str__(): str
    }
    class OrganizationAddress {
        -organization: ForeignKey
        -address_type: CharField
        -street: CharField
        -postal_code: DecimalField
        -city: CharField
        -district: CharField
        -country: CharField
        +__str__(): str
    }
    class OrganizationContact {
        -organization: ForeignKey
        -contact_type: CharField
        -contact_value: CharField
        -description: CharField
        -is_main: BooleanField
        +__str__(): str
    }
    BaseModel &lt;|-- Organization
    BaseModel &lt;|-- OrganizationAddress
    BaseModel &lt;|-- OrganizationContact
    Organization "1" *-- "*" OrganizationAddress : organization_addresses
    Organization "1" *-- "*" OrganizationContact : organization_contacts
```
