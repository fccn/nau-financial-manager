import xml.etree.ElementTree as ET

import requests
from django.conf import settings

from apps.billing.models import Transaction, TransactionItem
from apps.billing.services.financial_processor_service import TransactionProcessorInterface


class SageX3Processor(TransactionProcessorInterface):
    """
    This class is a transaction processor. It means that by implementing the `TransactionProcessorInterface` type,
    it can be replaced by another implementation.

    The two methods `send_transaction_to_processor` and `check_transaction_in_processor` come from `TransactionProcessorInterface`,
    it signs the interface contract to implement the business logic.

    This implementation is based on the `Sage X3` saas business logic, so it means that all the particular `Sage X3` functionalities
    need to be implemented here as private methods.
    """

    def __init__(self, transaction: Transaction) -> None:
        super().__init__(transaction)
        self.__processor_url = getattr(settings, "TRANSACTION_PROCESSOR_URL")
        self.__pool_alias = getattr(settings, "POOL_ALIAS")
        self.__vacitm1 = getattr(settings, "IVA_VACITM1_FIELD")
        self.__vacbpr = getattr(settings, "GEOGRAPHIC_ACTIVITY_VACBPR_FIELD")
        self.__user_processor_auth = getattr(settings, "USER_PROCESSOR_AUTH")
        self.__user_processor_password = getattr(settings, "USER_PROCESSOR_PASSWORD")
        self.__data = None

    def _series(self):
        info = None
        try:
            info = getattr(self.transaction, "sage_x3_transaction_information")
        except Exception:
            pass
        if info:
            return info.series
        else:
            return getattr(settings, "DEFAULT_SERIES")

    def send_transaction_to_processor(self) -> dict:
        """
        This method sends the transaction informations to the `Sage X3` service.
        """
        response = requests.post(
            url=self.__processor_url,
            data=self.data,
            headers={"Content-type": "text/xml; charset=UTF-8", "SOAPAction": "''"},
            auth=(
                self.__user_processor_auth,
                self.__user_processor_password,
            ),
        ).content

        return response

    def __generate_items_as_xml(self, items: list[TransactionItem]) -> str:
        """
        This method generates items from a transaction as xml text,
        as expected for the `Sage X3` service.
        """

        items_as_xml = ""
        for item in items:
            items_as_xml = f"""
            {items_as_xml}
            <LIN>
                <FLD NAME="ITMREF">N0001</FLD>
                <FLD NAME="ITMDES1">{item.description}</FLD>
                <FLD NAME="QTY">{item.quantity}</FLD>
                <FLD NAME="STU">UN</FLD>
                <FLD NAME="GROPRI">{item.unit_price_incl_vat}</FLD>
                <FLD NAME="DISCRGVAL1">{item.discount_rate * 100}</FLD>
                <FLD NAME="VACITM1">{self.__vacitm1}</FLD>
            </LIN>
            """

        return items_as_xml

    @property
    def data(self) -> str:
        """
        This method generates the request data as xml text from a transaction,
        as expected for the `Sage X3` service.

        It uses memoization to prevent the generation of data multiple times unnecessary.
        """
        if not self.__data:
            self.__data = self.__generate_data()
        return self.__data

    def __generate_data(self) -> str:
        """
        This method generates the request data as xml text from a transaction,
        as expected for the `Sage X3` service.
        """
        transaction: Transaction = self.transaction
        items: list[TransactionItem] = transaction.transaction_items.all()
        items_as_xml = self.__generate_items_as_xml(items=items)

        transaction_id = transaction.transaction_id
        transaction_date = str(transaction.transaction_date.date().strftime("%Y%m%d"))
        vat_identification_country = getattr(transaction, "vat_identification_country", "")
        city = getattr(transaction, "city", "")
        country_code = getattr(transaction, "country_code", "")
        postal_code = transaction.postal_code
        postal_code = postal_code.replace("-", "").replace(" ", "") if postal_code else ""
        vat_identification_number = str(transaction.vat_identification_number or "")
        email = str(transaction.email or "")
        transaction_type = str(transaction.transaction_type or "")
        client_name = str(transaction.client_name or "")
        address_line_1 = str(transaction.address_line_1 or "")
        address_line_2 = str(transaction.address_line_2 or "")

        objectXML = f"""
            <PARAM>
                <GRP ID="SIH0_1">
                    <FLD NAME="SALFCY">SED</FLD>
                    <FLD NAME="SIVTYP">{self._series()}</FLD>
                    <FLD NAME="NUM"></FLD>
                    <FLD NAME="INVREF">{transaction_id}</FLD>
                    <FLD NAME="INVDAT">{transaction_date}</FLD>
                    <FLD NAME="BPCINV">9999</FLD>
                    <FLD NAME="CUR">EUR</FLD>
                </GRP>
                <GRP ID="SIH1_6">
                    <FLD NAME="VACBPR">{self.__vacbpr}</FLD>
                    <FLD NAME="PRITYP">2</FLD>
                </GRP>
                <GRP ID="SIH1_7">
                    <FLD NAME="STOMVTFLG">1</FLD>
                </GRP>
                <GRP ID="SIH2_2">
                    <FLD NAME="PTE">PTTRFPP</FLD>
                </GRP>
                <GRP ID="YIL_2">
                    <FLD NAME="YCRY" TYPE="Char">{vat_identification_country}</FLD>
                    <FLD NAME="YCRYNAM" TYPE="Char">{country_code}</FLD>
                    <FLD NAME="YPOSCOD" TYPE="Char">{postal_code}</FLD>
                    <FLD NAME="YCTY" TYPE="Char">{city}</FLD>
                    <FLD NAME="YBPIEECNUM" TYPE="Char">{vat_identification_country}{vat_identification_number}</FLD>
                    <FLD NAME="YILINKMAIL" TYPE="Char">{email}</FLD>
                    <FLD NAME="YPAM" TYPE="Char">{transaction_type}</FLD>
                    <LST NAME="YBPRNAM" SIZE="2" TYPE="Char">
                        <ITM>{client_name}</ITM>
                    </LST>
                    <LST NAME="YBPAADDLIG" SIZE="3" TYPE="Char">
                        <ITM>{address_line_1}</ITM>
                        <ITM>{address_line_2}</ITM>
                    </LST>
                </GRP>
                <TAB ID="SIH4_1">{items_as_xml}</TAB>
            </PARAM>
        """
        # objectXML = self.__class__._pretty_format_xml(objectXML, space="\t")

        data = f"""
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
                <poolAlias xsi:type="xsd:string">{self.__pool_alias}</poolAlias>
                <poolId xsi:type="xsd:string">?</poolId>
                <requestConfig xsi:type="xsd:string">adxwss.beautify=true</requestConfig>
            </callContext>
            <publicName xsi:type="xsd:string">YWSSIH</publicName>
            <objectXml xsi:type="xsd:string"><![CDATA[<?xml version="1.0" encoding="utf-8" ?>
{objectXML}]]></objectXml>
        </wss:save>
    </soapenv:Body>
</soapenv:Envelope>"""
        return data

    @staticmethod
    def _pretty_format_xml(data, space="  ", level=0):
        element = ET.XML(data)
        ET.indent(element, space=space, level=level)
        pretty = ET.tostring(element, encoding="unicode")
        return pretty
