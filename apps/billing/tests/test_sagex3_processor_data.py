import xml.etree.ElementTree as ET
from datetime import datetime

from django.test import TestCase, override_settings

from apps.billing.factories import SageX3TransactionInformationFactory, TransactionFactory, TransactionItemFactory
from apps.billing.models import Transaction
from apps.billing.services.processor_service import SageX3Processor


class SageX3ProcessDataTest(TestCase):
    """
    A test case for the SageX3Processor data property.
    """

    @override_settings(POOL_ALIAS="MY_POOL")
    def test_pool_alias(self):
        transaction = TransactionFactory()
        xml = SageX3Processor(transaction).data
        root = ET.fromstring(xml)  # nosec
        poolAlias: str = root.findall(".//*/poolAlias")[0].text.strip()
        self.assertEqual(poolAlias, "MY_POOL")

    @staticmethod
    def _get_xml_element_from_transaction(transaction: Transaction) -> ET.Element:
        xml = SageX3Processor(transaction).data
        root = ET.fromstring(xml)  # nosec
        object_xml: str = root.findall(".//*/objectXml")[0].text.strip()
        return ET.fromstring(object_xml)  # nosec

    def test_data_processor_transaction_id(self):
        """
        Test the SageX3Processor for transaction_id field.
        """
        transaction_id = "NAU00653"
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(transaction_id=transaction_id)
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='INVREF']"), transaction_id)

    def test_data_processor_transaction_date(self):
        """
        Test the SageX3Processor for transaction_date field.
        """
        transaction_date = datetime.now()
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(transaction_date=transaction_date)
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='INVDAT']"), transaction_date.strftime("%Y-%m-%d"))

    @override_settings(GEOGRAPHIC_ACTIVITY_VACBPR_FIELD="XPTO")
    def test_data_processor_geographic_activity_override(self):
        """
        Test the SageX3Processor for geographic activity field.
        """
        transaction_date = datetime.now()
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(transaction_date=transaction_date)
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='VACBPR']"), "XPTO")

    def test_data_processor_geographic_activity_default(self):
        """
        Test the SageX3Processor for geographic activity field.
        """
        transaction_date = datetime.now()
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(transaction_date=transaction_date)
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='VACBPR']"), "CON")

    def test_data_processor_vat_identification_country_france(self):
        """
        Test the SageX3Processor for vat identification country field for france
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(vat_identification_country="FR")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YCRY']"), "FR")

    def test_data_processor_vat_identification_country_portugal(self):
        """
        Test the SageX3Processor for vat identification country field for portugal
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(vat_identification_country="PT")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YCRY']"), "PT")

    def test_data_processor_vat_identification_country_portugal_alpha2(self):
        """
        Test the SageX3Processor for vat identification country field for Portugal
        is using the correct format of 2 digits to represent the country.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(vat_identification_country="PRT")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YCRY']"), "PT")

    def test_data_processor_vat_identification_country_none(self):
        """
        Test the SageX3Processor for vat identification country field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(vat_identification_country=None)
        )
        self.assertEqual(object_xml_root.find(".//*/FLD[@NAME='YCRY']").text, None)

    def test_data_processor_country_code_portugal(self):
        """
        Test the SageX3Processor for country code field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(country_code="PT")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YCRYNAM']"), "Portugal")

    def test_data_processor_country_code_great_britain_in_portuguese(self):
        """
        Test the SageX3Processor for country code field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(country_code="GBR")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YCRYNAM']"), "Reino Unido")

    def test_data_processor_country_code_none(self):
        """
        Test the SageX3Processor for country code field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(country_code=None)
        )
        self.assertEqual(object_xml_root.find(".//*/FLD[@NAME='YCRYNAM']").text, None)

    def test_data_processor_postal_code_portugal(self):
        """
        Test the SageX3Processor for country code field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(postal_code="1249-068")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YPOSCOD']"), "1249068")

    def test_data_processor_postal_code_france(self):
        """
        Test the SageX3Processor for country code field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(postal_code="93600")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YPOSCOD']"), "93600")

    def test_data_processor_postal_code_none(self):
        """
        Test the SageX3Processor for country code field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(postal_code=None)
        )
        self.assertEqual(object_xml_root.find(".//*/FLD[@NAME='YPOSCOD']").text, None)

    def test_data_processor_vat_identification_number_corporate(self):
        """
        Test the SageX3Processor for country code field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(vat_identification_country="ES", vat_identification_number="A123456789")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YBPIEECNUM']"), "ESA123456789")

    def test_data_processor_email(self):
        """
        Test the SageX3Processor for email field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(email="example@email.com")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YILINKMAIL']"), "example@email.com")

    def test_data_processor_email_none(self):
        """
        Test the SageX3Processor for email field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(TransactionFactory(email=None))
        self.assertEqual(object_xml_root.find(".//*/FLD[@NAME='YILINKMAIL']").text, None)

    def test_data_processor_transaction_type_credit(self):
        """
        Test the SageX3Processor for transaction_type field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(transaction_type="credit")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YPAM']"), "credit")

    def test_data_processor_transaction_type_none(self):
        """
        The transaction_type is a required field.
        """
        with self.assertRaises(Exception):
            self.__class__._get_xml_element_from_transaction(TransactionFactory(transaction_type=None))

    def test_data_processor_transaction_type_strange(self):
        """
        Test the SageX3Processor for transaction_type field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(transaction_type="strange")
        )
        self.assertEqual(object_xml_root.findtext(".//*/FLD[@NAME='YPAM']"), "strange")

    def test_data_processor_client_name(self):
        """
        Test the SageX3Processor for client name field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(client_name="John Snow")
        )
        self.assertEqual(object_xml_root.findtext(".//*/LST[@NAME='YBPRNAM']/ITM"), "John Snow")

    def test_data_processor_client_name_special_character(self):
        """
        Test the SageX3Processor for client name field with special character.
        This tests if the xml is encoded on utf-8.
        """
        xml = SageX3Processor(TransactionFactory(client_name="Ana Rosário Maria")).data
        self.assertIn(b"Ana Ros\xc3\xa1rio Maria", xml)

    def test_data_processor_client_name_none(self):
        """
        Test the SageX3Processor for email field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(client_name=None)
        )
        self.assertEqual(object_xml_root.find(".//*/LST[@NAME='YBPRNAM']/ITM").text, None)

    def test_data_processor_address_line_1(self):
        """
        Test the SageX3Processor for address_line_1 field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(address_line_1="Estrada Nacional nº1")
        )
        self.assertEqual(object_xml_root.findall(".//*/LST[@NAME='YBPAADDLIG']/ITM")[0].text, "Estrada Nacional nº1")

    def test_data_processor_address_line_1_none(self):
        """
        Test the SageX3Processor for address_line_1 field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(address_line_1=None)
        )
        self.assertEqual(object_xml_root.find(".//*/LST[@NAME='YBPAADDLIG']/ITM").text, None)

    def test_data_processor_address_line_2(self):
        """
        Test the SageX3Processor for address_line_2 field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(address_line_2="Uma localidade")
        )
        self.assertEqual(object_xml_root.findall(".//*/LST[@NAME='YBPAADDLIG']/ITM")[1].text, "Uma localidade")

    def test_data_processor_address_line_2_none(self):
        """
        Test the SageX3Processor for address_line_2 field.
        """
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(
            TransactionFactory(address_line_2=None)
        )
        self.assertFalse(object_xml_root.findall(".//*/LST[@NAME='YBPAADDLIG']/ITM")[1].text)

    def test_data_processor_custom_series(self):
        """
        Test the SageX3Processor for a custom series.
        """
        transaction = TransactionFactory()
        SageX3TransactionInformationFactory(transaction=transaction, series="Some")
        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction)
        self.assertEqual(object_xml_root.findall(".//*/FLD[@NAME='SIVTYP']")[0].text, "Some")

    # def test_data_object_xml_is_formatted(self):
    #     """
    #     Test the SageX3Processor for a custom series.
    #     """
    #     transaction = TransactionFactory()
    #     SageX3TransactionInformationFactory(transaction=transaction, series="Some")
    #     xml = SageX3Processor(transaction).data
    #     root = ET.fromstring(xml)  # nosec
    #     object_xml: str = root.findall(".//*/objectXml")[0].text.strip()

    #     # pretty
    #     element = ET.XML(object_xml)
    #     ET.indent(element, space="\t")
    #     pretty = ET.tostring(element, encoding="unicode")

    #     param_idx = object_xml.index("<PARAM>")
    #     object_xml_without_1st_line = object_xml[param_idx:]

    #     self.assertEqual(object_xml_without_1st_line, pretty)

    def test_data_processor_items_ITEMREF_field(self):
        """
        This test validates the content of `ITEMREF` field.
        """

        transaction = TransactionFactory.create()
        items_quantity = 5

        TransactionItemFactory.create_batch(items_quantity, **{"transaction_id": transaction.id})

        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction=transaction)
        items_as_xml = object_xml_root.findall("./TAB/")

        self.assertEqual(len(items_as_xml), items_quantity)

        for xml in items_as_xml:
            field_ITMREF = xml.find("./*[@NAME='ITMREF']").text
            self.assertEqual(field_ITMREF, "N0001")

    def test_data_processor_items_ITMDES_ITMDES1_fields(self):
        """
        This test validates the content of `ITMDES` and `ITMDES1` fields.
        """

        transaction = TransactionFactory.create()
        items_quantity = 5
        items = []

        for i in range(0, items_quantity):
            item_data = {"transaction_id": transaction.id, "description": f"This is the item at position {i}"}

            item = TransactionItemFactory.create(**item_data)
            items.append(item)

        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction=transaction)
        items_as_xml = object_xml_root.findall("./TAB/")

        self.assertEqual(len(items_as_xml), items_quantity)

        for i in range(0, items_quantity):
            self.assertEqual(items[i].description, f"This is the item at position {i}")

            item_xml = [
                xml
                for xml in items_as_xml
                if xml.find("./*[@NAME='ITMDES']").text == items[i].description
                and xml.find("./*[@NAME='ITMDES1']").text == items[i].description
            ][0]

            self.assertIsNotNone(item_xml)

            self.assertEqual(item_xml.find("./*[@NAME='ITMDES']").text, f"This is the item at position {i}")
            self.assertEqual(item_xml.find("./*[@NAME='ITMDES1']").text, f"This is the item at position {i}")

    def test_data_processor_items_description_special_character(self):
        """
        This test validates the content of `ITMDES` and `ITMDES1` fields with special character.
        """

        transaction = TransactionFactory.create()

        item_data = {"transaction_id": transaction.id, "description": "This item was bought by Ana Rosário Maria"}
        item = TransactionItemFactory.create(**item_data)

        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction=transaction)
        items_as_xml = object_xml_root.findall("./TAB/")

        self.assertEqual(len(items_as_xml), 1)
        self.assertEqual(item.transaction_id, transaction.id)

        item_xml = [xml for xml in items_as_xml if xml.find("./*[@NAME='ITMDES']").text == item.description][0]

        self.assertIsNotNone(item_xml)

        decoded_name = b"Ana Ros\xc3\xa1rio Maria".decode()

        self.assertIn(decoded_name, item_xml.find("./*[@NAME='ITMDES']").text)
        self.assertIn(decoded_name, item_xml.find("./*[@NAME='ITMDES1']").text)

    def test_data_processor_items_QTY_field(self):
        """
        This test validates the content of `QTY` field.
        """

        transaction = TransactionFactory.create()
        items_quantity = 5

        item_data = {"transaction_id": transaction.id, "quantity": items_quantity}
        item = TransactionItemFactory.create(**item_data)

        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction=transaction)
        items_as_xml = object_xml_root.findall("./TAB/")

        self.assertEqual(len(items_as_xml), 1)
        self.assertEqual(item.transaction_id, transaction.id)

        item_xml = [xml for xml in items_as_xml if xml.find("./*[@NAME='ITMDES']").text == item.description][0]

        self.assertIsNotNone(item_xml)
        self.assertEqual(int(item_xml.find("./*[@NAME='QTY']").text), items_quantity)

    def test_data_processor_items_UN_field(self):
        """
        This test validates the content of `UN` field.
        """

        transaction = TransactionFactory.create()
        items_quantity = 5

        TransactionItemFactory.create_batch(items_quantity, **{"transaction_id": transaction.id})

        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction=transaction)
        items_as_xml = object_xml_root.findall("./TAB/")

        self.assertEqual(len(items_as_xml), items_quantity)

        for xml in items_as_xml:
            field_ITMREF = xml.find("./*[@NAME='STU']").text
            self.assertEqual(field_ITMREF, "UN")

    def test_data_processor_items_GROPRI_field(self):
        """
        This test validates the content of `GROPRI` field.
        """

        transaction = TransactionFactory.create()
        unit_price_incl_vat = 20.35

        item_data = {"transaction_id": transaction.id, "unit_price_incl_vat": unit_price_incl_vat}
        item = TransactionItemFactory.create(**item_data)

        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction=transaction)
        items_as_xml = object_xml_root.findall("./TAB/")

        self.assertEqual(len(items_as_xml), 1)
        self.assertEqual(item.transaction_id, transaction.id)

        item_xml = [xml for xml in items_as_xml if xml.find("./*[@NAME='ITMDES']").text == item.description][0]

        self.assertIsNotNone(item_xml)
        self.assertEqual(float(item_xml.find("./*[@NAME='GROPRI']").text), unit_price_incl_vat)

    def test_data_processor_items_DISCRGVAL1_field(self):
        """
        This test validates the content of `DISCRGVAL1` field.
        """

        transaction = TransactionFactory.create()
        discount_incl_tax = 0.3
        unit_price_incl_vat = 20.35

        item_data = {
            "transaction_id": transaction.id,
            "discount_incl_tax": discount_incl_tax,
            "unit_price_incl_vat": unit_price_incl_vat,
        }
        item = TransactionItemFactory.create(**item_data)

        discount_rate = round(discount_incl_tax / (unit_price_incl_vat + discount_incl_tax), 2)

        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction=transaction)
        items_as_xml = object_xml_root.findall("./TAB/")

        self.assertEqual(len(items_as_xml), 1)
        self.assertEqual(item.transaction_id, transaction.id)

        item_xml = [xml for xml in items_as_xml if xml.find("./*[@NAME='ITMDES']").text == item.description][0]

        self.assertIsNotNone(item_xml)
        self.assertEqual(float(item_xml.find("./*[@NAME='GROPRI']").text), unit_price_incl_vat)
        self.assertEqual(float(item_xml.find("./*[@NAME='DISCRGVAL1']").text), discount_rate * 100)

    @override_settings(IVA_VACITM1_FIELD="IVA_VACITM1_FIELD_TO_TEST")
    def test_data_processor_items_VACITM1_field(self):
        """
        This test validates the content of `VACITM1` field.
        """

        transaction = TransactionFactory.create()

        item = TransactionItemFactory.create(**{"transaction_id": transaction.id})

        object_xml_root: ET.Element = self.__class__._get_xml_element_from_transaction(transaction=transaction)
        items_as_xml = object_xml_root.findall("./TAB/")

        self.assertEqual(len(items_as_xml), 1)
        self.assertEqual(item.transaction_id, transaction.id)

        item_xml = [xml for xml in items_as_xml if xml.find("./*[@NAME='ITMDES']").text == item.description][0]

        self.assertIsNotNone(item_xml)
        self.assertEqual(item_xml.find("./*[@NAME='VACITM1']").text, "IVA_VACITM1_FIELD_TO_TEST")
