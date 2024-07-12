from unittest import mock

from django.test import TestCase, override_settings

from apps.billing.mocks import MockResponse
from apps.billing.services.processor_service import SageX3Processor


class SageX3ProcessServiceTest(TestCase):
    """
    A test case for the ProcessService.
    """

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com/somelocation")
    @mock.patch("requests.post", return_value=MockResponse(data="", status_code=200))
    @mock.patch("apps.billing.services.processor_service.SageX3Processor.data", side_effect=lambda: {"some": "thing"})
    def test_send_transaction_to_processor_transaction_processor_url_setting(self, mock_data, mock_post):
        """
        Test the `TRANSACTION_PROCESSOR_URL` setting changes the called URL.
        """
        SageX3Processor(None).send_transaction_to_processor()
        _, kwargs = mock_post.call_args

        self.assertEqual("http://fake-processor.com/somelocation", kwargs["url"])

    @override_settings(USER_PROCESSOR_AUTH="someuser", USER_PROCESSOR_PASSWORD="somepassword")
    @mock.patch("requests.post", return_value=MockResponse(data="", status_code=200))
    @mock.patch("apps.billing.services.processor_service.SageX3Processor.data", side_effect=lambda: {"some": "thing"})
    def test_send_transaction_to_processor_user_processor_auth_password(self, mock_data, mock_post):
        """
        Test the `USER_PROCESSOR_AUTH` and `USER_PROCESSOR_PASSWORD` settings changes
        the authentication user and password.
        """
        SageX3Processor(None).send_transaction_to_processor()
        _, kwargs = mock_post.call_args
        self.assertEqual(("someuser", "somepassword"), kwargs["auth"])

    @mock.patch("requests.post", return_value=MockResponse(data="", status_code=200))
    @mock.patch("apps.billing.services.processor_service.SageX3Processor.data", side_effect=lambda: {"some": "thing"})
    def test_send_transaction_to_processor_header_content_type(self, mock_data, mock_post):
        """
        Test the Content-type HTTP header sent to SageX3 is XML.
        """
        SageX3Processor(None).send_transaction_to_processor()
        _, kwargs = mock_post.call_args
        called_headers = kwargs["headers"]
        self.assertEqual("text/xml; charset=utf-8", called_headers["Content-type"])

    @mock.patch("requests.post", return_value=MockResponse(data="", status_code=200))
    @mock.patch("apps.billing.services.processor_service.SageX3Processor.data", side_effect=lambda: {"some": "thing"})
    def test_send_transaction_to_processor_header_soapaction(self, mock_data, mock_post):
        """
        Test the SOAPAction HTTP header sent to SageX3 is XML, it should be an empty string.
        """
        SageX3Processor(None).send_transaction_to_processor()
        _, kwargs = mock_post.call_args
        called_headers = kwargs["headers"]
        self.assertEqual("''", called_headers["SOAPAction"])
