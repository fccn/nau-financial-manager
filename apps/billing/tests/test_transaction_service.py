from unittest import mock

import xmltodict
from django.conf import settings
from django.test.testcases import TestCase
from requests import Response

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.services.financial_processor_service import ProcessorInstantiator, TransactionProcessorInterface
from apps.billing.services.processor_service import SageX3Processor
from apps.billing.services.transaction_service import TransactionService

nau_data = {}
billing_data = {}
client_data = {}
transaction_item_data = {}


def insert_in_dict(item: dict):
    """
    This method insets in the right dict the payload informations.

    Each dict will be used to populate the response payload.
    """

    if item["@NAME"] in ["SIVTYP", "INVREF", "INVDAT", "BPCINV", "CUR"]:
        nau_data[item["@NAME"]] = item["#text"]

    if item["@NAME"] in ["VACBPR", "PRITYP"]:
        billing_data[item["@NAME"]] = item["#text"]

    if item["@NAME"] in ["YPOSCOD", "YCTY", "YBPIEECNUM", "YILINKMAIL", "YPAM", "YBPAADDLIG", "ITM"]:
        if item["@NAME"] == "YBPAADDLIG":
            client_data[item["@NAME"]] = item["ITM"]
        else:
            client_data[item["@NAME"]] = item["#text"]

    if item["@NAME"] in ["ITMREF", "ITMDES1", "QTY", "STU", "GROPRI", "DISCRGVAL1", "VACITM1"]:
        transaction_item_data[item["@NAME"]] = item["#text"]


def processor_response(*args, **kwargs):
    """
    This method is a mock, when the `requests.post` method is called from the test,
    the result of the request will be returned from this method.
    """

    class MockResponse(Response):
        def __init__(self, data, status_code):
            self.data = data
            self.status_code = status_code

        @property
        def content(self):
            return str(self.data)

    received_data = xmltodict.parse(kwargs["data"])["soapenv:Envelope"]["soapenv:Body"]["wss:save"]["objectXml"]
    received_data = xmltodict.parse(received_data["#text"])

    for grp in received_data["PARAM"]["GRP"]:
        for k in ["LST", "FLD"]:
            if k in grp:
                if isinstance(grp[k], list):
                    for item in grp[k]:
                        insert_in_dict(item=item)
                else:
                    insert_in_dict(item=grp[k])

    for fld in received_data["PARAM"]["TAB"]["LIN"]["FLD"]:
        insert_in_dict(item=fld)

    response_as_xml = generate_data_to_response(
        nau_data=nau_data,
        billing_data=billing_data,
        client_data=client_data,
        transaction_item_data=transaction_item_data,
    )

    return MockResponse(response_as_xml, 200)


