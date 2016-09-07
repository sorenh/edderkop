import unittest

import mock

import edderkop.cli
from edderkop.receivers.collector import Collector


class CLITests(unittest.TestCase):
    def test_main_raises_error_without_urls(self):
        self.assertRaises(SystemExit, edderkop.cli.main, [])

    @mock.patch('edderkop.cli.Crawler')
    def test_main_instantiates_and_runs_crawler(self, Crawler):
        self.assertTrue(edderkop.cli.main(('http://example.com',)))

        Crawler.assert_called_with(mock.ANY)
        self.assertTrue(isinstance(Crawler.call_args[0][0], Collector))

        crawler = Crawler()
        crawler.add_urls.assert_called_with(['http://example.com'])
        crawler.run.assert_called_with()
