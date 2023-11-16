# Transaction complete payload

```json
{
	"transaction_id": "a9k05000-227f-4500-b71f-9f00fba1cf5f",
	"client_name": "Cliente name",
	"email": "cliente@email.com",
	"address_line_1": "Av. Liberdade",
	"address_line_2": "",
	"city": "Lisboa",
	"postal_code": "1250-142",
	"state": "",
	"country_code": "PT",
	"vat_identification_number": "PT123456789",
	"vat_identification_country": "PT",
	"total_amount_exclude_vat": 114.73,
	"total_amount_include_vat": 149.00,
	"currency": "EUR",
	"transaction_type" : "credit",
	"items": [{
		"description": "The product/line text with a description of what have been bought. The field need to be a string.",
		"quantity": 1,
		"vat_tax": 0.23,
		"unit_price_excl_tax": 114.73,
		"unit_price_incl_tax": 149.00,
		"organization_code": "UPorto",
		"course_id": "course-v1:UPorto+CBNEEF+2023_T3",
		"course_code": "CBNEEF"
	}]
}
```
