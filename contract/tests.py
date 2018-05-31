from django.test import TestCase
from contract.models import Contract
from django.utils import timezone
import datetime
import time as time_


class ContractTest(TestCase):

    def setUp(self):
        self.contract = Contract
        self.contract.client_name = "Paul"
        self.contract.project_name = "Baselink Group"
        self.contract.slug = "baselink-group"
        self.contract.project_lead = "1"
        self.contract.project_status = "Pending"
        self.contract.project_description = "This is a project to revamp the site"
        self.contract.publish_date = int(round(time_.time() * 1000))

    def test_contract_name(self):
        self.assertEqual(self.contract.client_name, 'Paul')
        self.assertNotEqual(self.contract.client_name, 'Paulo')

    def test_project_name(self):
        self.assertEqual(self.contract.project_name, 'Baselink Group')


    def test_slug(self):
        self.assertEqual(self.contract.slug, 'baselink-group')


    def test_project_lead(self):
        self.assertEqual(self.contract.project_lead, '1')


    def test_project_status(self):
        self.assertEqual(self.contract.project_status, 'Pending')


    def test_description(self):
        self.assertEqual(self.contract.project_description, 'This is a project to revamp the site')


    def test_publish_date(self):
        self.assertAlmostEqual(self.contract.publish_date, round(time_.time() * 1000))

