import os.path
import unittest

import mock

import edderkop.crawler
import edderkop.receivers.collector

class FakeReceiver(object):
    pass


class Tests(unittest.TestCase):
    @mock.patch('edderkop.crawler.requests')
    def test_session_is_singleton(self, requests):
        crawler = edderkop.crawler.Crawler(FakeReceiver())

        requests.Session.assert_not_called()
        self.assertEquals(requests.Session.return_value, crawler.session)
        crawler.session
        crawler.session
        self.assertEqual(len(requests.Session.call_args_list), 1)

    @mock.patch('edderkop.crawler.Crawler.add_url')
    def test_add_urls_calls_add_url(self, add_url):
        crawler = edderkop.crawler.Crawler(FakeReceiver())

        crawler.add_urls(['http://example.com', 'http://otherexample.com'])

        crawler.add_url.assert_any_call('http://example.com')
        crawler.add_url.assert_any_call('http://otherexample.com')

    def test_add_url_discards_duplicates(self):
        crawler = edderkop.crawler.Crawler(FakeReceiver())

        crawler.add_url('http://example.com')
        crawler.add_url('http://example.com')
        crawler.add_url('http://otherexample.com')

        self.assertEqual(len(crawler.urls), 2)
        self.assertIn('http://example.com/', crawler.urls)
        self.assertIn('http://otherexample.com/', crawler.urls)

    def test_add_url_records_each_allowed_domain_only_once(self):
        crawler = edderkop.crawler.Crawler(FakeReceiver())

        crawler.add_url('http://example.com')
        crawler.add_url('http://example.com/foobar')
        crawler.add_url('http://otherexample.com')

        self.assertEqual(crawler.allowed_domains, set(['example.com', 'otherexample.com']))

    @mock.patch('edderkop.crawler.Crawler.fetch_page')
    def test_inspect_page(self, fetch_page):
        collector = edderkop.receivers.collector.Collector()

        crawler = edderkop.crawler.Crawler(collector)
        crawler.allowed_domains.add('not.example.com')
        with open(os.path.join(os.path.dirname(__file__), 'test_data', 'test.html')) as fp:
            fetch_page.return_value = fp.read()

        url = 'http://not.example.com/fakeurl'
        for _ in crawler.inspect_page(url): pass

        self.assertIn(url, collector.sitemap)
        self.assertIn('http://example.com/script.js', collector.sitemap[url].scripts)
        self.assertIn('http://not.example.com/images/img.jpg', collector.sitemap[url].images)
        self.assertIn('http://not.example.com/otherpage.html', collector.sitemap[url].links)
        self.assertIn('http://not.example.com/otherpage.html', crawler.urls)
