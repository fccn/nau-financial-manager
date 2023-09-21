# Billing Module

Descripton:
This module is responsible for handling billing and receipts.

## ERD of models

```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        -id: IntegerField
        -created_at: DateTimeField
        -updated_at: DateTimeField
    }
    class CountryField {
        <<external>>
    }
    class Organization {
        <<external>>
    }
    class Receipt {
        -name: CharField
        -email: CharField
        -address: CharField
        -vat_identification_country: CountryField
        -vat_identification_number: CharField
        -total_amount_exclude_vat: DecimalField
        -total_amount_include_vat: DecimalField
        -receipt_link: CharField
        -receipt_document_id: CharField
        -organization: ForeignKey(Organization)
        +__str__(): str
    }
    class ReceiptItem {
        -receipt: ForeignKey(Receipt)
        -description: CharField
        -quantity: PositiveIntegerField
        -vat_tax: DecimalField
        -amount_exclude_vat: DecimalField
        -amount_include_vat: DecimalField
        -organization_code: CharField
        -course_code: CharField
        -course_id: CharField
        +__str__(): str
        +Meta: UniqueConstraint
    }
    BaseModel <|-- Receipt
    BaseModel <|-- ReceiptItem
```
