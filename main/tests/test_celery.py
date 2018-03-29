from django.test import TestCase, RequestFactory
from django.conf import settings
from django.core.management import call_command
from open_humans.models import OpenHumansMember
from main.celery import read_reference, clean_raw_23andme
from main.celery_helper import vcf_header
import os
import tempfile
import requests
import requests_mock


class ParsingTestCase(TestCase):
    """
    test that files are parsed correctly
    """

    def setUp(self):
        """
        Set up the app for following tests
        """
        settings.DEBUG = True
        call_command('init_proj_config')
        self.factory = RequestFactory()
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='12345678',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()

    def test_read_reference(self):
        """
        Test function to read the reference file.
        """
        REF_23ANDME_FILE = os.path.join(os.path.dirname(__file__),
                                        'fixtures/test_reference.txt')
        ref = read_reference(REF_23ANDME_FILE)
        self.assertEqual(ref, {'1': {'82154': 'A', '752566': 'G'}})

    def test_vcf_header(self):
        """
        Test function to create a VCF header
        """
        hd = vcf_header(
            source='23andme',
            reference='http://example.com',
            format_info=['<ID=GT,Number=1,Type=String,Description="GT">'])
        self.assertEqual(len(hd), 6)
        expected_header_fields = ["##fileformat",
                                  "##fileDate",
                                  '##source',
                                  '##reference',
                                  '##FORMAT',
                                  '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER' +
                                  '\tINFO\tFORMAT\t23ANDME_DATA']
        self.assertEqual([i.split("=")[0] for i in hd], expected_header_fields)

    def test_23andme_cleaning(self):
        """
        Test that cleanup works as expected
        """
        with requests_mock.Mocker() as m:
            get_url = 'http://example.com/23andme_file.txt'
            closed_input_file = os.path.join(os.path.dirname(__file__),
                                             'fixtures/23andme_invalid.txt')
            fhandle = open(closed_input_file, "rb")
            content = fhandle.read()
            m.register_uri('GET',
                           get_url,
                           content=content,
                           status_code=200)
            tf_in = tempfile.NamedTemporaryFile(suffix=".txt")
            tf_in.write(requests.get(get_url).content)
            tf_in.flush()

            cleaned_input = clean_raw_23andme(tf_in)
            cleaned_input.seek(0)
            lines = cleaned_input.read()
            self.assertEqual(lines.find('John Doe'), -1)
            self.assertNotEqual(lines.find('data file generated'), -1)