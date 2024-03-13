import json
from random import randint

from django.conf import settings
from requests import Response

ILINK_RESPONSE_MOCK = {
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


def xml_success_response_mock(data):
    return f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:wss="http://www.adonix.com/WSS">
                <soapenv:Body>
                    <wss:saveResponse soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                        <saveReturn xsi:type="wss:CAdxResultXml">
                            <messages xsi:type="soapenc:Array" soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" soapenc:arrayType="wss:CAdxMessage[0]"/>
                            <resultXml xsi:type="xsd:string"><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
                <RESULT>
                    <GRP ID="SIH0_1">
                        <FLD NAME="SALFCY" TYPE="Char">SED</FLD>
                        <FLD NAME="ZSALFCY" TYPE="Char"/>
                        <FLD NAME="SIVTYP" TYPE="Char">{data["nau_data"]['SIVTYP']}</FLD>
                        <FLD NAME="ZSIVTYP" TYPE="Char"/>
                        <FLD NAME="NUM" TYPE="Char">{settings.DEFAULT_SERIES}-23/000{randint(10, 99)}</FLD>
                        <FLD NAME="INVREF" TYPE="Char">{data["nau_data"]['INVREF']}</FLD>
                        <FLD NAME="INVDAT" TYPE="Date">{data["nau_data"]['INVDAT']}</FLD>
                        <FLD NAME="BPCINV" TYPE="Char">{data["nau_data"]['BPCINV']}</FLD>
                        <FLD NAME="BPINAM" TYPE="Char">Cliente NAU via soap-ui 2</FLD>
                        <FLD NAME="CUR" TYPE="Char">{data["nau_data"]['CUR']}</FLD>
                        <FLD NAME="ZCUR" TYPE="Char"/>
                        <FLD NAME="ORIDOCNUM" TYPE="Char"/>
                        <FLD MENULAB="F1- Factura (art. 6.7.7 y 7.3 del RD 1619/2012) " MENULOCAL="2109" NAME="INVTYPSPA" TYPE="Integer">1</FLD>
                    </GRP>
                    <GRP ID="SIH1_1">
                        <FLD NAME="SIHNUMEND" TYPE="Char"/>
                        <FLD MENULAB="Não" MENULOCAL="1" NAME="SIHCFMFLG" TYPE="Integer">1</FLD>
                    </GRP>
                    <GRP ID="SIH1_4">
                        <FLD MENULAB="Retificação integra" MENULOCAL="2069" NAME="METCOR" TYPE="Integer">1</FLD>
                        <FLD NAME="PERDEB" TYPE="Date"></FLD>
                        <FLD NAME="PERFIN" TYPE="Date"></FLD>
                        <FLD NAME="BELVCS" TYPE="Char"/>
                    </GRP>
                    <GRP ID="SIH1_5">
                        <FLD NAME="VACBPR" TYPE="Char">{data["billing_data"]['VACBPR']}</FLD>
                        <FLD NAME="ZVACBPR" TYPE="Char"/>
                        <FLD MENULAB="c/IVA" MENULOCAL="243" NAME="PRITYP" TYPE="Integer">{data["billing_data"]['PRITYP']}</FLD>
                    </GRP>
                    <GRP ID="SIH1_6">
                        <FLD MENULAB="Não" MENULOCAL="1" NAME="STOMVTFLG" TYPE="Integer">1</FLD>
                        <FLD NAME="YVCRNUM" TYPE="Char"/>
                        <FLD MENULAB="Não" MENULOCAL="1" NAME="YGIAFSTA" TYPE="Integer">1</FLD>
                        <FLD MENULAB="Não" MENULOCAL="1" NAME="YGIAFSTAPAR" TYPE="Integer">1</FLD>
                    </GRP>
                    <GRP ID="SIH2_2">
                        <FLD NAME="PTE" TYPE="Char">PTTRFPP</FLD>
                        <FLD NAME="ZPTE" TYPE="Char"/>
                        <FLD NAME="PAYBAN" TYPE="Char"/>
                        <FLD NAME="ZPAYBAN" TYPE="Char"/>
                    </GRP>
                    <GRP ID="SIH4_2">
                        <FLD NAME="PFMTOT" TYPE="Decimal">0</FLD>
                    </GRP>
                    <GRP ID="SIH4_3">
                        <FLD NAME="INVNOT" TYPE="Decimal">0</FLD>
                        <FLD NAME="INVATI" TYPE="Decimal">0</FLD>
                    </GRP>
                    <GRP ID="SIHV_1">
                        <FLD NAME="VALUATION" TYPE="Char"/>
                    </GRP>
                    <GRP ID="SIHV_4">
                        <FLD NAME="INVNOT" TYPE="Decimal">0</FLD>
                        <FLD NAME="INVNOTRPT" TYPE="Decimal">0</FLD>
                        <FLD NAME="DEVRPT1" TYPE="Char"/>
                        <FLD NAME="BASDEP" TYPE="Decimal">0</FLD>
                        <FLD NAME="INVATI" TYPE="Decimal">0</FLD>
                        <FLD NAME="INVATIRPT" TYPE="Decimal">0</FLD>
                        <FLD NAME="DEVRPT2" TYPE="Char"/>
                    </GRP>
                    <GRP ID="YIL_1">
                        <FLD MENULAB="" MENULOCAL="6100" NAME="YILINK" TYPE="Integer">0</FLD>
                        <FLD NAME="YILINKDATE" TYPE="Date"></FLD>
                        <FLD NAME="YILINKTIME" TYPE="Char"/>
                        <FLD NAME="YILINKPROC" TYPE="Char"/>
                        <FLD NAME="YILINKUSR" TYPE="Char"/>
                        <FLD NAME="YILINKMESS" TYPE="Char"/>
                    </GRP>
                    <GRP ID="YIL_2">
                        <FLD NAME="YCRY" TYPE="Char">PT</FLD>
                        <FLD NAME="YCRYNAM" TYPE="Char">Portugal</FLD>
                        <FLD NAME="YPOSCOD" TYPE="Char">{data["client_data"]['YPOSCOD']}</FLD>
                        <FLD NAME="YCTY" TYPE="Char">{data["client_data"]['YCTY']}</FLD>
                        <FLD NAME="YBPIEECNUM" TYPE="Char">{data["client_data"]['YBPIEECNUM']}</FLD>
                        <FLD NAME="YILINKMAIL" TYPE="Char">{data["client_data"]['YILINKMAIL']}</FLD>
                        <FLD NAME="YPAM" TYPE="Char">{data["client_data"]['YPAM']}</FLD>
                        <LST NAME="YBPRNAM" SIZE="2" TYPE="Char">
                            <ITM>Cliente NAU via soap-ui 1</ITM>
                            <ITM>Cliente NAU via soap-ui 2</ITM>
                        </LST>
                        <LST NAME="YBPAADDLIG" SIZE="3" TYPE="Char">
                            {data["address_items"]}
                        </LST>
                    </GRP>
                    <GRP ID="ADXTEC">
                        <FLD NAME="WW_MODSTAMP" TYPE="Char">20231109103351</FLD>
                        <FLD NAME="WW_MODUSER" TYPE="Char">WSNAU</FLD>
                    </GRP>
                    <TAB DIM="300" ID="SIH4_1" SIZE="2">
                        <LIN NUM="1">
                            <FLD NAME="ITMREF" TYPE="Char">{data["transaction_item_data"]['ITMREF']}</FLD>
                            <FLD NAME="ITMDES" TYPE="Char">Genérico NAU - Formação Cientifca e Tec. </FLD>
                            <FLD NAME="ITMDES1" TYPE="Char">{data["transaction_item_data"]['ITMDES1']}</FLD>
                            <FLD NAME="YPERIODO" TYPE="Date"></FLD>
                            <FLD NAME="YPERIODOF" TYPE="Date"></FLD>
                            <FLD NAME="ECCVALMAJ" TYPE="Char"/>
                            <FLD NAME="INVPRC" TYPE="Decimal">0</FLD>
                            <FLD NAME="SAU" TYPE="Char">UN</FLD>
                            <FLD NAME="QTY" TYPE="Decimal">{data["transaction_item_data"]['QTY']}</FLD>
                            <FLD NAME="SAUSTUCOE" TYPE="Decimal">1</FLD>
                            <FLD NAME="STU" TYPE="Char">{data["transaction_item_data"]['STU']}</FLD>
                            <FLD NAME="GROPRI" TYPE="Decimal">{data["transaction_item_data"]['GROPRI']}</FLD>
                            <FLD NAME="DISCRGVAL1" TYPE="Decimal">{data["transaction_item_data"]['DISCRGVAL1']}</FLD>
                            <FLD NAME="DISCRGVAL2" TYPE="Decimal">0</FLD>
                            <FLD NAME="DISCRGVAL3" TYPE="Decimal">0</FLD>
                            <FLD NAME="DISCRGVAL4" TYPE="Decimal">0</FLD>
                            <FLD NAME="DISCRGVAL5" TYPE="Decimal">0</FLD>
                            <FLD NAME="DISCRGVAL6" TYPE="Decimal">0</FLD>
                            <FLD NAME="NETPRI" TYPE="Decimal">100</FLD>
                            <FLD NAME="CPRPRI" TYPE="Decimal">0</FLD>
                            <FLD NAME="PFM" TYPE="Decimal">81.3008</FLD>
                            <FLD NAME="VACITM1" TYPE="Char">{data["transaction_item_data"]['VACITM1']}</FLD>
                            <FLD NAME="VACITM2" TYPE="Char"/>
                            <FLD NAME="VACITM3" TYPE="Char"/>
                            <FLD NAME="SSTCOD" TYPE="Char"/>
                            <FLD NAME="CCE1" TYPE="Char"/>
                            <FLD NAME="CCE2" TYPE="Char"/>
                            <FLD NAME="CCE3" TYPE="Char"/>
                            <FLD NAME="CCE4" TYPE="Char"/>
                            <FLD NAME="CCE5" TYPE="Char"/>
                            <FLD NAME="CCE6" TYPE="Char"/>
                            <FLD NAME="CCE7" TYPE="Char"/>
                            <FLD NAME="CCE8" TYPE="Char"/>
                            <FLD NAME="CCE9" TYPE="Char"/>
                            <FLD NAME="CCE10" TYPE="Char"/>
                            <FLD NAME="CCE11" TYPE="Char"/>
                            <FLD NAME="CCE12" TYPE="Char"/>
                            <FLD NAME="CCE13" TYPE="Char"/>
                            <FLD NAME="CCE14" TYPE="Char"/>
                            <FLD NAME="CCE15" TYPE="Char"/>
                            <FLD NAME="CCE16" TYPE="Char"/>
                            <FLD NAME="CCE17" TYPE="Char"/>
                            <FLD NAME="CCE18" TYPE="Char"/>
                            <FLD NAME="CCE19" TYPE="Char"/>
                            <FLD NAME="CCE20" TYPE="Char"/>
                            <FLD MENULAB="Não" MENULOCAL="439" NAME="FOCFLG" TYPE="Integer">1</FLD>
                            <FLD MENULAB="Não" MENULOCAL="1" NAME="EECFLOPHY" TYPE="Integer">1</FLD>
                            <FLD NAME="YNRPAR" TYPE="Char"/>
                            <FLD NAME="YNPAR" TYPE="Char"/>
                            <FLD NAME="YDPAR" TYPE="Char"/>
                            <FLD NAME="YRUBPRJ" TYPE="Char"/>
                            <FLD NAME="YPROGRAMA" TYPE="Char"/>
                            <FLD NAME="YORIORC" TYPE="Char"/>
                            <FLD NAME="ZYORIORC" TYPE="Char"/>
                            <FLD NAME="YNGPROC" TYPE="Char"/>
                            <FLD NAME="YMEDIDA" TYPE="Char"/>
                            <FLD NAME="YFONTFIN" TYPE="Char"/>
                            <FLD NAME="YCPOC" TYPE="Char"/>
                            <FLD NAME="YCONTANL" TYPE="Char"/>
                            <FLD NAME="YCLASORG" TYPE="Char"/>
                            <FLD NAME="YCLASFUNC" TYPE="Char"/>
                            <FLD NAME="YCCUSTO" TYPE="Char"/>
                            <FLD NAME="YCECON" TYPE="Char"/>
                            <FLD NAME="YBASELEGAL" TYPE="Char"/>
                            <FLD NAME="YSUBCENTRO" TYPE="Char"/>
                            <FLD NAME="YTCONT" TYPE="Char"/>
                            <FLD NAME="YCPOCREC" TYPE="Char"/>
                            <FLD NAME="YACT" TYPE="Char"/>
                            <FLD NAME="YTRUBPRJ" TYPE="Char"/>
                            <FLD NAME="YACCANALFCCN" TYPE="Char"/>
                        </LIN>
                    </TAB>
                    <TAB DIM="20" ID="SIHV_2" SIZE="1">
                        <LIN NUM="1">
                            <FLD NAME="NOLIGV" TYPE="Integer">0</FLD>
                            <FLD NAME="XVSHO" TYPE="Char"/>
                            <FLD NAME="XVNOT" TYPE="Decimal">1626.02</FLD>
                            <FLD NAME="XVSMI" TYPE="Decimal">1626.02</FLD>
                            <FLD NAME="XVTAX" TYPE="Char">PT003</FLD>
                            <FLD NAME="XVRAT" TYPE="Decimal">23</FLD>
                            <FLD NAME="XVAMT" TYPE="Decimal">373.98</FLD>
                            <FLD NAME="XVSUP" TYPE="Decimal">0</FLD>
                            <FLD NAME="XVATI" TYPE="Decimal">0</FLD>
                        </LIN>
                    </TAB>
                </RESULT>]]></resultXml>
                            <status xsi:type="xsd:int">1</status>
                            <technicalInfos xsi:type="wss:CAdxTechnicalInfos">
                            <busy xsi:type="xsd:boolean">false</busy>
                            <changeLanguage xsi:type="xsd:boolean">false</changeLanguage>
                            <changeUserId xsi:type="xsd:boolean">false</changeUserId>
                            <flushAdx xsi:type="xsd:boolean">false</flushAdx>
                            <loadWebsDuration xsi:type="xsd:double">5</loadWebsDuration>
                            <nbDistributionCycle xsi:type="xsd:int">-1</nbDistributionCycle>
                            <poolDistribDuration xsi:type="xsd:double">3</poolDistribDuration>
                            <poolEntryIdx xsi:type="xsd:int">14948</poolEntryIdx>
                            <poolExecDuration xsi:type="xsd:double">5480</poolExecDuration>
                            <poolRequestDuration xsi:type="xsd:double">-1</poolRequestDuration>
                            <poolWaitDuration xsi:type="xsd:double">0</poolWaitDuration>
                            <processReport xsi:type="xsd:string" xsi:nil="true"/>
                            <processReportSize xsi:type="xsd:int">-1</processReportSize>
                            <reloadWebs xsi:type="xsd:boolean">false</reloadWebs>
                            <resumitAfterDBOpen xsi:type="xsd:boolean">false</resumitAfterDBOpen>
                            <rowInDistribStack xsi:type="xsd:int" xsi:nil="true"/>
                            <totalDuration xsi:type="xsd:double">5507</totalDuration>
                            <traceRequest xsi:type="xsd:string"/>
                            <traceRequestSize xsi:type="xsd:int">0</traceRequestSize>
                            </technicalInfos>
                        </saveReturn>
                    </wss:saveResponse>
                </soapenv:Body>
                </soapenv:Envelope>
        """


def xml_duplicate_error_response_mock():
    return f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:wss="http://www.adonix.com/WSS">
            <soapenv:Body>
                <wss:saveResponse soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <saveReturn xsi:type="wss:CAdxResultXml">
                        <messages xsi:type="soapenc:Array" soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" soapenc:arrayType="wss:CAdxMessage[1]">
                        <messages href="#id0"/>
                        </messages>
                        <resultXml xsi:type="xsd:string" xsi:nil="true"/>
                        <status xsi:type="xsd:int">0</status>
                        <technicalInfos xsi:type="wss:CAdxTechnicalInfos">
                        <busy xsi:type="xsd:boolean">false</busy>
                        <changeLanguage xsi:type="xsd:boolean">false</changeLanguage>
                        <changeUserId xsi:type="xsd:boolean">true</changeUserId>
                        <flushAdx xsi:type="xsd:boolean">false</flushAdx>
                        <loadWebsDuration xsi:type="xsd:double">36</loadWebsDuration>
                        <nbDistributionCycle xsi:type="xsd:int">-1</nbDistributionCycle>
                        <poolDistribDuration xsi:type="xsd:double">2</poolDistribDuration>
                        <poolEntryIdx xsi:type="xsd:int">11260</poolEntryIdx>
                        <poolExecDuration xsi:type="xsd:double">16770</poolExecDuration>
                        <poolRequestDuration xsi:type="xsd:double">-1</poolRequestDuration>
                        <poolWaitDuration xsi:type="xsd:double">1</poolWaitDuration>
                        <processReport xsi:type="xsd:string" xsi:nil="true"/>
                        <processReportSize xsi:type="xsd:int">-1</processReportSize>
                        <reloadWebs xsi:type="xsd:boolean">false</reloadWebs>
                        <resumitAfterDBOpen xsi:type="xsd:boolean">false</resumitAfterDBOpen>
                        <rowInDistribStack xsi:type="xsd:int" xsi:nil="true"/>
                        <totalDuration xsi:type="xsd:double">16866</totalDuration>
                        <traceRequest xsi:type="xsd:string"/>
                        <traceRequestSize xsi:type="xsd:int">0</traceRequestSize>
                        </technicalInfos>
                    </saveReturn>
                </wss:saveResponse>
                <multiRef id="id0" soapenc:root="0" soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xsi:type="wss:CAdxMessage">
                    <type>3</type>
                    <message>Nº Fatura NAU já registada no documento: {settings.DEFAULT_SERIES}-{randint(21, 23)}/000{randint(10, 64)}</message>
                </multiRef>
            </soapenv:Body>
            </soapenv:Envelope>
        """


UNAUTHORIZED_ILINK_RESPONSE = {"success": False, "errors": [{"code": "e069", "msg": "Autenticação inválida."}]}


class MockResponse(Response):
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    @property
    def content(self):
        data = self.data
        if not isinstance(data, str):
            data = json.JSONEncoder().encode(o=self.data)

        return data
