from apps.billing.services.financial_processor_service import TransactionProcessorInterface


class SageX3Processor(TransactionProcessorInterface):
    """
    This class is a transaction processor. It means that by implementing the `TransactionProcessorInterface` type,
    it can be replaced by another implementation.

    The two methods `send_transaction_to_processor` and `check_transaction_in_processor` come from `TransactionProcessorInterface`,
    it signs the interface contract to implement the business logic.

    This implementation is based on the `Sage X3` saas business logic, so it means that all the particular `Sage X3` functionalities
    need to be implemented here as privated methods.
    """

    def send_transaction_to_processor(self, transaction_data) -> str:
        return "DOCUMENT_ID"

    def check_transaction_in_processor(self) -> bool:
        return False

    def __generate_data(self) -> None:
        self.__getattribute__data = """
        <soapenv:Envelope
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:wss="http://www.adonix.com/WSS">
            <soapenv:Header/>
            <soapenv:Body>
                <wss:save soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <callContext xsi:type="wss:CAdxCallContext">
                        <codeLang xsi:type="xsd:string">POR</codeLang>
                        <poolAlias xsi:type="xsd:string">WSTEST</poolAlias>
                        <poolId xsi:type="xsd:string">?</poolId>
                        <requestConfig xsi:type="xsd:string">adxwss.beautify=true</requestConfig>
                    </callContext>
                    <publicName xsi:type="xsd:string">YWSSIH</publicName>
                    <objectXml xsi:type="xsd:string">
                        <![CDATA[
                        <?xml version="1.0" encoding="utf-8" ?><PARAM><GRP ID="SIH0_1"><FLD NAME="SALFCY">SED</FLD><FLD NAME="SIVTYP">FRN</FLD><FLD NAME="NUM"></FLD><FLD NAME="INVREF">Nº Fatura NAU via SOAPUI</FLD><FLD NAME="INVDAT">20231025</FLD><FLD NAME="BPCINV">9999</FLD><FLD NAME="CUR">EUR</FLD></GRP><GRP ID="SIH1_5"><FLD NAME="VACBPR">CON</FLD><FLD NAME="PRITYP">2</FLD></GRP><GRP ID="SIH1_6"><FLD NAME="STOMVTFLG">1</FLD></GRP><GRP ID="SIH2_2"><FLD NAME="PTE">PTTRFPP</FLD></GRP><GRP ID="YIL_2"><FLD NAME="YCRY" TYPE="Char">PT</FLD><FLD NAME="YCRYNAM" TYPE="Char">Portugal</FLD><FLD NAME="YPOSCOD" TYPE="Char">2675487</FLD><FLD NAME="YCTY" TYPE="Char">Odivelas</FLD><FLD NAME="YBPIEECNUM" TYPE="Char">PT507798791</FLD><FLD NAME="YILINKMAIL" TYPE="Char">NauEmaililink@ilink.pt</FLD><FLD NAME="YPAM" TYPE="Char">MBWAY</FLD><LST NAME="YBPRNAM" SIZE="2" TYPE="Char"><ITM>Cliente NAU via soap-ui 1</ITM><ITM>Cliente NAU via soap-ui 2</ITM></LST><LST NAME="YBPAADDLIG" SIZE="3" TYPE="Char"><ITM>linha end 1</ITM><ITM>linha end 2</ITM><ITM>linha end 3</ITM></LST></GRP><TAB ID="SIH4_1"><LIN><FLD NAME="ITMREF">N0001</FLD><FLD NAME="ITMDES1">Artigo VIA SOAP UI 1</FLD><FLD NAME="QTY">10</FLD><FLD NAME="STU">UN</FLD><FLD NAME="GROPRI">100</FLD><FLD NAME="DISCRGVAL1">0</FLD><FLD NAME="VACITM1">NOR</FLD></LIN><LIN><FLD NAME="ITMREF">N0001</FLD><FLD NAME="ITMDES1">Artigo VIA SOAP UI 2</FLD><FLD NAME="QTY">20</FLD><FLD NAME="STU">UN</FLD><FLD NAME="GROPRI">50</FLD><FLD NAME="DISCRGVAL1">0</FLD><FLD NAME="VACITM1">NOR</FLD></LIN></TAB></PARAM>]]>
                    </objectXml>
                </wss:save>
            </soapenv:Body>
        </soapenv:Envelope>
        """
