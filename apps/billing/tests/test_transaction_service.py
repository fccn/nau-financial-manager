from enum import Enum
from unittest import mock

import xmltodict
from django.conf import settings
from django.test.testcases import TestCase
from requests.exceptions import Timeout

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.mocks import MockResponse, xml_duplicate_error_response_mock, xml_success_response_mock
from apps.billing.services.financial_processor_service import TransactionProcessorInterface
from apps.billing.services.transaction_service import TransactionService

nau_data = {}
billing_data = {}
client_data = {}
transaction_item_data = {}


class ProcessorResponseType(Enum):
    SUCCESS = 1
    DUPLICATE_ERROR = 2
    GENERAL_ERROR = 3


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


def processor_success_response(*args, **kwargs):
    """
    This method is a mock, when the `requests.post` method is called from the test,
    the result of the request will be returned from this method.
    """

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
        response_type=ProcessorResponseType.SUCCESS,
    )

    return MockResponse(response_as_xml, 200)


def processor_duplicate_error_response(*args, **kwargs):
    response_as_xml = generate_data_to_response(
        transaction_item_data=transaction_item_data,
        response_type=ProcessorResponseType.DUPLICATE_ERROR,
    )

    return MockResponse(response_as_xml, 200)


def processor_timeout_exception_response(*args, **kwargs):
    response_as_xml = ""

    return MockResponse(response_as_xml, 408)


class TransactionServiceTestCase(TestCase):
    def setUp(self) -> None:
        """
        This method instantiates all the necessary components, get the url for transaction processor service
        and creates a combination of one `Transaction` and `TransactionItem`.
        """

        self.transaction = TransactionFactory.create()
        self.transaction_item = TransactionItemFactory.create(transaction=self.transaction)
        self.processor_url = getattr(settings, "TRANSACTION_PROCESSOR_URL")
        self.transaction_service = TransactionService(transaction=self.transaction)

    def test_financial_processor_service_interface(self):
        """
        This test ensures that if not implemented, the method from the interface
        will raise an exception.

        """
        with self.assertRaisesMessage(
            expected_exception=Exception,
            expected_message="This method needs to be implemented",
        ):
            TransactionProcessorInterface().send_transaction_to_processor()

    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_transaction_to_processor_success(self, mocked_post):
        """
        This test ensures the success result from the processor.

        Calling the `self.transaction_service.send_transaction_to_processor`, it deals with the success result
        and extracts the document id from response payload.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        document_id: str = self.transaction_service.send_transaction_to_processor()

        self.assertTrue(isinstance(document_id, str))
        self.assertNotEqual(document_id, "")
        self.assertTrue(document_id.startswith("FRN-"))

    @mock.patch("requests.post", side_effect=processor_duplicate_error_response)
    def test_transaction_to_processor_duplicate_error(self, mocked_post):
        """
        This test ensures the duplicate result from the processor.

        Calling the `self.transaction_service.send_transaction_to_processor`, it deals with the duplicate result
        and extracts the document id from response payload that indicates the duplicate information.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        document_id: str = self.transaction_service.send_transaction_to_processor()

        self.assertTrue(isinstance(document_id, str))
        self.assertNotEqual(document_id, "")
        self.assertTrue(document_id.startswith("FRN-"))

    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_run_steps_to_send_transaction(self, mocked_post):
        """
        This test ensures the success triggering the method that runs each step to send a
        transaction to processor.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        self.transaction_service.run_steps_to_send_transaction()

    @mock.patch("requests.post", side_effect=Timeout)
    def test_transaction_to_processor_timeout_error(self, mocked_post):
        """
        This test ensures that the transaction service correctly handles a timeout error from the processor.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        with self.assertRaises(Timeout):
            self.transaction_service.send_transaction_to_processor()

    def tearDown(self) -> None:
        """
        This method is called in the last moment of the `TestCase` class and sets the `TRANSACTION_PROCESSOR_URL`
        varible as the real service url again.
        """
        setattr(settings, "TRANSACTION_PROCESSOR_URL", self.processor_url)


def generate_data_to_response(
    transaction_item_data: dict,
    response_type: ProcessorResponseType,
    nau_data: dict = None,
    billing_data: dict = None,
    client_data: dict = None,
):

    if response_type not in ProcessorResponseType:
        raise "Invalid response type"

    if response_type == ProcessorResponseType.SUCCESS:
        address_items = ""
        for address in client_data["YBPAADDLIG"]:
            address_items = f"{address_items}<ITM>{address}</ITM>"

        data = {
            "transaction_item_data": transaction_item_data,
            "nau_data": nau_data,
            "billing_data": billing_data,
            "client_data": client_data,
            "address_items": address_items,
        }

        return xml_success_response_mock(data)

    if response_type == ProcessorResponseType.DUPLICATE_ERROR:
        return xml_duplicate_error_response_mock()