class TransactionServiceTestCase(TestCase):
    def setUp(self) -> None:
        """
        This method instantiates all the necessary components, get the url for transaction processor service
        and creates a combination of one `Transaction` and `TransactionItem`.
        """

        self.financial_processor_interface = TransactionProcessorInterface()
        self.transaction_service = TransactionService()
        self._transaction_processor = SageX3Processor()
        self.transaction = TransactionFactory.create()
        self.transaction_item = TransactionItemFactory.create(transaction=self.transaction)
        self.processor_url = getattr(settings, "TRANSACTION_PROCESSOR_URL")

        return super().setUp()

    def test_financial_processor_service(self):
        """
        This test ensures that if not implemented, the method from the interface
        will raise an exception.

        """
        with self.assertRaisesMessage(
            expected_exception=Exception,
            expected_message="This method needs to be implemented",
        ):
            self.financial_processor_interface.send_transaction_to_processor(transaction=self.transaction)

    def test_processor_instance(self):
        """
        This test ensures that the dependency inversion of the `ProcessorInstantiator` and `TransactionProcessorInterface`
        is working as expected.
        """

        processor = ProcessorInstantiator(processor=SageX3Processor)

        self.assertEqual(type(processor), type(self._transaction_processor))
        self.assertEqual(type(processor), SageX3Processor)
        self.assertTrue(isinstance(processor, TransactionProcessorInterface))

    @mock.patch("requests.post", side_effect=processor_response)
    def test_transaction_processor(self, mocked_post):
        """
        This test is a call for the processor service, it will use the written service with a mocked response.

        It sets the `TRANSACTION_PROCESSOR_URL` variable as `http://fake-processor.com`, which will be
        setted as the real service url again in the `tearDown` class test method.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        processor: SageX3Processor = ProcessorInstantiator(processor=SageX3Processor)
        response = processor.send_transaction_to_processor(transaction=self.transaction)

        self.assertTrue(response)
        self.assertEqual(type(response), dict)

    def tearDown(self) -> None:
        """
        This method is called in the last moment of the `TestCase` class and sets the `TRANSACTION_PROCESSOR_URL`
        varible as the real service url again.
        """
        setattr(settings, "TRANSACTION_PROCESSOR_URL", self.processor_url)
        return super().tearDown()


def generate_data_to_response(
    nau_data: dict,
    billing_data: dict,
    client_data: dict,
    transaction_item_data: dict,
):
    address_items = ""
    for address in client_data["YBPAADDLIG"]:
        address_items = f"{address_items}<ITM>{address}</ITM>"

    response_as_xml = f"""
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
                    <FLD NAME="SIVTYP" TYPE="Char">{nau_data['SIVTYP']}</FLD>
                    <FLD NAME="ZSIVTYP" TYPE="Char"/>
                    <FLD NAME="NUM" TYPE="Char">FRN-23/00051</FLD>
                    <FLD NAME="INVREF" TYPE="Char">{nau_data['INVREF']}</FLD>
                    <FLD NAME="INVDAT" TYPE="Date">{nau_data['INVDAT']}</FLD>
                    <FLD NAME="BPCINV" TYPE="Char">{nau_data['BPCINV']}</FLD>
                    <FLD NAME="BPINAM" TYPE="Char">Cliente NAU via soap-ui 2</FLD>
                    <FLD NAME="CUR" TYPE="Char">{nau_data['CUR']}</FLD>
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
                    <FLD NAME="VACBPR" TYPE="Char">{billing_data['VACBPR']}</FLD>
                    <FLD NAME="ZVACBPR" TYPE="Char"/>
                    <FLD MENULAB="c/IVA" MENULOCAL="243" NAME="PRITYP" TYPE="Integer">{billing_data['PRITYP']}</FLD>
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
                    <FLD NAME="YPOSCOD" TYPE="Char">{client_data['YPOSCOD']}</FLD>
                    <FLD NAME="YCTY" TYPE="Char">{client_data['YCTY']}</FLD>
                    <FLD NAME="YBPIEECNUM" TYPE="Char">{client_data['YBPIEECNUM']}</FLD>
                    <FLD NAME="YILINKMAIL" TYPE="Char">{client_data['YILINKMAIL']}</FLD>
                    <FLD NAME="YPAM" TYPE="Char">{client_data['YPAM']}</FLD>
                    <LST NAME="YBPRNAM" SIZE="2" TYPE="Char">
                        <ITM>Cliente NAU via soap-ui 1</ITM>
                        <ITM>Cliente NAU via soap-ui 2</ITM>
                    </LST>
                    <LST NAME="YBPAADDLIG" SIZE="3" TYPE="Char">
                        {address_items}
                    </LST>
                </GRP>
                <GRP ID="ADXTEC">
                    <FLD NAME="WW_MODSTAMP" TYPE="Char">20231109103351</FLD>
                    <FLD NAME="WW_MODUSER" TYPE="Char">WSNAU</FLD>
                </GRP>
                <TAB DIM="300" ID="SIH4_1" SIZE="2">
                    <LIN NUM="1">
                        <FLD NAME="ITMREF" TYPE="Char">{transaction_item_data['ITMREF']}</FLD>
                        <FLD NAME="ITMDES" TYPE="Char">Genérico NAU - Formação Cientifca e Tec. </FLD>
                        <FLD NAME="ITMDES1" TYPE="Char">{transaction_item_data['ITMDES1']}</FLD>
                        <FLD NAME="YPERIODO" TYPE="Date"></FLD>
                        <FLD NAME="YPERIODOF" TYPE="Date"></FLD>
                        <FLD NAME="ECCVALMAJ" TYPE="Char"/>
                        <FLD NAME="INVPRC" TYPE="Decimal">0</FLD>
                        <FLD NAME="SAU" TYPE="Char">UN</FLD>
                        <FLD NAME="QTY" TYPE="Decimal">{transaction_item_data['QTY']}</FLD>
                        <FLD NAME="SAUSTUCOE" TYPE="Decimal">1</FLD>
                        <FLD NAME="STU" TYPE="Char">{transaction_item_data['STU']}</FLD>
                        <FLD NAME="GROPRI" TYPE="Decimal">{transaction_item_data['GROPRI']}</FLD>
                        <FLD NAME="DISCRGVAL1" TYPE="Decimal">{transaction_item_data['DISCRGVAL1']}</FLD>
                        <FLD NAME="DISCRGVAL2" TYPE="Decimal">0</FLD>
                        <FLD NAME="DISCRGVAL3" TYPE="Decimal">0</FLD>
                        <FLD NAME="DISCRGVAL4" TYPE="Decimal">0</FLD>
                        <FLD NAME="DISCRGVAL5" TYPE="Decimal">0</FLD>
                        <FLD NAME="DISCRGVAL6" TYPE="Decimal">0</FLD>
                        <FLD NAME="NETPRI" TYPE="Decimal">100</FLD>
                        <FLD NAME="CPRPRI" TYPE="Decimal">0</FLD>
                        <FLD NAME="PFM" TYPE="Decimal">81.3008</FLD>
                        <FLD NAME="VACITM1" TYPE="Char">{transaction_item_data['VACITM1']}</FLD>
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

    return response_as_xml
