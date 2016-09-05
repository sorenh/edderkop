import unittest

import edderkop.utils


class UtilTests(unittest.TestCase):
    def test_target_url_full_url(self):
        self.assertEquals(edderkop.utils.target_url('http://example.com/', 'http://somewhereelse.com/'), 'http://somewhereelse.com/')

    def test_target_url_absolute_path(self):
        self.assertEquals(edderkop.utils.target_url('http://example.com', '/'), 'http://example.com/')
        self.assertEquals(edderkop.utils.target_url('http://example.com/', '/'), 'http://example.com/')
        self.assertEquals(edderkop.utils.target_url('http://example.com', '/subpage'), 'http://example.com/subpage')
        self.assertEquals(edderkop.utils.target_url('http://example.com/', '/subpage'), 'http://example.com/subpage')
        self.assertEquals(edderkop.utils.target_url('http://example.com/foo', '/subpage'), 'http://example.com/subpage')
        self.assertEquals(edderkop.utils.target_url('http://example.com/foo/', '/subpage'), 'http://example.com/subpage')

    def test_target_url_relative_path(self):
        self.assertEquals(edderkop.utils.target_url('http://example.com', 'subpage'), 'http://example.com/subpage')
        self.assertEquals(edderkop.utils.target_url('http://example.com/', 'subpage'), 'http://example.com/subpage')
        self.assertEquals(edderkop.utils.target_url('http://example.com/foo', 'subpage'), 'http://example.com/subpage')
        self.assertEquals(edderkop.utils.target_url('http://example.com/foo/', 'subpage'), 'http://example.com/foo/subpage')
        self.assertEquals(edderkop.utils.target_url('http://example.com/foo', '#'), 'http://example.com/foo')
        self.assertEquals(edderkop.utils.target_url('http://example.com/foo/', '#'), 'http://example.com/foo/')

    def test_href_usable_unusual_scheme(self):
        self.assertFalse(edderkop.utils.href_usable('gopher://'))

    def test_href_usable_javascript(self):
        self.assertFalse(edderkop.utils.href_usable('javascript:alert("hi mom")'))

    def test_href_usable_relative(self):
        self.assertTrue(edderkop.utils.href_usable('somepage'))

    def test_href_usable_absolute(self):
        self.assertTrue(edderkop.utils.href_usable('/somepage'))

    def test_href_usable_full_url(self):
        self.assertTrue(edderkop.utils.href_usable('http://example.com/somewhereelse'))
