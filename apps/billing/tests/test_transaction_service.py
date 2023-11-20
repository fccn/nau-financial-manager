from unittest import mock

import xmltodict
from django.conf import settings
from django.test.testcases import TestCase
from requests import Response

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.services.financial_processor_service import ProcessorInstantiator, TransactionProcessorInterface
from apps.billing.services.processor_service import SageX3Processor
from apps.billing.services.transaction_service import TransactionService


def processor_response(*args, **kwargs):
    class MockResponse(Response):
        def __init__(
            self,
            data,
            status_code,
        ):
            self.data = data
            self.status_code = status_code

        def json(self):
            return xmltodict.parse(self.data)

        @property
        def content(self):
            return str(self.data)

    return MockResponse(response_as_xml, 200)


class TransactionServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.financial_processor_interface = TransactionProcessorInterface()
        self.transaction_service = TransactionService()
        self._transaction_processor = SageX3Processor()
        self.transaction = TransactionFactory.create()
        self.transaction_item = TransactionItemFactory.create(transaction=self.transaction)
        self.processor_url = getattr(settings, "TRANSACTION_PROCESSOR_URL")

        return super().setUp()

    def test_financial_processor_service(self):
        with self.assertRaisesMessage(
            expected_exception=Exception,
            expected_message="This method needs to be implemented",
        ):
            self.financial_processor_interface.check_transaction_in_processor(transaction=self.transaction)
            self.financial_processor_interface.send_transaction_to_processor(transaction=self.transaction)

    def test_processor_instance(self):
        processor = ProcessorInstantiator(processor=SageX3Processor)

        self.assertEqual(type(processor), type(self._transaction_processor))
        self.assertEqual(type(processor), SageX3Processor)
        self.assertTrue(isinstance(processor, TransactionProcessorInterface))

    @mock.patch("requests.post", side_effect=processor_response)
    def test_transaction_processor(self, mocked_post):
        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        processor: SageX3Processor = ProcessorInstantiator(processor=SageX3Processor)
        response = processor.send_transaction_to_processor(transaction=self.transaction)

        self.assertTrue(response)
        self.assertEqual(type(response), dict)

    def tearDown(self) -> None:
        setattr(settings, "TRANSACTION_PROCESSOR_URL", self.processor_url)
        return super().tearDown()


