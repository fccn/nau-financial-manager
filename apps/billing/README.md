# Billing Module

Descripton:
This module is responsible for handling billing and receipts.

## ERD of models

```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        -id: Integer
        -created_at: DateTime
        -updated_at: DateTime
    }
    class Receipt {
        -transaction_id: CharField
        -client_name: CharField
        -email: CharField
        -address_line_1: CharField
        -address_line_2: CharField
        -city: CharField
        -postal_code: CharField
        -state: CharField
        -country_code: CharField
        -vat_identification_number: CharField
        -vat_identification_country: CountryField
        -total_amount_exclude_vat: DecimalField
        -total_amount_include_vat: DecimalField
        -currency: CharField
        -payment_type: CharField
        -transaction_date: DateTime
        --
        +receipt_items: ReceiptItem [1-*]
    }
    class ReceiptItem {
        -description: CharField
        -quantity: PositiveIntegerField
        -vat_tax: DecimalField
        -amount_exclude_vat: DecimalField
        -amount_include_vat: DecimalField
        -organization_code: CharField
        -course_id: CharField
        -course_code: CharField
        --
        +receipt: Receipt [1]
    }
    BaseModel <|-- Receipt
    BaseModel <|-- ReceiptItem
```
