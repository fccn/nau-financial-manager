MOCKED_RESPONSE = {
    "success": "true",
    "response": {
        "data": {
            "id": "5c65775834a084.67949646",
            "number": "FR0293841",
            "atcud": "N987456123",
            "emission_date": "2019-02-12",
            "due_date": "2019-02-14",
            "tax_point_date": "2020-06-02 09:36:39",
            "invoice_period": {"start_date": "2020-06-02", "end_date": "2020-07-03"},
            "created_at": "2020-06-02 09:36:39",
            "type_document_fact": "Fatura",
            "type_document": "Recebido",
            "state_document": "Enviado",
            "currency": {"code": "EUR", "symbol": "€"},
            "decimal_place": "2",
            "supplier": {
                "id": "5c9cb8ad792050.40584384",
                "gln": "PT1589854154120002541",
                "number": "172804094",
                "tax_scheme": "VAT",
                "name": "Abreu-Cunha Lda",
                "city": "Lisboa",
                "street": "Estrada XPTO",
                "additional_street": "Rua 29",
                "building": "Ed. Por do Sol",
                "building_number": "20",
                "postal_zone": "4200-060",
                "region": "Madeira",
                "country_code": "PT",
                "country": "Portugal",
                "email": "macedo17642@gmail.com",
                "telephone": "799396117",
                "telefax": "291456852",
                "company_legal_form": "50.000 €",
            },
            "customer": {
                "id": "5da5cec2db1413.55248297",
                "number": "256869146",
                "gln": "PT1589854154120002541",
                "tax_scheme": "VAT",
                "name": "Entidade exemplo",
                "city": "Lisboa",
                "street": "Estrada...",
                "additional_street": "Rua 23",
                "building": "Ed. Por do Sol",
                "building_number": "20",
                "postal_zone": "4200-060",
                "region": "Madeira",
                "country_code": "PT",
                "country": "Portugal",
                "email": "exemplo@gmail.com",
                "telephone": "799396117",
                "telefax": "291456852",
            },
            "platform": "iGest",
            "attachments": [
                {
                    "type": "pdf",
                    "file": "https://ilink.pt/ilink-api/file/lPikLsRAJEyjGmHsrAVATZuJgba7xgjf7dgJsJ85eEd8ScQbAEwG8ovh0IeP",
                    "identifier": "FT 1/1",
                    "ubl_type": "invoice_representation",
                    "hash": "pPikLsRAJEyjGmHsrAVATZuJgba7xgjf7dgJsJ85eEd8ScQbAEwG8ovh0IeP",
                }
            ],
            "amounts": {
                "tax_amount": "4.86",
                "amount": "26.00",
                "discount_amount": "1.00",
                "charge_amount": "1.00",
                "prepaid_amount": "0.00",
                "payable_amount": "29.86",
                "payable_rounding_amount": "0.00",
                "withholding_tax_amount": "1.00",
                "total_amount": "29.86",
            },
            "process_state": {
                "id": "5eec77c7a13500.90538935",
                "name": "Pago",
                "group": {"id": "5eec77c61cd3d5.41780466", "name": "iDok"},
                "created_at": "2020-02-19 09:31:03",
            },
            "validity_period": "2020-07-06",
            "buyer_number": "1145",
            "exchange_currency": "GBP",
            "exchange_calculation_rate": "1.00",
            "project_reference": "BT77855",
            "despatch_document_reference": "X8745715747898",
            "receipt_document_reference": "RC87575411",
            "payee": {
                "gln": "PT1587456211",
                "number": "256869146",
                "name": "Entidade exemplo",
                "city": "Funchal",
                "street": "Rua das flores",
                "additional_street": "ER 145",
                "postal_zone": "9000-444",
                "region": "Porto",
                "country_code": "PT",
                "country": "Portugal",
                "email": "exemplo@gmail.com",
                "telephone": "799396117",
                "telefax": "985454125",
            },
            "tax_representative": {
                "number": "256869146",
                "name": "Entidade exemplo",
                "city": "Porto",
                "street": "Rua exemplo",
                "additional_street": "Rua Extra",
                "postal_zone": "9000-111",
                "region": "Porto",
                "country_code": "PT",
                "country": "Portugal",
                "email": "exemplo@gmail.com",
                "telephone": "799396117",
                "telefax": "9865124456",
            },
            "lines": [
                {
                    "id": "1",
                    "seller_number": "H458445",
                    "buyer_number": "998565",
                    "name": "Caderno",
                    "description": "Ref 1458789",
                    "quantity": "5.000",
                    "base_quantity": "1.000",
                    "price_amount": "4.00000000",
                    "unit": "C62",
                    "origin_country": "PT",
                    "commodity_classification": "005",
                    "ean_item_identification": "77451",
                    "buyer_material_code": "X5689855",
                    "seller_material_code": "456875111",
                    "currency": "EUR",
                    "amount": "20.00000000",
                    "tax_amount": "4.40000000",
                    "allowance_charge": [
                        {
                            "type": "false",
                            "reason_code": "R01",
                            "reason": "Desconto comercial",
                            "amount": "1.00",
                            "base_amount": "1.00",
                        }
                    ],
                    "taxes_info": [
                        {
                            "taxable_amount": "20.000",
                            "tax_amount": "4.40",
                            "id": "NOR",
                            "percent": "22.00",
                            "code": "VAT",
                            "name": "S",
                            "tax_exemption_reason_code": "M06",
                            "tax_exemption_reason": "Autofaturação",
                        }
                    ],
                    "price_discount": {"type": "false", "amount": "1.00", "base_amount": "5.00"},
                    "references": [{"document_type": "invoice", "line": "2"}],
                    "informations": [
                        {"description": "Nº Compromisso", "type": "requisition", "number": "256", "line": "1"}
                    ],
                    "commitment": {"number": "155/2021", "line": "1"},
                    "invoice_period": {"start_date": "2020-06-02", "end_date": "2020-07-03"},
                    "notes": ["Cor: azul, formato: PVC-75"],
                }
            ],
            "allowance_charge": [
                {
                    "type": "false",
                    "reason_code": "R01",
                    "reason": "Portes",
                    "amount": "1.00",
                    "base_amount": "1.00",
                    "tax_info": {"id": "NOR", "percent": "23.00", "code": "VAT", "name": "S"},
                }
            ],
            "withholding_tax": [{"description": "IRS", "tax_amount": "1.00", "type": "IRF"}],
            "payment_terms": {"note": "20 dias", "due_date": "2020-07-03"},
            "payment_means": {
                "code": "CC",
                "atm_payment_entity": "21947",
                "atm_payment_reference": "111222555444",
                "atm_payment_value": "200.24",
                "card_number": "11134697648528",
                "card_name": "João",
                "credits": "{}",
                "debited_mandate": "Mandato R457451",
                "debited_account": "PT5011456587854",
            },
            "delivery": {
                "id": "PT158985400001541264",
                "delivery_date": "2020-06-02",
                "name_place": "Local...",
                "city": "Lisboa",
                "street": "Rua ...",
                "postal_zone": "1234-321",
                "country_name": "Portugal",
                "country_code": "PT",
            },
            "references": [{"document_type": "invoice", "number": "FT/1"}],
            "informations": [{"description": "Nº Compromisso", "type": "commitment", "number": "991"}],
            "additional_informations": [{"description": "Nº de ...", "value": "4735744"}],
            "reasons": [
                {"reason": "Inconformidade: Deve existir número de compromisso.", "created_at": "2020-06-02 15:51:12"}
            ],
            "notes": ["Os bens foram colocados à disposição na data indicada"],
            "document_related": [
                {
                    "description": "Ficheiro xpto",
                    "file": "https://ilink.pt/file/Gg5Eh9UMfAivaHbuS5boKDSPHd6F88GEfalP9UhpVtAfcbwSo0JPKRvN8tlx",
                }
            ],
            "state_edi_document": {
                "id": "605369246b3412.42340492",
                "alias": "accepted",
                "alias_espap": "ACCEPTED",
                "description": "Aceite",
            },
            "emails": [
                {
                    "id": "605369246b3412.42341492",
                    "b_open": True,
                    "b_sent": True,
                    "created_at": "Unknown Type: date",
                    "opened_at": "Unknown Type: date",
                    "address": {},
                }
            ],
            "to_send_status": {
                "alias": "sent_document",
                "description": "A aguardar o envio do documento ao destinatário.",
            },
        }
    },
}