response_as_xml = """
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
                <FLD NAME="SIVTYP" TYPE="Char">FRN</FLD>
                <FLD NAME="ZSIVTYP" TYPE="Char"/>
                <FLD NAME="NUM" TYPE="Char">FRN-23/00051</FLD>
                <FLD NAME="INVREF" TYPE="Char">Nº Fatura NAU via SOAPUI</FLD>
                <FLD NAME="INVDAT" TYPE="Date">20231025</FLD>
                <FLD NAME="BPCINV" TYPE="Char">9999</FLD>
                <FLD NAME="BPINAM" TYPE="Char">Cliente NAU via soap-ui 2</FLD>
                <FLD NAME="CUR" TYPE="Char">EUR</FLD>
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
                <FLD NAME="VACBPR" TYPE="Char"></FLD>
                <FLD NAME="ZVACBPR" TYPE="Char"/>
                <FLD MENULAB="c/IVA" MENULOCAL="243" NAME="PRITYP" TYPE="Integer">2</FLD>
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
                <FLD NAME="YPOSCOD" TYPE="Char">2675487</FLD>
                <FLD NAME="YCTY" TYPE="Char">Odivelas</FLD>
                <FLD NAME="YBPIEECNUM" TYPE="Char">PT507798791</FLD>
                <FLD NAME="YILINKMAIL" TYPE="Char">NauEmaililink@ilink.ptAAA</FLD>
                <FLD NAME="YPAM" TYPE="Char">MBWAY</FLD>
                <LST NAME="YBPRNAM" SIZE="2" TYPE="Char">
                    <ITM>Cliente NAU via soap-ui 1</ITM>
                    <ITM>Cliente NAU via soap-ui 2</ITM>
                </LST>
                <LST NAME="YBPAADDLIG" SIZE="3" TYPE="Char">
                    <ITM>linha end 1</ITM>
                    <ITM>linha end 2</ITM>
                    <ITM>linha end 3</ITM>
                </LST>
            </GRP>
            <GRP ID="ADXTEC">
                <FLD NAME="WW_MODSTAMP" TYPE="Char">20231109103351</FLD>
                <FLD NAME="WW_MODUSER" TYPE="Char">WSNAU</FLD>
            </GRP>
            <TAB DIM="300" ID="SIH4_1" SIZE="2">
                <LIN NUM="1">
                    <FLD NAME="ITMREF" TYPE="Char">N0001</FLD>
                    <FLD NAME="ITMDES" TYPE="Char">Genérico NAU - Formação Cientifca e Tec. </FLD>
                    <FLD NAME="ITMDES1" TYPE="Char">Artigo VIA SOAP UI 1</FLD>
                    <FLD NAME="YPERIODO" TYPE="Date"></FLD>
                    <FLD NAME="YPERIODOF" TYPE="Date"></FLD>
                    <FLD NAME="ECCVALMAJ" TYPE="Char"/>
                    <FLD NAME="INVPRC" TYPE="Decimal">0</FLD>
                    <FLD NAME="SAU" TYPE="Char">UN</FLD>
                    <FLD NAME="QTY" TYPE="Decimal">10</FLD>
                    <FLD NAME="SAUSTUCOE" TYPE="Decimal">1</FLD>
                    <FLD NAME="STU" TYPE="Char">UN</FLD>
                    <FLD NAME="GROPRI" TYPE="Decimal">100</FLD>
                    <FLD NAME="DISCRGVAL1" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL2" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL3" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL4" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL5" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL6" TYPE="Decimal">0</FLD>
                    <FLD NAME="NETPRI" TYPE="Decimal">100</FLD>
                    <FLD NAME="CPRPRI" TYPE="Decimal">0</FLD>
                    <FLD NAME="PFM" TYPE="Decimal">81.3008</FLD>
                    <FLD NAME="VACITM1" TYPE="Char"></FLD>
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
                <LIN NUM="2">
                    <FLD NAME="ITMREF" TYPE="Char">N0001</FLD>
                    <FLD NAME="ITMDES" TYPE="Char">Genérico NAU - Formação Cientifca e Tec. </FLD>
                    <FLD NAME="ITMDES1" TYPE="Char">Artigo VIA SOAP UI 2</FLD>
                    <FLD NAME="YPERIODO" TYPE="Date"></FLD>
                    <FLD NAME="YPERIODOF" TYPE="Date"></FLD>
                    <FLD NAME="ECCVALMAJ" TYPE="Char"/>
                    <FLD NAME="INVPRC" TYPE="Decimal">0</FLD>
                    <FLD NAME="SAU" TYPE="Char">UN</FLD>
                    <FLD NAME="QTY" TYPE="Decimal">20</FLD>
                    <FLD NAME="SAUSTUCOE" TYPE="Decimal">1</FLD>
                    <FLD NAME="STU" TYPE="Char">UN</FLD>
                    <FLD NAME="GROPRI" TYPE="Decimal">50</FLD>
                    <FLD NAME="DISCRGVAL1" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL2" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL3" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL4" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL5" TYPE="Decimal">0</FLD>
                    <FLD NAME="DISCRGVAL6" TYPE="Decimal">0</FLD>
                    <FLD NAME="NETPRI" TYPE="Decimal">50</FLD>
                    <FLD NAME="CPRPRI" TYPE="Decimal">0</FLD>
                    <FLD NAME="PFM" TYPE="Decimal">40.6504</FLD>
                    <FLD NAME="VACITM1" TYPE="Char"></FLD>
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
