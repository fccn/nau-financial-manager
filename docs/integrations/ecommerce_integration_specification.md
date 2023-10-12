# Specification of the integration with the Open edX Ecommerce

The NAU financial manager is the server and the Open edX Ecommerce is the client of the integration.

Note, this integration is similar of the [SAGE X3 integration](sage_x3_integration_specification.md).

- [Specification of the integration with the Open edX Ecommerce](#specification-of-the-integration-with-the-open-edx-ecommerce)
  - [Create Receipt](#create-receipt)
    - [Input](#input)
    - [Transaction id](#transaction-id)
      - [Client Name](#client-name)
      - [Email](#email)
      - [Address](#address)
      - [VAT Identification Number](#vat-identification-number)
      - [VAT Identification Country](#vat-identification-country)
      - [Total amount excluding VAT](#total-amount-excluding-vat)
      - [Total amount including VAT](#total-amount-including-vat)
      - [Currency](#currency)
      - [List of Receipt line's](#list-of-receipt-lines)
        - [Description](#description)
        - [Quantity](#quantity)
        - [Amount excluding VAT](#amount-excluding-vat)
        - [Amount including VAT](#amount-including-vat)
        - [Course id](#course-id)
        - [Organization code](#organization-code)
        - [Course code](#course-code)
    - [Output](#output)
      - [receipt id](#receipt-id)

## Create Receipt
The create receipt method should need to allow the NAU Financial Manager system to send this
kind of information.

### Input

### Transaction id
An identification of this transaction from the upstream system, to prevent the creation of
duplicate receipts.

#### Client Name
The name of the person or company that have payed and that we need to generate a receipt.

#### Email
The email of the person or company that bought the product, this field is important because is the
email address that the receipt will be sent automatically from the iLink.

#### Address
The optional address that should be put on the receipt.

The address need to have this fields:
- Address Line 1
- Address Line 2
- City
- Postal Code
- State
- Country Code

#### VAT Identification Number
The VAT identification number https://en.wikipedia.org/wiki/VAT_identification_number it need to be
a string because some countries use some letters in this identification.
Note without the country identification.

Example: 123456789
L99999999G

#### VAT Identification Country
The identification of the country on the VAT Identification Number.
It should need to be a 2 letter code using the standard
https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

Example, for Portugal use 'PT' and for Spain use 'ES'

#### Total amount excluding VAT
The amount excluding tax, in Portugal the IVA value.

#### Total amount including VAT
How much the client have payed.

#### Currency
The https://en.wikipedia.org/wiki/ISO_4217 standard that represent the currency.
In our case will always be the 'EUR'.

#### List of Receipt line's
Each Receipt has a list of Receipt lines.
A line on a receipt that represents a quantity of a product bought by a user.

##### Description
The product/line text with a description of what have been bought.
The field need to be a string.

##### Quantity
The quantity of have been bought.
In our case we should have always be with '1' has its value.
This field should be an integer.

##### Amount excluding VAT

Example: 114.73

##### Amount including VAT
The amount the user has bought including the VAT (IVA).

Example: 149.00

##### Course id
The course identification in the LMS.
Example: 'course-v1:UPorto+CBNEEF+2023_T3'

##### Organization code
The primary organization of that course.
Example: 'UPorto' or'INA'

Used by the the shared revenue module, if the the course doesn't have a specific multiple
organizations shared revenue configuration.

##### Course code
The smaller course code.
Example: 'CBNEEF'

### Output
The create Receipt method need to return a receipt identification inside the NAU Financial manager.
So we also store the pairs of transaction id and receipt identification inside the Ecommerce.
This is important so we know what already have been sent to the NAU Financial manager and what
still need to be sent.

#### receipt id
An Identification of this receipt inside the NAU Financial manager.
