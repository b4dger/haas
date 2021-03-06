import os
import unittest
import boto3
from haascli.haas import cli
from click.testing import CliRunner
from moto import mock_cloudformation
from haascli import ROOT_DIR
from utils import create_stack


class TestStack(unittest.TestCase):
    '''List is simple so use it to test the parameters to stack
    '''
    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_bad_argument(self):
        r = self.runner.invoke(cli, ['stack', '-j', 'list'])
        self.assertEqual(2, r.exit_code)
        self.assertTrue('no such option' in r.output)


class TestStackList(unittest.TestCase):
    '''
    '''
    def setUp(self):
        # create runner
        self.runner = CliRunner()
        mock = mock_cloudformation()
        mock.start()
        self.mock_client = boto3.client('cloudformation')

        # open template body
        f = open(os.path.join(ROOT_DIR, 'tests', 'mock.json'), 'r')
        self.template_body = f.read()
        f.close()               # use explicit close to suppress moto warning

    def tearDown(self):
        pass

    @mock_cloudformation
    def test_list(self):
        # first created these stacks in setUp, but didn't carry over
        # "create" two stacks
        create_stack('tank', 'never', self.template_body, self.mock_client)
        create_stack('beef', 'canoe', self.template_body, self.mock_client)

        r = self.runner.invoke(cli, ['stack', 'list'])
        self.assertEqual(0, r.exit_code)
        statuses = r.output.strip().split('\n')
        self.assertEqual(2, len(statuses))
        self.assertTrue(statuses[0].startswith('tank'))
        self.assertTrue(statuses[1].startswith('beef'))

    def test_list_long(self):
        create_stack('tank', 'never', self.template_body, self.mock_client)
        create_stack('beef', 'canoe', self.template_body, self.mock_client)

        r = self.runner.invoke(cli, ['stack', 'list', '-l'])
        self.assertEqual(0, r.exit_code)
        statuses = r.output.strip().split('\n')
        self.assertEqual(6, len(statuses))
        self.assertTrue(statuses[0].startswith('tank'))
        self.assertTrue('Id' in statuses[1])
        self.assertTrue('Created' in statuses[2])
        self.assertTrue(statuses[3].startswith('beef'))
        self.assertTrue('Id' in statuses[4])
        self.assertTrue('Created' in statuses[5])

    def test_list_empty(self):
        r = self.runner.invoke(cli, ['stack', 'list'])
        self.assertEqual(0, r.exit_code)
        statuses = r.output.strip().split('\n')
        self.assertEqual(1, len(statuses))

    def test_list_empty_long(self):
        r = self.runner.invoke(cli, ['stack', 'list', '-l'])
        self.assertEqual(0, r.exit_code)
        statuses = r.output.strip().split('\n')
        self.assertEqual(1, len(statuses))

    def test_list_filter_hit(self):
        create_stack('tank', 'never', self.template_body, self.mock_client)
        create_stack('beef', 'canoe', self.template_body, self.mock_client)

        r = self.runner.invoke(cli, ['stack', 'list', '-f', 'CREATE_COMPLETE'])
        self.assertEqual(0, r.exit_code)
        statuses = r.output.strip().split('\n')
        self.assertEqual(2, len(statuses))
        self.assertTrue(statuses[0].startswith('tank'))
        self.assertTrue(statuses[1].startswith('beef'))

    def off_test_list_filter_miss(self):
        '''filtering not working for mock'''
        create_stack('tank', 'never', self.template_body, self.mock_client)
        create_stack('beef', 'canoe', self.template_body, self.mock_client)

        r = self.runner.invoke(cli, ['stack', 'list', '-f', 'DELETE_COMPLETE'])
        self.assertEqual(0, r.exit_code)
        statuses = r.output.strip().split('\n')
        self.assertEqual(1, len(statuses))

    def off_test_list_filter_bad(self):
        '''invalid status not working for mock'''
        r = self.runner.invoke(cli, ['stack', 'list', '-f', 'invalid'])
        self.assertEqual(0, r.exit_code)
