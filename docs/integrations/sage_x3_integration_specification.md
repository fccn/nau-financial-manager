# Specification of the integration with the Sage X3

This document describes the specification of integration from the NAU Financial Manager application
with the Sage X3 ERP.

The NAU Financial Manager system is the client and the Sage X3 ERP is the server of the integration.

- [Specification of the integration with the Sage X3](#specification-of-the-integration-with-the-sage-x3)
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
    - [Output](#output)
      - [receipt id or number](#receipt-id-or-number)
  - [Get receipt document link](#get-receipt-document-link)
    - [Input](#input-1)
      - [receipt id or number](#receipt-id-or-number-1)
    - [Output](#output-1)
      - [Receipt link to PDF](#receipt-link-to-pdf)

## Create Receipt
The create receipt method should need to allow the NAU Financial Manager system to send this
kind of information.

### Input

### Transaction id
An identification of this transaction from the upstream system, to prevent the creation of duplicate receipts.

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
It should need to be a 2 letter code using the standard https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

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

### Output
The create Receipt method need to return a receipt identification.
So the NAU Financial Manager system knows how to get the receipt link to the PDF document.

#### receipt id or number
The standard receipt number.
Ex:  'FS 1234567/123456'

## Get receipt document link

This service is need so we can show the receipt PDF to the client inside the user interface of NAU.

Should this method be called directly to the iLink system?

### Input

#### receipt id or number

### Output

#### Receipt link to PDF
A link to a PDF document with the receipt. This link shown be similar with the link to the receipt
PDF document sent by email by the iLink system to the client.
