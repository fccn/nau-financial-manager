from enum import Enum

import xmltodict

from apps.billing.mocks import MockResponse, xml_duplicate_error_response_mock, xml_success_response_mock

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
