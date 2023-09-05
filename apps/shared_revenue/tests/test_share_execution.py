from django.test import TestCase

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.factories import ShareExecutionFactory


class ShareExecutionTestCase(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.share_execution = ShareExecutionFactory(organization=self.organization)

    def test_str_method(self):
        self.assertEqual(
            str(self.share_execution),
            f"{self.organization} - {self.share_execution.revenue_configuration} - {self.share_execution.percentage}",
        )

    def test_executed_default(self):
        self.assertFalse(self.share_execution.executed)

    def test_organization_required(self):
        with self.assertRaises(TypeError):
            ShareExecutionFactory(
                revenue_configuration={"foo": "bar"},
                percentage=50.0,
                value=1000.0,
                receipt="ABC123",
                executed=False,
                response_payload={"baz": "qux"},
            )

    def test_percentage_required(self):
        with self.assertRaises(TypeError):
            ShareExecutionFactory(
                organization=self.organization,
                revenue_configuration={"foo": "bar"},
                value=1000.0,
                receipt="ABC123",
                executed=False,
                response_payload={"baz": "qux"},
            )

    def test_value_required(self):
        with self.assertRaises(TypeError):
            ShareExecutionFactory(
                organization=self.organization,
                revenue_configuration={"foo": "bar"},
                percentage=50.0,
                receipt="ABC123",
                executed=False,
                response_payload={"baz": "qux"},
            )

    def test_receipt_required(self):
        with self.assertRaises(TypeError):
            ShareExecutionFactory(
                organization=self.organization,
                revenue_configuration={"foo": "bar"},
                percentage=50.0,
                value=1000.0,
                executed=False,
                response_payload={"baz": "qux"},
            )

    def test_response_payload_required(self):
        with self.assertRaises(TypeError):
            ShareExecutionFactory(
                organization=self.organization,
                revenue_configuration={"foo": "bar"},
                percentage=50.0,
                value=1000.0,
                receipt="ABC123",
                executed=False,
            )

    def test_revenue_configuration_optional(self):
        share_execution = ShareExecutionFactory(
            organization=self.organization,
            percentage=50.0,
            value=1000.0,
            receipt="ABC123",
            executed=False,
            response_payload={"baz": "qux"},
        )
        self.assertIsNone(share_execution.revenue_configuration)
